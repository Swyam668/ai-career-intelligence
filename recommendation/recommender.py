import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os
import ast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "tfidf_vectorizer.pkl")
vectorizer = joblib.load(MODEL_PATH)

VECTOR_PATH = os.path.join(BASE_DIR, "..", "models", "job_vectors.pkl")
job_vectors = joblib.load(VECTOR_PATH)


def ensure_skill_set(skills):
    # Converts extracted_skills into a clean Python set
    # Handles set, list, tuple, stringified list/set, and empty values

    if skills is None:
        return set()

    # handling in case, skills are in different format, for example say in CSV (its a string)
    if isinstance(skills, set):
        return {str(skill).lower().strip() for skill in skills}

    if isinstance(skills, list) or isinstance(skills, tuple):
        return {str(skill).lower().strip() for skill in skills}

    if isinstance(skills, str):
        try:
            # conversion to actual python ds
            parsed = ast.literal_eval(skills)

            if isinstance(parsed, set) or isinstance(parsed, list) or isinstance(parsed, tuple):
                return {str(skill).lower().strip() for skill in parsed}

        except Exception:
            return set()

    return set()


def match_percentage(user_skills, job_skills):
    if not job_skills:
        return 0

    return round(
        len(user_skills & job_skills) / len(job_skills) * 100,
        2
    )


def build_user_recommendation_text(user_profile):
    skills_text = " ".join(user_profile.get("skills", []))

    return " ".join([
        str(user_profile.get("job_title", "")),
        str(user_profile.get("education_level", "")),
        str(user_profile.get("industry", "")),
        str(user_profile.get("experience_years", "")),
        skills_text
    ])


def diversify_recommendations(
    user_skills,
    df,
    ranked_indices,
    scores,
    top_n=5,
    max_per_title=2,
    min_match_percentage=0
):
    recommendations = []
    seen_keys = set()
    title_count = {}

    user_skills = ensure_skill_set(user_skills)

    skip_reasons = {
        "duplicate_key": 0,
        "title_limit": 0,
        "empty_skills": 0,
        "low_match": 0
    }

    for idx in ranked_indices:
        row = df.iloc[idx]

        title = str(row["Job Title"]).strip()
        role = str(row["Role"]).strip()
        qualifications = str(row["Qualifications"]).strip()
        experience = str(row["Experience"]).strip()

        job_skills = ensure_skill_set(row["extracted_skills"])

        if len(job_skills) == 0:
            skip_reasons["empty_skills"] += 1
            continue

        matched = user_skills & job_skills
        missing = job_skills - user_skills

        skill_match = match_percentage(user_skills, job_skills)

        if skill_match < min_match_percentage:
            skip_reasons["low_match"] += 1
            continue

        dedup_key = (
            title.lower(),
            role.lower()
        )

        if dedup_key in seen_keys:
            skip_reasons["duplicate_key"] += 1
            continue

        if title_count.get(title.lower(), 0) >= max_per_title:
            skip_reasons["title_limit"] += 1
            continue

        seen_keys.add(dedup_key)
        title_count[title.lower()] = title_count.get(title.lower(), 0) + 1

        recommendations.append({
            "job_title": title,
            "role": role,
            "qualifications": qualifications,
            "experience": experience,

            "similarity_score": round(
                float(scores[idx]),
                4
            ),

            "match_percentage": skill_match,

            "matched_skills": sorted(list(matched)),

            "missing_skills": sorted(list(missing))[:10]
        })

        if len(recommendations) == top_n:
            break

    print("Skip reasons:", skip_reasons)
    print("Final recommendations:", len(recommendations))

    return recommendations


def recommend_jobs(
    user_profile,
    df,
    vectorizer,
    job_vectors,
    top_n=5,
    candidate_pool_size=300
):
    user_skills = ensure_skill_set(user_profile.get("skills", []))

    user_text = build_user_recommendation_text(user_profile)

    user_vector = vectorizer.transform([user_text])

    scores = cosine_similarity(user_vector, job_vectors).flatten()

    ranked_indices = scores.argsort()[::-1][:candidate_pool_size]

    recommendations = diversify_recommendations(
        user_skills=user_skills,
        df=df,
        ranked_indices=ranked_indices,
        scores=scores,
        top_n=top_n,
        max_per_title=2,
        min_match_percentage=0
    )

    return recommendations