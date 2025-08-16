# Chapter 7 Practice: Cycle Notes Analyzer (robust BBT parsing)
import re

def analyze_cycle_notes(filename):
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        print("File not found:", filename)
        return

    temps = []
    fertile_days = []
    symptom_days = []

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        lower = raw.lower()
        day = raw.split(":", 1)[0].strip()

        # ---- Robust BBT capture: matches 'BBT 36.70' even if followed by commas ----
        m = re.search(r'bbt\s*([0-9]+(?:\.[0-9]+)?)', lower)
        if m:
            temps.append(float(m.group(1)))

        # Fertile signs
        if "eggwhite" in lower or "opk positive" in lower:
            fertile_days.append(day)

        # Symptoms
        if "cramp" in lower:
            symptom_days.append(day)

    print("=== Cycle Notes Report ===")
    print("Total BBT entries:", len(temps))
    if temps:
        avg = round(sum(temps) / len(temps), 2)
        print("Average BBT:", avg)
    print("Possible fertile days:", fertile_days)
    print("Days with cramps:", symptom_days)


if __name__ == "__main__":
    analyze_cycle_notes("cycle_notes.txt")
