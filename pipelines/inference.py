from resume_parser.parser import build_user_profile
from salary.predictor import predict_salary
from recommendation.recommender import recommend_jobs


def run_pipeline(resume_text, df, vectorizer, job_vectors, salary_model, nlp_model):


    user_profile = build_user_profile(resume_text, nlp_model)

    salary = predict_salary(user_profile, salary_model)

    recommendations = recommend_jobs(
        user_profile,
        df,
        vectorizer,
        job_vectors
    )

    # to make it compatible with json formatting
    user_profile["skills"] = list(user_profile["skills"])

    return {
        "profile": user_profile,
        "predicted_salary": salary,
        "recommendations": recommendations,
        # "scores": scores
    }