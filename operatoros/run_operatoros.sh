#!/data/data/com.termux/files/usr/bin/bash

# Activate virtual environment
source ~/operatoros/venv/bin/activate

# Run OperatorOS for today
python -m operatoros.main

# Zip today's bundle for easy sharing
TODAY=$(date +%Y-%m-%d)
ZIP_DIR=~/operatoros/daily_zips
mkdir -p $ZIP_DIR
zip -r $ZIP_DIR/operatoros_$TODAY.zip ~/operatoros/data/*

echo "Daily ZIP saved to $ZIP_DIR/operatoros_$TODAY.zip"
