from resume_parser.parser import build_user_profile
from salary.predictor import predict_salary
from recommendation.recommender import recommend_jobs


def run_pipeline(resume_text, df, vectorizer, job_vectors, model):

    user_profile = build_user_profile(resume_text)

    # salary = predict_salary(user_profile, model)

    recommendations = recommend_jobs(
        user_profile,
        df,
        vectorizer,
        job_vectors
    )

    user_profile["skills"] = list(user_profile["skills"])

    return {
        "profile": user_profile,
        # "predicted_salary": salary,
        "recommendations": recommendations,
        # "scores": scores
    }