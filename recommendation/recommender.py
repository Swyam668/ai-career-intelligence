import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "tfidf_vectorizer.pkl")
vectorizer = joblib.load(MODEL_PATH)
VECTOR_PATH = os.path.join(BASE_DIR, "..", "models", "job_vectors.pkl")
job_vectors = joblib.load(VECTOR_PATH)


def match_percentage(user_skills, job_skills):
    if not job_skills:
        return 0

    return round(
        len(user_skills & job_skills)
        / len(job_skills)
        * 100,
        2
    )

# for json response
def build_recommendations(
    user_skills,
    df,
    top_idx,
    scores
):
    recommendations = []

    for idx, similarity_score in zip(top_idx, scores):

        row = df.iloc[idx]

        job_skills = row["extracted_skills"]

        matched = user_skills & job_skills

        missing = job_skills - user_skills

        recommendations.append({
            "job_title": row["Job Title"],
            "role": row["Role"],
            "qualifications": row["Qualifications"],
            "experience": row["Experience"],

            "similarity_score": round(
                float(similarity_score),
                4
            ),

            "match_percentage": match_percentage(
                user_skills,
                job_skills
            ),

            "matched_skills": sorted(list(matched)),

            "missing_skills": sorted(
                list(missing)
            )[:10]
        })

    return recommendations


def recommend_jobs(user_profile, df, vectorizer, job_vectors, top_n=50):

    # user_text = " ".join(list(user_profile["skills"]))
    user_skills = set(user_profile["skills"])

    user_text = " ".join(user_skills)
    
    user_vector = vectorizer.transform([user_text])

    scores = cosine_similarity(user_vector, job_vectors).flatten()

    top_idx = scores.argsort()[-top_n:][::-1]

    unique_idx = []
    seen = set()

    for idx in top_idx:

        row = df.iloc[idx]

        key = (
            str(row["Job Title"]).lower(),
            str(row["Role"]).lower()
        )

        if key not in seen:
            seen.add(key)
            unique_idx.append(idx)

    recommendations = build_recommendations(
        user_skills,
        df,
        top_idx,
        scores[unique_idx]
    )

    return recommendations
    # return df.iloc[top_idx][["Job Title", "skills", "Role", "Qualifications", "Experience"]], scores[top_idx]