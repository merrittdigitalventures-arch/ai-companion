def launch_gui(scored_niches):
    print("--- Launching OperatorOS GUI ---")
    if not scored_niches:
        print("No niches available. Please run scoring first.")
        return

    # Display available niches for user selection
    print("Select a niche to continue:")
    for idx, niche in enumerate(scored_niches, start=1):
        print(f"{idx}. {niche['name']} (Score: {niche.get('score', 0)})")

    choice = input("Enter the number of your chosen niche: ")
    try:
        choice_idx = int(choice) - 1
        selected = scored_niches[choice_idx]
        print(f"Selected niche: {selected['name']}")
        # Set current niche in state
        from operatoros.state import set_current_niche
        set_current_niche(selected)
    except (ValueError, IndexError):
        print("Invalid choice. OperatorOS halted.")
        return
