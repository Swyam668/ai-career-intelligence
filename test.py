import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_prediction_pipeline.pkl")
model = joblib.load(MODEL_PATH)

print(model.named_steps["preprocessor"].get_feature_names_out())