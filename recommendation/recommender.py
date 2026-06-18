import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "tfidf_vectorizer.pkl")
vectorizer = joblib.load(MODEL_PATH)
VECTOR_PATH = os.path.join(BASE_DIR, "..", "models", "job_vectors.pkl")
job_vectors = joblib.load(VECTOR_PATH)

def recommend_jobs(user_profile, df, vectorizer, job_vectors, top_n=10):

    user_text = " ".join(list(user_profile["skills"]))

    user_vector = vectorizer.transform([user_text])

    scores = cosine_similarity(user_vector, job_vectors).flatten()

    top_idx = scores.argsort()[-top_n:][::-1]

    return df.iloc[top_idx][["Job Title", "skills", "Role", "Qualifications", "Experience"]], scores[top_idx]