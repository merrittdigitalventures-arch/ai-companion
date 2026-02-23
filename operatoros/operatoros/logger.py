import json
import os
from datetime import datetime


LOG_FILE = "data/run_log.json"


def log_run(summary: dict, state: dict):
    """
    Appends the daily run summary to a persistent log.
    """

    if not os.path.exists("data"):
        os.makedirs("data")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "day": summary["day"],
        "niche": summary["niche"],
        "asset_count": summary["asset_count"],
        "estimated_value": summary["estimated_daily_value"]
    }

    # Load existing log
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    # Also store in state history for quick reference
    state.setdefault("history", []).append(log_entry)
