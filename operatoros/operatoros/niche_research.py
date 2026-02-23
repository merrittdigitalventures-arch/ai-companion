import random

# Revenue-first mock niche database (beta-safe)
NICHES = [
    {"niche": "AI Prompt Packs", "base_revenue": 92},
    {"niche": "Local Lead Gen (Roofing)", "base_revenue": 88},
    {"niche": "Fitness Digital Programs", "base_revenue": 84},
    {"niche": "E-commerce Automation", "base_revenue": 90},
    {"niche": "Real Estate Investing", "base_revenue": 86},
    {"niche": "Online Course Creators", "base_revenue": 83},
    {"niche": "Small Business Marketing", "base_revenue": 87},
    {"niche": "Crypto Education", "base_revenue": 79},
    {"niche": "Personal Finance Tools", "base_revenue": 85},
    {"niche": "Career Resume Services", "base_revenue": 82},
]


def get_top_5_niches():
    """
    Returns the top 5 niches ranked by simulated revenue potential.
    Each run introduces slight variance to mimic market movement.
    """

    scored = []

    for item in NICHES:
        # Add small randomness to simulate market fluctuation
        variance = random.randint(-5, 5)
        revenue_score = max(50, item["base_revenue"] + variance)

        scored.append({
            "niche": item["niche"],
            "revenue_score": revenue_score
        })

    # Sort by revenue score descending
    scored.sort(key=lambda x: x["revenue_score"], reverse=True)

    return scored[:5]
