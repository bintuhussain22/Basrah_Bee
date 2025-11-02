"""
PCOS Food Tracker — Automated Version (Chapters 13 + 14)
---------------------------------------------------------
Fetches nutrition info automatically from Edamam API,
estimates Glycemic Index & Insulin Risk, and stores results in SQLite.
"""

import sqlite3
import urllib.request, urllib.parse, json

# --- API CONFIG ---
APP_ID = "4fb0f986"
APP_KEY = "665a4a71517cd9b7e08704a6d4542b4f"
BASE_URL = "https://api.edamam.com/api/food-database/v2/parser"


# --- DATABASE SETUP ---
def create_table():
    """Create the SQLite table if not exists."""
    conn = sqlite3.connect('food_log.sqlite')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS food_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food TEXT,
        calories REAL,
        carbs REAL,
        fiber REAL,
        fat REAL,
        protein REAL,
        gi REAL,
        insulin_score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    return conn, cur


# --- API FETCH ---
def fetch_food_data(food_name):
    """Fetch food info from Edamam API."""
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "ingr": food_name,
        "nutrition-type": "logging"
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    print(f"\n🔎 Fetching data for '{food_name}'...")

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode()
            js = json.loads(data)
            if "parsed" not in js or not js["parsed"]:
                print("⚠️ Food not found. Try a different name.")
                return None
            item = js["parsed"][0]["food"]
            nutrients = item["nutrients"]
            return {
                "name": item["label"],
                "calories": nutrients.get("ENERC_KCAL", 0),
                "carbs": nutrients.get("CHOCDF", 0),
                "fiber": nutrients.get("FIBTG", 0),
                "fat": nutrients.get("FAT", 0),
                "protein": nutrients.get("PROCNT", 0)
            }
    except Exception as e:
        print("❌ Error fetching data:", e)
        return None


# --- GI & INSULIN LOGIC ---
def estimate_gi(n):
    """Estimate glycemic index based on nutrient ratio."""
    carbs, fiber, fat, protein = n["carbs"], n["fiber"], n["fat"], n["protein"]
    gi = 70 * (carbs / (carbs + fiber + fat + protein + 1)) - fiber * 2 - fat * 0.5
    return round(max(0, min(100, gi)), 1)


def insulin_risk(n):
    """Estimate insulin risk (0–10)."""
    carbs, fiber, fat, protein = n["carbs"], n["fiber"], n["fat"], n["protein"]
    score = (carbs - fiber) / (protein + fat + 1)
    return round(max(0, min(10, score)), 1)


# --- DATABASE INSERT ---
def insert_food(cur, data):
    """Insert one food record into database."""
    cur.execute('''
    INSERT INTO food_log (food, calories, carbs, fiber, fat, protein, gi, insulin_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["name"], data["calories"], data["carbs"], data["fiber"], data["fat"],
          data["protein"], data["gi"], data["insulin"]))


# --- SHOW SUMMARY ---
def show_summary(cur):
    """Display recent foods and best PCOS choices."""
    print("\n📋 Your PCOS Food Log:")
    for row in cur.execute(
        'SELECT id, food, gi, insulin_score, timestamp FROM food_log ORDER BY timestamp DESC LIMIT 10'
    ):
        print(row)

    print("\n🥇 Top 5 lowest-GI foods (best for PCOS):")
    for row in cur.execute('SELECT food, gi FROM food_log ORDER BY gi ASC LIMIT 5'):
        print(f"  • {row[0].title()} — GI {row[1]}")


# --- MAIN PROGRAM ---
def main():
    conn, cur = create_table()
    print("\n🥗 Welcome to the PCOS Food Tracker (Auto Version)!")
    print("Type your food name to fetch data, or 'quit' to stop.\n")

    while True:
        food = input("🍽 Food name (or 'quit' to exit): ").strip()
        if food.lower() == "quit":
            break

        data = fetch_food_data(food)
        if not data:
            continue

        # Compute scores
        data["gi"] = estimate_gi(data)
        data["insulin"] = insulin_risk(data)

        print(f"✅ Found: {data['name']}")
        print(
            f"Calories: {data['calories']} kcal | Carbs: {data['carbs']} g | Fiber: {data['fiber']} g | Fat: {data['fat']} g | Protein: {data['protein']} g"
        )
        print(f"Predicted GI: {data['gi']} | Insulin Risk: {data['insulin']}/10")

        insert_food(cur, data)
        conn.commit()
        print(f"💾 Saved {data['name']} to your PCOS food log!\n")

    show_summary(cur)
    conn.close()
    print("\n🌿 Data saved in 'food_log.sqlite'. Goodbye, Basrah! 🩷")


if __name__ == "__main__":
    main()
