from operatoros.api_fetcher import APIFetcher

def get_scored_niches(mock=False):
    fetcher = APIFetcher()
    trends = fetcher.fetch_trends()
    financials = fetcher.fetch_financials()

    # Merge trend names with financial data
    niches = []
    for trend in trends:
        for fin in financials:
            if trend['name'] == fin['name']:
                niche = {"name": trend['name'], "revenue": fin['revenue']}
                niches.append(niche)
                break
        else:
            niches.append({"name": trend['name'], "revenue": 0})

    # Score niches
    scored = fetcher.score_niches(niches, mock=mock)
    return scored

def save_top_niches(scored_niches, path="data/top_niches.json"):
    import json
    with open(path, "w") as f:
        json.dump(scored_niches, f, indent=2)
