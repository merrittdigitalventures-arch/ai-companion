#!/bin/bash
# operatoros_one_command.sh — Fully automated OperatorOS runner

set -e

echo "Starting OperatorOS one-command runner..."

# Step 0: Create virtual environment if missing
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Step 1: Activate venv
source venv/bin/activate

# Step 2: Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Run OperatorOS
python -m operatoros.main

# Step 4: Auto-export ZIP
python - <<END
from operatoros.gui import export_daily_zip
zip_file = export_daily_zip()
print(f"Daily ZIP saved to: {zip_file}")
END

echo "OperatorOS run complete."
