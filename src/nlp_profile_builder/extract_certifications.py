import re


CERTIFICATION_KEYWORDS = [
    "certification",
    "certificate",
    "certified",
    "course",
    "specialization",
    "professional certificate",
    "nanodegree",
]


def extract_certifications(resume_text: str) -> dict:
    lines = resume_text.lower().splitlines()

    cert_lines = []

    for line in lines:
        if any(keyword in line for keyword in CERTIFICATION_KEYWORDS):
            cert_lines.append(line.strip())

    return {
        "certifications": len(cert_lines),
        "certification_items": cert_lines
    }