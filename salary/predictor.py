import joblib
import os
import pandas as pd

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "salary_prediction_pipeline.pkl")
# model = joblib.load(MODEL_PATH)

def predict_salary(user_profile, model):

    input_df = pd.DataFrame([{
        "job_title": user_profile["job_title"],
        "education_level": user_profile["education_level"],
        "industry": user_profile["industry"],
        "company_size": user_profile["company_size"],
        "location": user_profile["location"],
        "remote_work": user_profile["remote_work"],
        "experience_years": user_profile["experience_years"],
        "skills_count": user_profile["skills_count"],
        "certifications": user_profile["certifications"]
    }])

    return model.predict(input_df)[0]