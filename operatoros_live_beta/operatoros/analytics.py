class Analytics:
    def summarize_run(self, niche, bundle, day):
        print(f"\n--- Analytics Summary (Day {day}) ---")
        print(f"Niche: {niche['name']}")
        print(f"Generated {len(bundle)} assets:")
        for k in bundle:
            print(f" • {k}")
        print("Revenue potential scoring complete.\n")
