from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import joblib
import ast
import os
from pipelines.inference import run_pipeline
from utils.pdf_parser import extract_pdf_text
from fastapi.middleware.cors import CORSMiddleware
# NLP
from sentence_transformers import SentenceTransformer
# SHAP
from salary.shap_explainer import create_salary_explainer, explain_salary_prediction
import json
import hashlib

#ROADMAP GEN
from roadmap_generator.roadmap_generator import generate_career_roadmap
from typing import List, Dict, Any


from utils.redis_client import redis_client

import time


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



df = pd.read_csv("data/processed/jobs_processed.csv")
df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "models", "job_vectors.pkl")
SALARY_MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_prediction_pipeline.pkl")

vectorizer = joblib.load(MODEL_PATH)
job_vectors = joblib.load(VECTOR_PATH)
salary_model = joblib.load(SALARY_MODEL_PATH)

nlp_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# SHAP
BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "shap_background.csv"
)

# def load_background_data():
#     return pd.read_csv(BACKGROUND_PATH)


explainer = create_salary_explainer(salary_model)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class ResumeRequest(BaseModel):
#     resume_text: str




def generate_roadmap_cache_key(
    profile: Dict[str, Any],
    recommendations: List[Dict[str, Any]]
) -> str:
    
    cache_data = {
        "profile": profile,
        "recommendations": recommendations
    }

    serialized_data = json.dumps(
        cache_data,
        # the dictionary key order won't accidentally produce different cache keys for logically identical data.
        sort_keys=True,
        default=str
    )

    request_hash = hashlib.sha256(
        serialized_data.encode("utf-8")
    ).hexdigest()

    return f"roadmap:{request_hash}"


@app.get("/")
def home():
    return {"message": "API working"}

@app.get("/health")
def health():
    return {"status": "ok"}

# @app.post("/recommend")
# def recommend(request: ResumeRequest):

#     result = run_pipeline(
#         request.resume_text,
#         df,
#         vectorizer,
#         job_vectors,
#         None
#     )

#     return result

# for debugging
@app.post("/pdf-text")
async def pdf_text(
    # ... for required
    # File tells fastapi that this comes from file upload field (from multipart)
    file: UploadFile = File(...)
):

    pdf_bytes = await file.read()

    text = extract_pdf_text(
        pdf_bytes
    )

    return {
        "characters": len(text),
        "preview": text[:500]
    }


def generate_analysis_cache_key(pdf_bytes: bytes) -> str:
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    return f"analysis:{pdf_hash}"


@app.post("/recommend-pdf")
async def recommend_pdf(
    file: UploadFile = File(...)
):
    # start_time = time.perf_counter()

    pdf_bytes = await file.read()

    cache_key = generate_analysis_cache_key(pdf_bytes)

    cached_result = None

    try:
        cached_result = await redis_client.get(cache_key)
    except Exception as e:
        logger.warning(f"Redis unavailable while reading analysis cache: {e}")


    if cached_result:
        # elapsed = time.perf_counter() - start_time
        # print(f"Analysis CACHE HIT: {elapsed:.4f}s")

        return {
            **json.loads(cached_result),
            "cached": True
        }
    

    resume_text = extract_pdf_text(pdf_bytes)

    result = run_pipeline(
        resume_text,
        df,
        vectorizer,
        job_vectors,
        salary_model,
        nlp_model,
        explainer,
        explain_salary_prediction
    )

    response = {
        "profile": result["profile"],
        "recommendations": result["recommendations"],
        "salary": result["salary"],
    }

    try:
        await redis_client.setex(
            cache_key,
            1800,
            json.dumps(response, default=str)
        )
    except Exception as e:
        logger.warning(f"Redis unavailable while writing analysis cache: {e}")

    # elapsed = time.perf_counter() - start_time
    # print(f"Analysis CACHE MISS: {elapsed:.4f}s")

    return {
        **response,
        "cached": False
    }



class RoadmapRequest(BaseModel):
    profile: Dict[str, Any]
    recommendations: List[Dict[str, Any]]




@app.post("/generate-roadmap")
async def generate_roadmap(request: RoadmapRequest):

    # start_time = time.perf_counter()

    cache_key = generate_roadmap_cache_key(
        request.profile,
        request.recommendations
    )

    cached_roadmap = None

    try:
        cached_roadmap = await redis_client.get(cache_key)
    except Exception as e:
        logger.warning(f"Redis unavailable while reading roadmap cache: {e}")


    if cached_roadmap:
        # elapsed = time.perf_counter() - start_time

        # print(f"Redis CACHE HIT: {elapsed:.4f}s")

        return {
            "roadmap": json.loads(cached_roadmap),
            "cached": True
        }

    roadmap = generate_career_roadmap(
        user_profile=request.profile,
        recommendations=request.recommendations,
        mode="llm"
    )

    try:
        await redis_client.setex(
            cache_key,
            # roadmap stays cached for 1 hour
            3600,
            json.dumps(roadmap, default=str)
        )
    
    except Exception as e:
        logger.warning(f"Redis unavailable while writing roadmap cache: {e}")

    # elapsed = time.perf_counter() - start_time

    # print(f"Redis CACHE MISS: {elapsed:.4f}s")

    return {
        "roadmap": roadmap,
        "cached": False
    }