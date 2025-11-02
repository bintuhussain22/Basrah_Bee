"""
PCOS Food Tracker 2.0 — Combined API + SQL Project
---------------------------------------------------
Author: Basrah Bee

This integrates:
• Chapter 13 — Using Web Services (Edamam API)
• Chapter 14 — Using Databases (SQLite)
• Chapter 15 — Using SQL for Analysis

Features:
- Fetch nutrition data automatically via Edamam API
- Compute GI, GL, and Insulin Risk
- Save all entries to SQLite
- Show daily total glycemic load and average insulin score
"""

import sqlite3
import urllib.request, urllib.parse, json
from datetime import datetime, date

# --- API CONFIG ---
APP_ID = "4fb0f986"
APP_KEY = "665a4a71517cd9b7e08704a6d4542b4f"
BASE_URL = "https://api.edamam.com/api/food-database/v2/parser"

# --- DATABASE SETUP ---
def create_table():
    """Create SQLite database and table."""
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
        gl REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    return conn, cur

# --- API FETCH ---
def fetch_food_data(food_name):
    """Fetch nutrition data for a given food using Edamam API."""
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
                print("⚠️ Food not found. Try another name.")
                return None
            item = js["parsed"][0]["food"]
            n = item["nutrients"]
            return {
                "name": item["label"],
                "calories": n.get("ENERC_KCAL", 0),
                "carbs": n.get("CHOCDF", 0),
                "fiber": n.get("FIBTG", 0),
                "fat": n.get("FAT", 0),
                "protein": n.get("PROCNT", 0)
            }
    except Exception as e:
        print("❌ Error fetching data:", e)
        return None

# --- METABOLIC CALCULATIONS ---
def estimate_gi(n):
    carbs, fiber, fat, protein = n["carbs"], n["fiber"], n["fat"], n["protein"]
    gi = 70 * (carbs / (carbs + fiber + fat + protein + 1)) - fiber * 2 - fat * 0.5
    return round(max(0, min(100, gi)), 1)

def insulin_risk(n):
    carbs, fiber, fat, protein = n["carbs"], n["fiber"], n["fat"], n["protein"]
    score = (carbs - fiber) / (protein + fat + 1)
    return round(max(0, min(10, score)), 1)

def estimate_gl(gi, carbs):
    gl = (gi * carbs) / 100
    return round(gl, 1)

# --- DATABASE INSERT ---
def insert_food(cur, data):
    """Insert one record into the food_log table."""
    cur.execute('''
    INSERT INTO food_log (food, calories, carbs, fiber, fat, protein, gi, insulin_score, gl)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["name"], data["calories"], data["carbs"], data["fiber"], data["fat"],
          data["protein"], data["gi"], data["insulin"], data["gl"]))

# --- SQL QUERIES ---
def show_today_summary(cur):
    """Show today's total glycemic load and average insulin score."""
    today = date.today().strftime("%Y-%m-%d")
    cur.execute('''
        SELECT ROUND(SUM(gl),1), ROUND(AVG(insulin_score),1)
        FROM food_log
        WHERE DATE(timestamp) = ?
    ''', (today,))
    row = cur.fetchone()
    print("\n📅 --- Today's Summary ---")
    print(f"Date: {today}")
    print(f"Total Glycemic Load: {row[0] or 0}")
    print(f"Average Insulin Score: {row[1] or 0}/10")

def show_best_foods(cur):
    print("\n🌿 --- Top 5 Lowest GL Foods ---")
    cur.execute('SELECT food, gl FROM food_log ORDER BY gl ASC LIMIT 5')
    for row in cur.fetchall():
        print(f"  • {row[0]} — GL {row[1]}")

# --- MAIN PROGRAM ---
def main():
    conn, cur = create_table()

    print("\n🥗 Welcome to the PCOS Food Tracker 2.0!")
    print("Type any food name to log it, or 'quit' to stop.\n")

    while True:
        food = input("🍽 Enter food name (or 'quit' to exit): ").strip()
        if food.lower() == "quit":
            break

        data = fetch_food_data(food)
        if not data:
            continue

        # Compute metrics
        data["gi"] = estimate_gi(data)
        data["insulin"] = insulin_risk(data)
        data["gl"] = estimate_gl(data["gi"], data["carbs"])

        print(f"\n✅ {data['name']} added!")
        print(f"Calories: {data['calories']} kcal | Carbs: {data['carbs']}g | Fiber: {data['fiber']}g | Fat: {data['fat']}g | Protein: {data['protein']}g")
        print(f"GI: {data['gi']} | GL: {data['gl']} | Insulin Risk: {data['insulin']}/10")

        # Save to database
        insert_food(cur, data)
        conn.commit()

    # Show daily summary after quitting
    show_today_summary(cur)
    show_best_foods(cur)

    conn.close()
    print("\n🌸 All data saved in 'food_log.sqlite'. Goodbye, Basrah! 🩷")

if __name__ == "__main__":
    main()
