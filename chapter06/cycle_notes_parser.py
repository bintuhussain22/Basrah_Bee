"""
Chapter 6: Strings — Cycle Notes String Parser (PCOS project)
Educational only. Parses simple text notes like:
  "D14: OPK pos @ 5:45am; BBT 36.45; CM: eggwhite; cramps mild"
No regex—just Chapter-6 string methods.
"""

def to_float_safe(s: str) -> float | None:
    """Return float if possible; else None."""
    try:
        return float(s)
    except:
        return None

def extract_day(note: str) -> int | None:
    # Expect patterns like "D14:" or "Day 14"
    n = note.strip()
    n_low = n.lower()
    if n_low.startswith("d"):
        # e.g., "D14: ..." -> slice after leading 'd'
        # take consecutive digits
        digits = ""
        for ch in n[1:]:
            if ch.isdigit():
                digits += ch
            else:
                break
        return int(digits) if digits else None
    if n_low.startswith("day "):
        parts = n.split()  # ["Day", "14", ...]
        if len(parts) >= 2 and parts[1].isdigit():
            return int(parts[1])
    return None

def extract_opk(note: str) -> str | None:
    n = note.lower()
    if "opk" in n:
        # look for "opk pos" or "opk neg"
        if "opk pos" in n or "opk positive" in n:
            return "positive"
        if "opk neg" in n or "opk negative" in n:
            return "negative"
    return None

def extract_bbt(note: str) -> float | None:
    n = note.lower()
    if "bbt" not in n:
        return None
    # crude parse: split by ';' and look for piece starting with "bbt"
    pieces = [p.strip() for p in n.split(";")]
    for p in pieces:
        if p.startswith("bbt"):
            # examples: "bbt 36.45" or "bbt:36.6"
            p = p.replace("bbt", "").replace(":", " ").strip()
            # first token that looks like a number
            for tok in p.split():
                val = to_float_safe(tok)
                if val is not None:
                    return val
    return None

def extract_cm(note: str) -> str | None:
    # cervical mucus description after "CM:" or "cm "
    n = note.lower()
    if "cm:" in n:
        after = n.split("cm:", 1)[1].strip()
        # take up to next ';'
        desc = after.split(";", 1)[0].strip()
        return desc if desc else None
    if "cm " in n:
        # e.g., "CM eggwhite"
        after = n.split("cm ", 1)[1].strip()
        return after.split(";", 1)[0].strip() or None
    # common keywords
    for k in ["eggwhite", "creamy", "watery", "sticky", "dry"]:
        if k in n:
            return k
    return None

def extract_symptoms(note: str) -> list[str]:
    n = note.lower()
    keywords = [
        "cramp", "cramps", "bloat", "spotting", "tender", "sore",
        "fatigue", "headache", "nausea", "mood"
    ]
    found = []
    for k in keywords:
        if k in n and k not in found:
            found.append(k)
    return found

def parse_note(note: str) -> dict:
    return {
        "day": extract_day(note),
        "opk": extract_opk(note),
        "bbt": extract_bbt(note),
        "cm": extract_cm(note),
        "symptoms": extract_symptoms(note),
        "raw": note.strip()
    }

def normalize_note(note: str) -> str:
    """Basic cleanup using string methods."""
    return " ".join(note.strip().replace("\t", " ").split())

def demo():
    notes = [
        "D14: OPK pos @ 5:45am; BBT 36.45; CM: eggwhite; cramps mild",
        "Day 15 OPK negative; bbt:36.25; cm creamy; slight spotting",
        "d16: bbt 36.60; CM watery; mood low",
        "D17: OPK positive; BBT 36.58; tender breasts",
        "Day 18  cm dry; headache"
    ]
    print("=== Chapter 6 Cycle Notes Parser (demo) ===")
    for line in notes:
        clean = normalize_note(line)
        result = parse_note(clean)
        print(result)

if __name__ == "__main__":
    demo()
