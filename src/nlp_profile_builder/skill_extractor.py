
class SkillExtractor:
    def __init__(self, model, skill_database, threshold=0.60):
        self.model = model
        self.skill_database = skill_database
        self.threshold = threshold
        self.skill_embeddings = self.model.encode(
            self.skill_database,
            convert_to_tensor=True
        )

    def normalize_skill(self, candidate):
        from sentence_transformers.util import cos_sim

        candidate = candidate.strip().lower()

        abbreviation_map = {
            "ml": "machine learning",
            "dl": "deep learning",
            "nlp": "natural language processing",
            "cv": "computer vision",
            "llm": "large language models",
        }

        if candidate in abbreviation_map:
            return abbreviation_map[candidate]

        candidate_embedding = self.model.encode(
            candidate,
            convert_to_tensor=True
        )

        similarities = cos_sim(
            candidate_embedding,
            self.skill_embeddings
        )[0]

        best_idx = similarities.argmax().item()
        best_score = similarities[best_idx].item()

        if best_score >= self.threshold:
            return self.skill_database[best_idx]

        return None

    def extract(self, candidates):
        skills = set()

        for candidate in candidates:
            skill = self.normalize_skill(candidate)

            if skill:
                skills.add(skill.lower())

        return sorted(skills)