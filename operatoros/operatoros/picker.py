def pick_niche(top_5, state):
    if state.get("autopick") and "last_niche" in state:
        chosen = state["last_niche"]
    else:
        print("Top 5 Niches by Revenue Potential:\n")
        for i, niche in enumerate(top_5, 1):
            print(f"{i}. {niche['niche']} (Score: {niche['revenue_score']})")
        choice = input("Pick a niche number [1-5] (1): ") or "1"
        chosen = top_5[int(choice)-1]
        if state.get("autopick"):
            state["last_niche"] = chosen
    return chosen
