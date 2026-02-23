import time
from review_brain import analyze_review
from ad_math import run_simulation

def run_genie():
    print("\n" + "="*50)
    print("🔥 NICHEFORGE x MERRITT DIGITAL VENTURES 🔥")
    print("="*50)
    
    # Simulate finding a high-value review
    review = "I was skeptical about NicheForge, but it finally fixed my workflow!"
    analysis = analyze_review(review)
    
    print(f"[*] Brain Output: {analysis['hook']}")
    
    # Run the math based on your 'Unicorn' 7.76x metrics
    results = run_simulation(budget=500, cpc=0.45, conversion_rate=0.04, product_price=97.00)
    
    print(f"[*] Projected ROAS: {results['roas']}x")
    print(f"[*] Net Profit: ${results['profit']}")
    print("\n[✔] ALL SYSTEMS GREEN. READY TO FORGE.")
    print("="*50)

if __name__ == "__main__":
    run_genie()
