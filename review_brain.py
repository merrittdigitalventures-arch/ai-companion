def analyze_review(text):
    # Red flags that kill an ad immediately
    red_flags = ["broken", "junk", "refund", "terrible", "scam", "slow", "waste"]
    hooks = ["fixed", "finally", "best", "saved", "amazing", "results"]
    
    # Check for red flags first
    if any(flag in text.lower() for flag in red_flags):
        return {"score": -1, "hook": "DISCARD: Negative Sentiment"}
    
    score = sum([1 for word in hooks if word in text.lower()])
    sentences = text.split('!')
    best_hook = text
    for s in sentences:
        if any(h in s.lower() for h in hooks):
            best_hook = s.strip()
            break
    return {"score": score, "hook": best_hook}

# Test the safety gate
test_data = [
    "Finally, a refund! This was junk.", 
    "This amazing tool finally fixed my life!"
]

print("[*] Testing Safety Gate...")
for t in test_data:
    res = analyze_review(t)
    print(f"Input: {t[:20]}... | Result: {res['hook']}")
