import re


EDUCATION_PATTERNS = [
    ("PhD", [
        r"\bph\.?d\b",
        r"\bdoctorate\b",
    ]),

    ("Master", [
        r"\bmaster'?s?\b",
        r"\bm\.?\s?tech\b",
        r"\bmtech\b",
        r"\bm\.?\s?s\.?\b",
        r"\bmba\b",
        r"\bmca\b",
    ]),

    ("Bachelor", [
        r"\bbachelor'?s?\b",
        r"\bb\.?\s?tech\b",
        r"\bbtech\b",
        r"\bb\.?\s?e\.?\b",
        r"\bb\.?\s?sc\b",
        r"\bbsc\b",
        r"\bbca\b",
    ]),

    ("Diploma", [
        r"\bdiploma\b",
    ]),

    ("High School", [
        r"\bhigh school\b",
        r"\b12th\b",
        r"\bsenior secondary\b",
    ]),
]


def extract_education(resume_text: str) -> dict:
    text = resume_text.lower()

    for level, patterns in EDUCATION_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text):
                return {
                    "education_level": level
                }

    return {
        "education_level": "Bachelor"
    }