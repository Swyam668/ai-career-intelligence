# ml/salary_explainer.py

import os
import pandas as pd
import shap


SALARY_FEATURES = [
    "job_title",
    "experience_years",
    "education_level",
    "skills_count",
    "industry",
    "company_size",
    "location",
    "remote_work",
    "certifications",
]


def prepare_salary_input(user_profile):
    salary_input = {
        "job_title": user_profile.get("job_title", "Data Scientist"),
        "experience_years": user_profile.get("experience_years", 0),
        "education_level": user_profile.get("education_level", "Bachelor"),
        "skills_count": user_profile.get("skills_count", 0),
        "industry": user_profile.get("industry", "Tech"),
        "company_size": user_profile.get("company_size", "Medium"),
        "location": user_profile.get("location", "India"),
        "remote_work": user_profile.get("remote_work", "No"),
        "certifications": user_profile.get("certifications", 0),
    }

    return pd.DataFrame([salary_input], columns=SALARY_FEATURES)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "shap_background.csv"
)


def load_background_data():
    return pd.read_csv(BACKGROUND_PATH)

# for app.py


# to safely handle sparse matrix
# def to_dense(matrix):
#     if hasattr(matrix, "toarray"):
#         return matrix.toarray()
#     return matrix


def create_salary_explainer(lr_pipeline):
    preprocessor = lr_pipeline.named_steps["preprocessor"]
    model = lr_pipeline.named_steps["model"]

    background_df = load_background_data()
    background_transformed = preprocessor.transform(background_df)

    masker = shap.maskers.Independent(
        background_transformed,
        max_samples=100
    )

    explainer = shap.LinearExplainer(
        model,
        masker
    )

    return explainer


# for inference.py
def clean_feature_name(feature):
    """
    Removes ColumnTransformer prefixes if present.
    Example:
    cat__location_India - location_India
    num__experience_years - experience_years
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






##################### HUMANIZE THE FORMAT ########################
def humanize_feature_label(feature):
    """
    Converts raw SHAP feature names into readable labels.

    Examples:
    location_India -> Location: India
    job_title_Machine Learning Engineer -> Job Title: Machine Learning Engineer
    experience_years -> Experience
    skills_count -> Skills Count
    certifications -> Certifications
    """

    direct_labels = {
        "experience_years": "Experience",
        "skills_count": "Skills Count",
        "certifications": "Certifications",
    }

    if feature in direct_labels:
        return direct_labels[feature]

    known_prefixes = {
        "job_title_": "Job Title",
        "education_level_": "Education Level",
        "industry_": "Industry",
        "company_size_": "Company Size",
        "location_": "Location",
        "remote_work_": "Remote Work",
    }

    for prefix, label in known_prefixes.items():
        if feature.startswith(prefix):
            value = feature.replace(prefix, "", 1)
            return f"{label}: {value}"

    return feature.replace("_", " ").title()



def humanize_impact_message(feature, impact):
    """
    Converts SHAP impact into a readable sentence.
    """

    amount = abs(round(float(impact)))

    if impact > 0:
        direction = "Increased"
    else:
        direction = "Lowered"

    if feature == "experience_years":
        return f"{direction} the estimate by ₹{amount:,} based on experience level"

    if feature == "skills_count":
        return f"{direction} the estimate by ₹{amount:,} based on number of skills"

    if feature == "certifications":
        return f"{direction} the estimate by ₹{amount:,} based on certifications"

    if feature.startswith("location_"):
        return f"{direction} the estimate by ₹{amount:,} based on location"

    if feature.startswith("job_title_"):
        return f"{direction} the estimate by ₹{amount:,} based on target job role"

    if feature.startswith("education_level_"):
        return f"{direction} the estimate by ₹{amount:,} based on education level"

    if feature.startswith("company_size_"):
        return f"{direction} the estimate by ₹{amount:,} based on company size"

    if feature.startswith("remote_work_"):
        return f"{direction} the estimate by ₹{amount:,} based on remote work preference"

    if feature.startswith("industry_"):
        return f"{direction} the estimate by ₹{amount:,} based on industry"

    return f"{direction} the estimate by ₹{amount:,}"


def humanize_salary_explanation(explanation):
    """
    Converts raw SHAP explanation list into frontend-friendly explanation list.
    """

    humanized = []

    for item in explanation:
        feature = item["feature"]
        impact = item["impact"]
        effect = item["effect"]

        humanized.append({
            "feature": feature,
            "title": humanize_feature_label(feature),
            "message": humanize_impact_message(feature, impact),
            "impact": impact,
            "effect": effect
        })

    return humanized










def explain_salary_prediction(lr_pipeline, explainer, input_df):
    """
    Explains one salary prediction using SHAP.

    Args:
        lr_pipeline: trained salary prediction pipeline
        input_df: single-row dataframe used for prediction

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

    humanized_explanation = humanize_salary_explanation(explanation)

    return {
        "predicted_salary": round(float(prediction), 2),
        "base_salary": round(float(shap_values.base_values[0]), 2),
        "explanation": humanized_explanation,
        # for debugging
        "raw_explanation": explanation
    }