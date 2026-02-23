import re

def scrape_market_insights(raw_text):
    # Looking for 'I wish', 'finally', 'problem'
    patterns = [r"finally.*", r"wish I had.*", r"better than.*"]
    findings = []
    
    for pattern in patterns:
        matches = re.findall(pattern, raw_text, re.IGNORECASE)
        findings.extend(matches)
    
    return findings

# Simulating raw text from a forum or competitor page
market_chatter = """
I've used Tool X, but I wish I had more automation. 
Finally found a way to save time on my emails!
This is better than anything else I've tried.
"""

print("[*] GENIE SCRAPER: EXTRACTING MARKET GAPS")
insights = scrape_market_insights(market_chatter)
for i in insights:
    print(f"Potential Hook: {i.strip()}")
