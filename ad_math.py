import random

def run_simulation(budget, cpc, conversion_rate, product_price):
    clicks = budget / cpc
    sales = clicks * conversion_rate
    revenue = sales * product_price
    profit = revenue - budget
    roas = revenue / budget if budget > 0 else 0
    
    return {
        "clicks": int(clicks),
        "sales": int(sales),
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "roas": round(roas, 2)
    }

# Variables for Merritt Digital Ventures
BUDGET = 500.00         # Total spend
CPC = 0.85              # Cost per click (Average for tech ads)
CONV_RATE = 0.03        # 3% of people buy
PRICE = 97.00           # Your product price

print("\n[*] CAMPAIGN SIMULATOR: AD VARIANT B (10 HOURS SAVED)")
print("="*45)
results = run_simulation(BUDGET, CPC, CONV_RATE, PRICE)

print(f"Total Clicks: {results['clicks']}")
print(f"Total Sales:  {results['sales']}")
print(f"Revenue:      ${results['revenue']}")
print(f"Net Profit:   ${results['profit']}")
print(f"ROAS:         {results['roas']}x (Return on Ad Spend)")

if results['roas'] > 2:
    print("\n[+] STRATEGY: High Performance. Scale the budget!")
else:
    print("\n[-] STRATEGY: Optimize the 'Brain' hooks to lower CPC.")
