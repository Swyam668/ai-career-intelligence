import joblib
import os
import pandas as pd
import shap
import numpy as np
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "shap_background.csv"
)



def load_background_data():
    return pd.read_csv(BACKGROUND_PATH)


def create_salary_explainer(lr_pipeline):
    preprocessor = lr_pipeline.named_steps["preprocessor"]
    model = lr_pipeline.named_steps["model"]

    background_df = load_background_data()
    background_transformed = preprocessor.transform(background_df)

    explainer = shap.LinearExplainer(
        model,
        background_transformed
    )

    return explainer











BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_prediction_pipeline.pkl")
model = joblib.load(MODEL_PATH)

sample = pd.DataFrame([{
    "job_title": "Data Scientist",
    "education_level": "Bachelor",
    "industry": "Tech",
    "company_size": "Unknown",
    "location": "Unknown",
    "remote_work": "Unknown",
    "experience_years": 5,
    "skills_count": 8,
    "certifications": 2
}])

res = model.predict(sample)

print(res)


explainer = create_salary_explainer(model)

# SHAP test



def clean_feature_name(feature):
    """
    Removes ColumnTransformer prefixes if present.
    Example:
    cat__location_India -> location_India
    num__experience_years -> experience_years
    """
    if "__" in feature:
        return feature.split("__", 1)[1]
    return feature

def format_salary_explanation(shap_values, feature_names, input_df):
    values = shap_values.values[0]

    input_row = input_df.iloc[0].to_dict()

    active_features = set()

    # numeric features
    numeric_features = [
        "experience_years",
        "skills_count",
        "certifications"
    ]

    for feature in numeric_features:
        active_features.add(feature)

    # categorical active one-hot features
    categorical_features = [
        "job_title",
        "education_level",
        "industry",
        "company_size",
        "location",
        "remote_work"
    ]

    for col in categorical_features:
        value = input_row[col]
        active_features.add(f"{col}_{value}")

    explanation = []

    for feature, impact in zip(feature_names, values):
        feature = clean_feature_name(feature)

        if feature not in active_features:
            continue

        explanation.append({
            "feature": feature,
            "impact": round(float(impact), 2),
            "effect": "positive" if impact > 0 else "negative"
        })

    explanation = sorted(
        explanation,
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    return explanation












# def get_feature_names(preprocessor):
#     cat_features = preprocessor.named_transformers_["cat"].get_feature_names_out()
#     num_features = preprocessor.transformers_[1][2]

#     return list(cat_features) + list(num_features)


def explain_salary_prediction(lr_pipeline, explainer, input_df):
    """
    Explains one salary prediction using SHAP.

    Args:
        lr_pipeline: trained salary prediction pipeline
        input_df: single-row dataframe used for prediction
        background_df: X_train or sample of X_train

    Returns:
        dict with prediction and SHAP explanation
    """

    preprocessor = lr_pipeline.named_steps["preprocessor"]

    input_transformed = preprocessor.transform(input_df)

    shap_values = explainer(input_transformed)

    feature_names = preprocessor.get_feature_names_out()

    explanation = format_salary_explanation(
        shap_values,
        feature_names,
        input_df
    )

    prediction = lr_pipeline.predict(input_df)[0]

    return {
        "predicted_salary": round(float(prediction), 2),
        "base_salary": round(float(shap_values.base_values[0]), 2),
        "explanation": explanation
    }


explanation = explain_salary_prediction(model, explainer, sample)
print(explanation)