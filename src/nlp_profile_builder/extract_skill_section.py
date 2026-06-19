# skill section extraction from resume
SECTION_HEADERS = [
    "skills",
    "technical skills",
    "core competencies",
    "technologies",
    "tools"
]

def extract_skills_section(text):
    text_lower = text.lower()

    for header in SECTION_HEADERS:

        idx = text_lower.find(header)

        if idx != -1:
            return text[idx:idx+1000]

    return ""

def extract_candidates(resume_text):
    skills_section = extract_skills_section(
        resume_text
    )

    import re

    candidates = re.split(
        r"[,|\n|•]",
        skills_section
    )

    # cleaning
    candidates = [
        c.strip()
        for c in candidates
        if len(c.strip()) > 1
    ]

    return candidates
