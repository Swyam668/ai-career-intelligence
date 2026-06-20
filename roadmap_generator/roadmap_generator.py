def get_top_recommendation(recommendations):
    if not recommendations:
        return None

    return recommendations[0]


def normalize_skills(skills):
    if not skills:
        return []

    return sorted({
        str(skill).lower().strip()
        for skill in skills
        if str(skill).strip()
    })


ROLE_SKILL_PRIORITY = {
    "machine learning engineer": [
        "python",
        "machine learning",
        "scikit-learn",
        "xgboost",
        "deep learning",
        "tensorflow",
        "pytorch",
        "model evaluation",
        "feature engineering",
        "fastapi",
        "docker",
        "aws"
    ],

    "data scientist": [
        "python",
        "statistics",
        "sql",
        "pandas",
        "numpy",
        "machine learning",
        "scikit-learn",
        "xgboost",
        "data visualization",
        "shap"
    ],

    "ai engineer": [
        "python",
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "transformers",
        "nlp",
        "llm",
        "rag",
        "fastapi",
        "docker"
    ],

    "nlp engineer": [
        "python",
        "nlp",
        "natural language processing",
        "transformers",
        "sentence transformers",
        "bert",
        "llm",
        "rag",
        "pytorch",
        "fastapi"
    ],

    "data analyst": [
        "sql",
        "excel",
        "python",
        "pandas",
        "numpy",
        "statistics",
        "power bi",
        "tableau",
        "data visualization"
    ],

    "backend developer": [
        "python",
        "java",
        "node.js",
        "fastapi",
        "django",
        "flask",
        "sql",
        "mongodb",
        "docker",
        "aws"
    ],

    "full stack developer": [
        "javascript",
        "typescript",
        "react",
        "next.js",
        "node.js",
        "express.js",
        "mongodb",
        "sql",
        "tailwind css",
        "docker"
    ]
}


SKILL_PHASE_MAP = {
    "ml_foundations": {
        "title": "Phase 1: Strengthen ML Foundations",
        "duration": "1-2 weeks",
        "focus": "Build stronger machine learning fundamentals and improve model evaluation skills.",
        "skills": [
            "machine learning",
            "scikit-learn",
            "xgboost",
            "model evaluation",
            "feature engineering",
            "statistics"
        ],
        "action_items": [
            "Build one tabular ML project using scikit-learn or XGBoost.",
            "Compare multiple models using MAE, RMSE, R2 score, precision, recall, and F1 score where relevant.",
            "Document preprocessing, feature engineering, model selection, and evaluation clearly."
        ]
    },

    "deep_learning": {
        "title": "Phase 2: Learn Deep Learning",
        "duration": "2-3 weeks",
        "focus": "Develop neural network and deep learning skills for AI-focused roles.",
        "skills": [
            "deep learning",
            "tensorflow",
            "pytorch",
            "neural networks"
        ],
        "action_items": [
            "Train a basic neural network using TensorFlow or PyTorch.",
            "Understand forward propagation, loss functions, backpropagation, and optimizers.",
            "Build a small image, text, or tabular deep learning experiment."
        ]
    },

    "nlp": {
        "title": "Phase 3: Applied NLP and Transformers",
        "duration": "2-3 weeks",
        "focus": "Learn transformer-based NLP and semantic search techniques.",
        "skills": [
            "nlp",
            "natural language processing",
            "transformers",
            "sentence transformers",
            "bert",
            "llm",
            "rag"
        ],
        "action_items": [
            "Build a semantic search or resume-job matching system using Sentence Transformers.",
            "Use embeddings and cosine similarity to compare text meaningfully.",
            "Experiment with transformer-based models for classification, retrieval, or recommendation."
        ]
    },

    "deployment": {
        "title": "Phase 4: Deployment and MLOps Basics",
        "duration": "1-2 weeks",
        "focus": "Deploy ML models as usable backend services.",
        "skills": [
            "fastapi",
            "flask",
            "docker",
            "aws",
            "render",
            "vercel"
        ],
        "action_items": [
            "Expose one ML model through a FastAPI endpoint.",
            "Dockerize the backend application.",
            "Deploy the frontend and backend so users can interact with the ML system."
        ]
    },

    "data_analysis": {
        "title": "Phase 1: Data Analysis and Visualization",
        "duration": "1-2 weeks",
        "focus": "Improve data cleaning, analysis, and visualization skills.",
        "skills": [
            "sql",
            "pandas",
            "numpy",
            "excel",
            "power bi",
            "tableau",
            "data visualization"
        ],
        "action_items": [
            "Analyze a real dataset using pandas and SQL.",
            "Create visual insights using charts or a BI dashboard.",
            "Write clear observations and business conclusions from the analysis."
        ]
    },

    "web_development": {
        "title": "Phase 2: Web Application Development",
        "duration": "2-3 weeks",
        "focus": "Strengthen frontend and backend development for production-ready applications.",
        "skills": [
            "react",
            "next.js",
            "node.js",
            "express.js",
            "mongodb",
            "sql",
            "tailwind css"
        ],
        "action_items": [
            "Build a clean dashboard using Next.js or React.",
            "Create backend APIs for user-facing features.",
            "Connect frontend, backend, and database into one complete app."
        ]
    }
}


def build_roadmap_context(user_profile, recommendations):
    top_recommendation = get_top_recommendation(recommendations)

    if not top_recommendation:
        return {
            "target_role": user_profile.get("job_title", "Unknown"),
            "readiness_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "user_skills": normalize_skills(user_profile.get("skills", []))
        }

    target_role = (
        top_recommendation.get("role")
        or top_recommendation.get("job_title")
        or user_profile.get("job_title")
        or "Unknown"
    )

    return {
        "target_role": target_role,
        "readiness_score": top_recommendation.get("match_percentage", 0),
        "matched_skills": normalize_skills(top_recommendation.get("matched_skills", [])),
        "missing_skills": normalize_skills(top_recommendation.get("missing_skills", [])),
        "user_skills": normalize_skills(user_profile.get("skills", []))
    }


def prioritize_missing_skills(target_role, missing_skills):
    target_role_key = str(target_role).lower().strip()

    priority_list = ROLE_SKILL_PRIORITY.get(target_role_key, [])

    priority_skills = []

    for skill in priority_list:
        if skill in missing_skills:
            priority_skills.append(skill)

    for skill in missing_skills:
        if skill not in priority_skills:
            priority_skills.append(skill)

    return priority_skills[:8]


def detect_needed_phases(priority_skills):
    needed_phases = []

    for phase_key, phase_data in SKILL_PHASE_MAP.items():
        phase_skills = set(phase_data["skills"])

        if phase_skills & set(priority_skills):
            needed_phases.append(phase_key)

    return needed_phases


def build_phase(phase_key, priority_skills):
    phase_data = SKILL_PHASE_MAP[phase_key]

    relevant_skills = [
        skill for skill in priority_skills
        if skill in phase_data["skills"]
    ]

    if not relevant_skills:
        relevant_skills = phase_data["skills"][:3]

    return {
        "phase": phase_data["title"],
        "duration": phase_data["duration"],
        "focus": phase_data["focus"],
        "skills": relevant_skills,
        "action_items": phase_data["action_items"]
    }


def generate_project_suggestions(target_role, priority_skills):
    target_role_key = str(target_role).lower()

    suggestions = []

    if "xgboost" in priority_skills or "machine learning" in priority_skills:
        suggestions.append(
            "Build an XGBoost-based prediction project with feature engineering and SHAP explanations."
        )

    if "nlp" in priority_skills or "sentence transformers" in priority_skills or "transformers" in priority_skills:
        suggestions.append(
            "Build a semantic search or recommendation system using Sentence Transformers."
        )

    if "docker" in priority_skills or "fastapi" in priority_skills or "aws" in priority_skills:
        suggestions.append(
            "Deploy a FastAPI ML backend with Docker and connect it to a frontend dashboard."
        )

    if "data scientist" in target_role_key:
        suggestions.append(
            "Create an end-to-end data science case study with EDA, modeling, evaluation, and business insights."
        )

    if "full stack" in target_role_key or "backend" in target_role_key:
        suggestions.append(
            "Build a full-stack app with authentication, APIs, database integration, and deployment."
        )

    if not suggestions:
        suggestions.append(
            "Build one role-specific portfolio project using your missing skills and document it clearly."
        )

    return suggestions[:4]


def estimate_timeline(roadmap):
    total_weeks = 0

    for phase in roadmap:
        duration = phase["duration"]

        if "1-2" in duration:
            total_weeks += 2
        elif "2-3" in duration:
            total_weeks += 3
        else:
            total_weeks += 2

    return f"{max(total_weeks - 1, 1)}-{total_weeks} weeks"


def generate_rule_based_roadmap(context):
    target_role = context["target_role"]
    priority_skills = prioritize_missing_skills(
        target_role=target_role,
        missing_skills=context["missing_skills"]
    )

    needed_phases = detect_needed_phases(priority_skills)

    if not needed_phases:
        needed_phases = ["ml_foundations", "deployment"]

    roadmap = []

    for phase_key in needed_phases[:4]:
        roadmap.append(
            build_phase(
                phase_key=phase_key,
                priority_skills=priority_skills
            )
        )

    return {
        "target_role": target_role,
        "readiness_score": context["readiness_score"],
        "current_strengths": context["matched_skills"][:8],
        "priority_skills": priority_skills,
        "estimated_timeline": estimate_timeline(roadmap),
        "roadmap": roadmap,
        "project_suggestions": generate_project_suggestions(
            target_role=target_role,
            priority_skills=priority_skills
        )
    }


def generate_career_roadmap(user_profile, recommendations, mode="rule_based"):
    context = build_roadmap_context(
        user_profile=user_profile,
        recommendations=recommendations
    )

    if mode == "rule_based":
        return generate_rule_based_roadmap(context)

    raise ValueError(f"Unsupported roadmap generation mode: {mode}")