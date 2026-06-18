from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import joblib
import ast
import os
from pipelines.inference import run_pipeline
from utils.pdf_parser import extract_pdf_text


df = pd.read_csv("data/processed/jobs_processed.csv")
df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "models", "job_vectors.pkl")

vectorizer = joblib.load(MODEL_PATH)
job_vectors = joblib.load(VECTOR_PATH)



app = FastAPI()


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
        None
    )

    return {
    "candidate_profile": result["profile"],
    "total_recommendations": len(
        result["recommendations"]
    ),
    "recommendations": result["recommendations"]
}