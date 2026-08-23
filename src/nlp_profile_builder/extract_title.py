from sentence_transformers import util


KNOWN_ROLES = [
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Analyst",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Software Engineer",
    "DevOps Engineer",
    "Cloud Engineer",
    "Business Analyst",
    "Product Manager",
]


def extract_title(resume_text: str, model, known_roles=None) -> dict:
    """
    Extract the most likely target job title from resume text
    """

    if known_roles is None:
        known_roles = KNOWN_ROLES

    if not resume_text or not resume_text.strip():
        return {
            "job_title": "Unknown",
            "confidence": 0.0
        }

    role_embeddings = model.encode(
        known_roles,
        convert_to_tensor=True
    )

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    scores = util.cos_sim(resume_embedding, role_embeddings)[0]

    # tensor to python item
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    return {
        "job_title": known_roles[best_idx],
        "confidence": round(best_score, 4)
    }