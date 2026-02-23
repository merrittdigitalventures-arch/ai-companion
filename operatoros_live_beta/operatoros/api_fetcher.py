import requests
import os
from operatoros.logger import log_run

class APIFetcher:
    def __init__(self):
        self.twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.stripe_key = os.getenv("STRIPE_API_KEY")
        self.gumroad_token = os.getenv("GUMROAD_ACCESS_TOKEN")
        self.shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.paypal_token = os.getenv("PAYPAL_API_KEY")

    # --- Twitter Trends ---
    def fetch_trends(self):
        if not self.twitter_token:
            log_run("Twitter token missing, returning mock trends.")
            return [{"name": "AI Prompt Packs"}, {"name": "Local Lead Gen"}]
        headers = {"Authorization": f"Bearer {self.twitter_token}"}
        url = "https://api.twitter.com/2/tweets/search/recent?query=%23trending&max_results=10"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            trends = [{"name": t.get("text","Unknown Trend")[:50]} for t in data.get("data",[])]
            return trends if trends else [{"name": "AI Prompt Packs"}, {"name": "Local Lead Gen"}]
        except Exception as e:
            log_run(f"Twitter API fetch error: {e}")
            return [{"name": "AI Prompt Packs"}, {"name": "Local Lead Gen"}]

    # --- Financials ---
    def fetch_financials(self):
        result = []
        if self.stripe_key:
            headers = {"Authorization": f"Bearer {self.stripe_key}"}
            try:
                r = requests.get("https://api.stripe.com/v1/products", headers=headers, timeout=10)
                products = r.json().get("data",[])
                for p in products:
                    result.append({"name": p.get("name"), "revenue": int(p.get("metadata",{}).get("revenue",0))})
            except Exception as e:
                log_run(f"Stripe API fetch error: {e}")
        if self.gumroad_token:
            try:
                r = requests.get(f"https://api.gumroad.com/v2/products?access_token={self.gumroad_token}", timeout=10)
                products = r.json().get("products",[])
                for p in products:
                    result.append({"name": p.get("name"), "revenue": int(p.get("sales_count",0)*p.get("price_cents",0)/100)})
            except Exception as e:
                log_run(f"Gumroad API fetch error: {e}")
        if not result:
            result = [{"name": "AI Prompt Packs", "revenue": 1000}, {"name": "Local Lead Gen", "revenue": 800}]
        return result

    # --- Scoring ---
    def score_niches(self, niche_list, mock=False):
        if mock:
            for niche in niche_list:
                niche["score"] = 50
            return niche_list
        financials = {f["name"]: f["revenue"] for f in self.fetch_financials()}
        for niche in niche_list:
            niche["score"] = financials.get(niche["name"], 0)
        return niche_list
