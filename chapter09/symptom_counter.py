# Chapter 9: Dictionaries — Symptom Frequency Counter (PCOS-themed)

def parse_file(fname):
    """Read all lines from cycle_notes.txt into a list (lowercased)."""
    try:
        with open(fname, "r", encoding="utf-8") as fh:
            return [line.strip().lower() for line in fh if line.strip()]
    except FileNotFoundError:
        print("File not found:", fname)
        return []

def count_symptoms(lines):
    """Build a dictionary counting occurrences of symptoms."""
    symptoms = ["cramp", "spotting", "breast", "nausea", "bloat", "headache", "mood"]
    counts = {}

    for line in lines:
        for s in symptoms:
            if s in line:
                counts[s] = counts.get(s, 0) + 1
    return counts

def fertile_days(lines):
    """Build a dictionary mapping Day -> fertile sign(s)."""
    fert_dict = {}
    for line in lines:
        if line.startswith("day"):
            day = line.split(":")[0].capitalize()
            fert_dict[day] = []

            if "opk positive" in line:
                fert_dict[day].append("OPK+")
            if "eggwhite" in line or "slippery" in line or "watery" in line:
                fert_dict[day].append("CM fertile")
    return fert_dict

def main():
    lines = parse_file("cycle_notes.txt")

    print("=== Chapter 9: Dictionary Practice ===")

    # Symptom dictionary
    sym_counts = count_symptoms(lines)
    print("\nSymptom counts:", sym_counts)

    if sym_counts:
        most_common = max(sym_counts, key=sym_counts.get)
        print("Most common symptom:", most_common, "(", sym_counts[most_common], "times )")

    # Fertile dictionary
    fert = fertile_days(lines)
    print("\nFertile day signals:")
    for k, v in fert.items():
        if v:
            print(f"{k}: {', '.join(v)}")

if __name__ == "__main__":
    main()
