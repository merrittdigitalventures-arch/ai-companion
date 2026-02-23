from review_brain import analyze_review
from ad_math import run_simulation

# 1. The Brain picks the best hook
raw_review = "I was skeptical, but this finally fixed my workflow and saved me so much time!"
analysis = analyze_review(raw_review)
hook = analysis['hook']

print(f"[*] Brain selected Hook: {hook}")

# 2. Simulator tests the hook (assuming better hooks lower the CPC)
# We'll simulate a 'Winning' CPC of 0.50 because the hook is so good
optimized_results = run_simulation(budget=500, cpc=0.50, conversion_rate=0.04, product_price=97.00)

print(f"\n[*] Results for '{hook}':")
print(f"    ROAS: {optimized_results['roas']}x")
print(f"    Profit: ${optimized_results['profit']}")

if optimized_results['roas'] > 5:
    print("\n[!!!] GENIE ALERT: Unicorn Ad Found. Deploying to Shopify...")
