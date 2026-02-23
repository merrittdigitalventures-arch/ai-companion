from dotenv import load_dotenv, set_key
import os

load_dotenv()

print("\n--- OperatorOS API Setup ---\n")

# Twitter
twitter = input("Enter TWITTER_BEARER_TOKEN: ")
set_key(".env", "TWITTER_BEARER_TOKEN", twitter)

# Stripe
stripe = input("Enter STRIPE_API_KEY: ")
set_key(".env", "STRIPE_API_KEY", stripe)

# Gumroad
gumroad = input("Enter GUMROAD_ACCESS_TOKEN: ")
set_key(".env", "GUMROAD_ACCESS_TOKEN", gumroad)

print("\nAll required API keys saved.\n")
