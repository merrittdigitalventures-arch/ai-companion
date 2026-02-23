def summarize_run(day: int, niche: dict, bundle: dict):
    """
    Produces a revenue-focused summary of the day's execution.
    """

    estimated_value_per_asset = 25  # conservative beta estimate
    asset_count = len(bundle)
    daily_estimated_value = asset_count * estimated_value_per_asset

    summary = {
        "day": day,
        "niche": niche["niche"],
        "revenue_score": niche["revenue_score"],
        "assets_created": list(bundle.values()),
        "asset_count": asset_count,
        "estimated_daily_value": daily_estimated_value
    }

    print("\n=== DAILY SUMMARY ===")
    print(f"Day: {day}")
    print(f"Niche: {niche['niche']}")
    print(f"Revenue Score: {niche['revenue_score']}")
    print(f"Assets Created: {asset_count}")
    print(f"Estimated Daily Value: ${daily_estimated_value}")
    print("=====================\n")

    return summary
