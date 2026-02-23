import random
from datetime import datetime


ASSET_TEMPLATES = {
    "ebook": [
        "The Complete Guide to {niche}",
        "{niche}: A Practical Playbook",
        "How to Win in {niche}"
    ],
    "workbook": [
        "{niche} Action Workbook",
        "Hands-On {niche} Implementation Guide"
    ],
    "checklist": [
        "{niche} Launch Checklist",
        "{niche} Daily Execution Checklist"
    ],
    "prompt_pack": [
        "{niche} AI Prompt Pack",
        "High-Converting {niche} Prompt Library"
    ]
}


def generate_bundle(chosen: dict):
    """
    Generates a diversified asset bundle for the selected niche.
    Returns a dict of asset_type -> title.
    """

    niche = chosen["niche"]
    random.seed(f"{niche}-{datetime.utcnow().date()}")

    bundle = {}

    for asset_type, templates in ASSET_TEMPLATES.items():
        title_template = random.choice(templates)
        title = title_template.format(niche=niche)
        bundle[asset_type] = title

    return bundle
