# Chapter 8: Lists — List-Powered Cycle Summaries (PCOS-themed)
# Option B: Scientifically-aligned ovulation detection (sustained thermal shift)

import re

def parse_file(fname):
    """
    Parse a simple text file with lines like:
      Day 14: BBT 36.70, OPK positive, CM eggwhite, cramps
    Returns parallel lists: days, bbt, opk, cm, symptoms
    """
    days, bbt, opk, cm, symptoms = [], [], [], [], []
    try:
        with open(fname, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue

                # Day (e.g., "Day 14: ...")
                mday = re.match(r"Day\s+(\d+)\s*:", line, flags=re.I)
                days.append(int(mday.group(1)) if mday else None)

                lower = line.lower()

                # BBT (e.g., "BBT 36.70") — robust to trailing commas
                mbbt = re.search(r"bbt\s*([0-9]+(?:\.[0-9]+)?)", lower)
                bbt.append(float(mbbt.group(1)) if mbbt else None)

                # OPK (positive/negative)
                if "opk positive" in lower:
                    opk.append("positive")
                elif "opk" in lower and "negative" in lower:
                    opk.append("negative")
                else:
                    opk.append(None)

                # CM (dry/sticky/creamy/eggwhite/watery/slippery)
                cm_val = None
                for tag in ["eggwhite", "slippery", "watery", "creamy", "sticky", "dry"]:
                    if tag in lower:
                        cm_val = tag
                        break
                cm.append(cm_val)

                # Symptoms (simple flags list)
                sym = []
                for s in ["cramp", "spotting", "breast", "nausea", "bloat", "headache", "mood"]:
                    if s in lower:
                        sym.append(s)
                symptoms.append(sym if sym else None)

        return days, bbt, opk, cm, symptoms

    except FileNotFoundError:
        print("File not found:", fname)
        return [], [], [], [], []

def bbt_stats(bbt):
    vals = [x for x in bbt if isinstance(x, float)]
    if not vals:
        return None, None, None
    return min(vals), max(vals), round(sum(vals)/len(vals), 2)

def rolling_mean(bbt, window=3):
    out = []
    for i in range(len(bbt)):
        window_vals = [x for x in bbt[max(0, i-window+1):i+1] if isinstance(x, float)]
        out.append(round(sum(window_vals)/len(window_vals), 2) if window_vals else None)
    return out

def fertile_indices(opk, cm):
    """Indexes where OPK is positive OR CM is eggwhite/slippery/watery."""
    idx = []
    for i in range(len(opk)):
        if (opk[i] == "positive") or (cm[i] in ["eggwhite", "slippery", "watery"]):
            idx.append(i)
    return idx

def ovulation_index_sustained(bbt, lookback=6, rise=0.25, sustain_days=3):
    """
    Detect ovulation as the FIRST day with a temperature ≥ (avg of prior `lookback` days + `rise`)
    and this elevation is sustained for `sustain_days` consecutive days.

    Notes:
    - Requires enough prior non-None temps.
    - This is a retrospective estimate; clinical confirmation is via serum progesterone or ultrasound.
    """
    n = len(bbt)
    for i in range(lookback, n - sustain_days + 1):
        prev = [x for x in bbt[i-lookback:i] if isinstance(x, float)]
        if len(prev) < max(3, lookback // 2):
            continue  # not enough reliable past temps
        avg_prev = sum(prev) / len(prev)

        ok = True
        for j in range(sustain_days):
            if not isinstance(bbt[i + j], float) or bbt[i + j] < avg_prev + rise:
                ok = False
                break
        if ok:
            return i
    return None

def main():
    # Read from a local text file in the same folder
    days, bbt, opk, cm, symptoms = parse_file("cycle_notes.txt")

    print("=== Chapter 8: List-Powered Cycle Summaries ===")
    print("Rows parsed:", len(days))

    mn, mx, avg = bbt_stats(bbt)
    print("BBT min/max/avg:", (mn, mx, avg))

    roll3 = rolling_mean(bbt, window=3)
    fert_idx = fertile_indices(opk, cm)
    print("Fertile days (indexes):", fert_idx)
    print("Fertile days (cycle days):", [days[i] for i in fert_idx] if fert_idx else [])
    print("3-day rolling mean (first 10):", roll3[:10])

    # Scientifically-aligned ovulation detection (sustained rise)
    ovu_idx = ovulation_index_sustained(bbt, lookback=6, rise=0.25, sustain_days=3)
    if ovu_idx is not None:
        print("Ovulation cue at index:", ovu_idx, "→ cycle day", days[ovu_idx])
        print("(Note: BBT-based ovulation is retrospective; confirm with clinical testing if needed.)")
    else:
        print("No ovulation cue found with sustained-rise rule.")
        print("(Tip: ensure enough pre-ovulation temps; consider lookback=5, rise=0.20 if data are sparse.)")

if __name__ == "__main__":
    main()
