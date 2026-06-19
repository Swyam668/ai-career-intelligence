from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import joblib
import ast
import os
from pipelines.inference import run_pipeline
from utils.pdf_parser import extract_pdf_text
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer


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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    resume_text: str


@app.get("/")
def home():
    return {"message": "API working"}


@app.post("/recommend")
def recommend(request: ResumeRequest):

    result = run_pipeline(
        request.resume_text,
        df,
        vectorizer,
        job_vectors,
        None
    )

    return result

# for debugging
@app.post("/pdf-text")
async def pdf_text(
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


@app.post("/recommend-pdf")
async def recommend_pdf(
    file: UploadFile = File(...)
):

    pdf_bytes = await file.read()

    resume_text = extract_pdf_text(
        pdf_bytes
    )

    result = run_pipeline(
        resume_text,
        df,
        vectorizer,
        job_vectors,
        salary_model,
        nlp_model
    )

    return {
    "profile": result["profile"],
    "recommendations": result["recommendations"],
    "predicted_salary": result["predicted_salary"]
}