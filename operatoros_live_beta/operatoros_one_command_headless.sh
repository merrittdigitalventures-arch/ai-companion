#!/bin/bash
echo "=== OperatorOS Headless Runner ==="

# Activate virtual environment
source ./venv/bin/activate

# --- Step 1: API Setup (only prompts if missing) ---
echo "--- Checking API Keys ---"
python - << 'PYTHON_EOF'
import os
from operatoros.api_setup import ensure_api_keys

ensure_api_keys()  # will only prompt if keys are missing
PYTHON_EOF

# --- Step 2: Score Niches ---
echo "=== Scoring Niches via API Fetcher ==="
python - << 'PYTHON_EOF'
from operatoros.api_fetcher import APIFetcher
from operatoros.state import get_current_niche, set_current_niche

fetcher = APIFetcher()

# Fetch and score niches
niches = fetcher.fetch_trends()
niches = fetcher.score_niches(niches, mock=True)

# Save top niche automatically if none selected
top_niches = sorted(niches, key=lambda n: n.get("score", 0), reverse=True)
current = get_current_niche()
if not current:
    set_current_niche(top_niches[0])
    print(f"Auto-selected top niche: {top_niches[0]['name']}")
else:
    print(f"Using previously selected niche: {current['name']}")
PYTHON_EOF

# --- Step 3: Launch GUI with auto-selected niche ---
python - << 'PYTHON_EOF'
from operatoros.gui import launch_gui
from operatoros.state import get_current_niche

niche = get_current_niche()
launch_gui([niche])  # only loads the current niche
PYTHON_EOF

# --- Step 4: Save Daily ZIP ---
echo "=== Saving Daily ZIP ==="
zip -r -q daily_zips/operatoros_$(date +%Y-%m-%d).zip operatoros data

echo "OperatorOS headless run complete."
