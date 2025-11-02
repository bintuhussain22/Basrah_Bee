"""
PCOS Food & Nutrition Finder
---------------------------------
Chapter 12 Project — Python for Everybody (Networked Programs)
Author: Basrah Bee

Description:
This program connects to the Edamam Food Database API to fetch real-time
nutrition data for any food entered by the user. It then displays calories,
macronutrients, and a PCOS-friendly note based on fiber content.
"""

import urllib.request
import urllib.parse
import json

def fetch_food_data(food):
    """Fetch nutrition data for a food item from Edamam API."""
    app_id = "4fb0f986"  # your Edamam Application ID
    app_key = "665a4a71517cd9b7e08704a6d4542b4f"  # your Edamam Application Key
    base_url = "https://api.edamam.com/api/food-database/v2/parser"

    # Build URL query parameters
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "ingr": food,
        "nutrition-type": "logging"
    }

    url = base_url + "?" + urllib.parse.urlencode(params)
    print(f"\n🔎 Fetching data for '{food}' ...")

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode()
            js = json.loads(data)
            return js
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} — Check your API credentials or quota.")
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: {e.reason}")
    except Exception as e:
        print("❌ Unexpected Error:", e)
    return None


def show_nutrition(js):
    """Display nutrition info and PCOS-friendly note."""
    try:
        item = js["parsed"][0]["food"]
        label = item["label"]
        nutrients = item["nutrients"]

        print(f"\n=== 🍽 {label.title()} ===")
        print(f"Calories: {nutrients.get('ENERC_KCAL', 'N/A')} kcal")
        print(f"Protein: {nutrients.get('PROCNT', 'N/A')} g")
        print(f"Fat: {nutrients.get('FAT', 'N/A')} g")
        print(f"Fiber: {nutrients.get('FIBTG', 'N/A')} g")
        print(f"Carbs: {nutrients.get('CHOCDF', 'N/A')} g")

        fiber = nutrients.get("FIBTG", 0)
        carbs = nutrients.get("CHOCDF", 0)

        # Simple PCOS-friendly logic
        if fiber >= 3 and carbs <= 20:
            note = "🌿 Excellent for PCOS — high fiber, low carb!"
        elif fiber >= 3:
            note = "🌿 Good for PCOS — helps stabilize blood sugar."
        elif carbs > 30:
            note = "⚠️ High in carbs — eat in moderation."
        else:
            note = "😊 Neutral food — enjoy in balanced portions."

        print("Note:", note)

    except (KeyError, IndexError):
        print("⚠️ Food not found or incomplete data.")


def main():
    print("\n🥗 Welcome to the PCOS Food & Nutrition Finder!")
    print("Type any food name to get its nutrition info.")
    print("Type 'quit' anytime to exit.\n")

    while True:
        food = input("Enter a food name (or 'quit' to exit): ").strip()
        if food.lower() == "quit":
            print("\nGoodbye 👋 Stay mindful and eat nourishing foods!")
            break
        if not food:
            print("Please enter a valid food name.")
            continue

        js = fetch_food_data(food)
        if js:
            show_nutrition(js)


if __name__ == "__main__":
    main()
