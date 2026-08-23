from resume_parser.parser import build_user_profile
from salary.predictor import predict_salary
from recommendation.recommender import recommend_jobs
from salary.shap_explainer import prepare_salary_input

def run_pipeline(resume_text, df, vectorizer, job_vectors, salary_model, nlp_model, salary_explainer, explain_salary_prediction):


    user_profile = build_user_profile(resume_text, nlp_model)

    # removed because SHAP explainer already has this
    # salary = predict_salary(user_profile, salary_model)

    # explainer (ultimately SHAP) need pandas dataframe rather than dictionary
    salary_input_df = prepare_salary_input(user_profile)
    salary_explanation = explain_salary_prediction(
        salary_model,
        salary_explainer,
        salary_input_df
    )
    
    recommendations = recommend_jobs(
        user_profile,
        df,
        vectorizer,
        job_vectors
    )
    
    # career_roadmap = generate_career_roadmap(
    #     user_profile=user_profile,
    #     recommendations=recommendations,
    #     mode="llm"
    # )

    # to make it compatible with json formatting
    user_profile["skills"] = list(user_profile["skills"])

    return {
        "profile": user_profile,
        # "predicted_salary": salary_explanation["predicted_salary"],
        "recommendations": recommendations,
        # "base_salary": salary_explanation["base_salary"],
        # "explanation": salary_explanation["explanation"]
        "salary": salary_explanation,
        # "career_roadmap": career_roadmap
        # "scores": scores
    }