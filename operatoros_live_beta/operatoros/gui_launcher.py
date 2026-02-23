#!/usr/bin/env python3
import sys
import os

# --- API Setup ---
def check_or_prompt_keys():
    keys_file = os.path.expanduser("~/.operatoros_keys")
    keys = {}
    # Load existing keys
    if os.path.exists(keys_file):
        with open(keys_file, 'r') as f:
            for line in f:
                k,v = line.strip().split('=',1)
                keys[k] = v

    for key_name in ["TWITTER_BEARER_TOKEN", "STRIPE_API_KEY", "GUMROAD_ACCESS_TOKEN"]:
        if key_name not in keys or not keys[key_name]:
            keys[key_name] = input(f"Enter {key_name}: ").strip()

    # Save all keys
    with open(keys_file, 'w') as f:
        for k,v in keys.items():
            f.write(f"{k}={v}\n")
    print("All required API keys saved.")

# --- Logger ---
def log_run(entry):
    os.makedirs("logs", exist_ok=True)
    with open("logs/operatoros.log", "a") as f:
        f.write(entry+"\n")

# --- API Fetcher / Niche Research ---
class APIFetcher:
    def fetch_trends(self):
        return [{"name": "AI Prompt Packs"}, {"name": "Local Lead Gen"}, {"name": "E-commerce Automation"}]

    def score_niches(self, niches, mock=False):
        if mock:
            for n in niches:
                n["score"] = 50
        else:
            for n in niches:
                n["score"] = n.get("revenue", 0)
        return niches

def get_top_niches(mock=True):
    fetcher = APIFetcher()
    trends = fetcher.fetch_trends()
    scored = fetcher.score_niches(trends, mock=mock)
    return scored

# --- Bundle Generator ---
def generate_bundle(niche_name):
    os.makedirs("bundles", exist_ok=True)
    bundle_path = f"bundles/{niche_name.replace(' ','_')}_bundle.zip"
    with open(bundle_path, "w") as f:
        f.write(f"Bundle for {niche_name}\n")  # placeholder for actual bundle generation
    return bundle_path

# --- GUI / Terminal Interface ---
def print_menu():
    print("\n=== OperatorOS Terminal GUI ===")
    print("1. View top niches")
    print("2. Enter custom niche")
    print("3. Generate product bundle")
    print("4. Exit")

def select_niche():
    top_niches = get_top_niches(mock=True)
    print("\nTop Niches:")
    for i, n in enumerate(top_niches, start=1):
        print(f"{i}. {n['name']} (Score: {n['score']})")
    choice = input("Select a niche by number or enter 'c' for custom: ").strip()
    if choice.lower() == 'c':
        return input("Enter your custom niche: ").strip()
    try:
        return top_niches[int(choice)-1]['name']
    except:
        print("Invalid choice, defaulting to first niche.")
        return top_niches[0]['name']

def main():
    check_or_prompt_keys()
    current_niche = None
    while True:
        print_menu()
        option = input("Choose an option: ").strip()
        if option == '1':
            current_niche = select_niche()
            print(f"Selected niche: {current_niche}")
        elif option == '2':
            current_niche = input("Enter your custom niche: ").strip()
            print(f"Selected custom niche: {current_niche}")
        elif option == '3':
            if not current_niche:
                print("No niche selected. Please select or enter a niche first.")
                continue
            print(f"Generating bundle for '{current_niche}'...")
            bundle_path = generate_bundle(current_niche)
            print(f"Bundle generated: {bundle_path}")
            log_run(f"Generated bundle for {current_niche}")
        elif option == '4':
            print("Exiting OperatorOS GUI.")
            sys.exit(0)
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
