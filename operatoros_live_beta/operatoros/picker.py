class Picker:
    def __init__(self, state):
        self.state = state

    def choose_niche(self, top_niches):
        # Manual pick by default
        print("\nTop 5 Niches by Revenue Potential:\n")
        for i, niche in enumerate(top_niches, 1):
            print(f"{i}. {niche['name']} (Score: {niche['score']})")

        choice = input("\nPick a niche number [1/2/3/4/5] (1): ")
        choice = int(choice) if choice.isdigit() else 1
        chosen_niche = top_niches[choice - 1]

        # Autopick toggle
        auto = input("Enable autopick going forward? [y/n] (n): ")
        self.state.set("autopick", auto.lower() == "y")
        self.state.set("current_niche", chosen_niche)

        print(f"\nSelected niche: {chosen_niche['name']} (Revenue score: {chosen_niche['score']})")
        return chosen_niche
