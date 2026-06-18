import re
from datetime import datetime


# can be improved using date or time duration based calculaiton of internship (or jobs)
def extract_explicit_experience(text: str):
    text = text.lower()

    patterns = [
        r"(\d+)\+?\s+years?\s+of\s+experience",
        r"(\d+)\+?\s+years?\s+experience",
        r"experience\s*[:\-]?\s*(\d+)\+?\s+years?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return None


def extract_experience(resume_text: str) -> dict:
    years = extract_explicit_experience(resume_text)

    if years is None:
        years = 0

    return {
        "experience_years": years
    }