#!/bin/bash
# operatoros_one_command.sh — full OperatorOS beta runner

# Activate venv
source ./venv/bin/activate

# Step 1: Run API setup
echo "=== OperatorOS API Setup ==="
python operatoros/api_setup.py

# Step 2: Run live niche scoring using APIs
echo "=== Scoring Niches via API Fetcher ==="
python -c "
from operatoros.api_fetcher import APIFetcher
from operatoros.niche_research import save_top_niches

fetcher = APIFetcher()
trends = fetcher.fetch_trends()
financials = fetcher.fetch_financials()
scored = fetcher.score_niches(financials)
save_top_niches(scored)
print('Top niches scored and saved.')
"

# Step 3: Launch main GUI
echo "=== Launching OperatorOS GUI ==="
python -m operatoros.main

# Step 4: Create daily ZIP backup
echo "=== Saving Daily ZIP ==="
python -c "
import shutil, datetime
zip_name = f'daily_zips/operatoros_{datetime.date.today()}.zip'
shutil.make_archive(zip_name.replace('.zip',''), 'zip', 'operatoros')
print(f'Daily ZIP saved: {zip_name}')
"
