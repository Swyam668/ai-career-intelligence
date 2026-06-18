import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_prediction_pipeline.pkl")
model = joblib.load(MODEL_PATH)


sample = pd.DataFrame([{
    "job_title": "Data Scientist",
    "education_level": "Master",
    "industry": "Tech",
    "company_size": "Large",
    "location": "Delhi",
    "remote_work": "Yes",
    "experience_years": 5,
    "skills_count": 8,
    "certifications": 2
}])

res = model.predict(sample)

print(res)