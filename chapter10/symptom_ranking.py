# Chapter 10: Tuples — Ranking Symptoms (PCOS-themed)

def parse_file(fname):
    """Read all lines from cycle_notes.txt into a list (lowercased)."""
    try:
        with open(fname, "r", encoding="utf-8") as fh:
            return [line.strip().lower() for line in fh if line.strip()]
    except FileNotFoundError:
        print("File not found:", fname)
        return []

def count_symptoms(lines):
    """Build a dictionary of symptom counts."""
    symptoms = ["cramp", "spotting", "breast", "nausea", "bloat", "headache", "mood"]
    counts = {}
    for line in lines:
        for s in symptoms:
            if s in line:
                counts[s] = counts.get(s, 0) + 1
    return counts

def rank_symptoms(counts):
    """
    Convert dictionary into a list of tuples (count, symptom),
    then sort by count (highest first).
    """
    tuples = [(v, k) for k, v in counts.items()]
    tuples = sorted(tuples, reverse=True)
    return tuples

def main():
    lines = parse_file("cycle_notes.txt")
    print("=== Chapter 10: Tuple Practice ===")

    # Step 1: dictionary
    sym_counts = count_symptoms(lines)
    print("\nSymptom dictionary:", sym_counts)

    # Step 2: convert to tuples and sort
    ranked = rank_symptoms(sym_counts)
    print("\nSymptoms ranked by frequency:")
    for count, symptom in ranked:
        print(f"{symptom} → {count} times")

    # Step 3: show the top symptom
    if ranked:
        print("\nMost frequent symptom:", ranked[0][1],
              "(", ranked[0][0], "times )")

if __name__ == "__main__":
    main()
