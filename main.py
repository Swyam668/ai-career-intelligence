import pandas as pd
import joblib
from pipelines.inference import run_pipeline
import os
import pdfplumber
import ast
from sentence_transformers import SentenceTransformer
import fitz


df = pd.read_csv("data/processed/jobs_processed.csv")
# reconversion to set (because it gets converted to string when reextracting)
df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")
vectorizer = joblib.load(MODEL_PATH)
VECTOR_PATH = os.path.join(BASE_DIR, "models", "job_vectors.pkl")
job_vectors = joblib.load(VECTOR_PATH)
SALARY_MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_prediction_pipeline.pkl")


vectorizer = joblib.load(MODEL_PATH)
job_vectors = joblib.load(VECTOR_PATH)
salary_model = joblib.load(SALARY_MODEL_PATH)



# not using this, better version is below
# def extract_pdf_text(path):
#     text = ""

#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""

#     return text


def extract_text_from_pdf(pdf_path: str) -> str:

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text

resume_text = extract_text_from_pdf("docs/Resume2.pdf")

nlp_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

result = run_pipeline(
    resume_text,
    df,
    vectorizer,
    job_vectors,
    salary_model,
    nlp_model
)

print(result["profile"])
print(result["predicted_salary"])
print(result["recommendations"])
# print(result["scores"])