INDUSTRY_KEYWORDS = {
    "Tech": [
        "software",
        "web development",
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "python",
        "java",
        "react",
        "cloud",
        "aws",
        "docker",
        "kubernetes"
    ],

    "Finance": [
        "banking",
        "financial",
        "investment",
        "fintech",
        "trading",
        "risk analysis",
        "accounting"
    ],

    "Healthcare": [
        "hospital",
        "medical",
        "healthcare",
        "clinical",
        "patient",
        "diagnosis"
    ],

    "Education": [
        "teaching",
        "education",
        "curriculum",
        "student",
        "learning"
    ],

    "Retail": [
        "retail",
        "ecommerce",
        "customer service",
        "inventory"
    ],

    "Manufacturing": [
        "production",
        "manufacturing",
        "supply chain",
        "quality control"
    ],

    "Marketing": [
        "seo",
        "marketing",
        "social media",
        "advertising",
        "branding"
    ],

    "Consulting": [
        "consulting",
        "business analysis",
        "strategy"
    ],

    "Telecom": [
        "telecommunications",
        "networking",
        "5g",
        "wireless"
    ],

    "Government": [
        "government",
        "public sector",
        "policy"
    ]
}

def extract_industry(text):
    text = text.lower()

    scores = {}

    for industry, keywords in INDUSTRY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        scores[industry] = score

    best_industry = max(scores, key=scores.get)

    return best_industry if scores[best_industry] > 0 else "Tech"