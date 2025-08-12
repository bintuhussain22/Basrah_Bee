def cycle_irregularity(avg_cycle_len_days: float, cycles_per_year: int) -> bool:
    """Return True if cycles look oligo/irregular by simple rules."""
    if avg_cycle_len_days <= 0 or cycles_per_year <= 0:
        return False
    # Simple flags: long cycles, very short cycles, or <8 cycles/year
    return (avg_cycle_len_days > 35) or (avg_cycle_len_days < 21) or (cycles_per_year < 8)

def hyperandrogenism_flags(hirsutism: bool, acne: bool, hair_thinning: bool) -> bool:
    """Return True if there’s any clinical hyperandrogenism sign."""
    return bool(hirsutism or acne or hair_thinning)

def ovarian_appearance(known_pc_ovaries: bool = False, amh_high: bool = False) -> bool:
    """
    Proxy for 'polycystic ovarian morphology'.
    If user knows ultrasound shows PCO or AMH is high, treat as True.
    """
    return bool(known_pc_ovaries or amh_high)

def bmi_category(weight_kg: float, height_m: float) -> str:
    """Compute BMI and return a simple category string."""
    if height_m <= 0:
        return "unknown"
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"

# ---------- Rotterdam-style aggregator ----------

def rotterdam_criteria(irregular: bool, hyperandrogenism: bool, pco_morphology: bool) -> tuple[bool, int]:
    """
    Returns (meets_screening, count_true) based on 2-of-3 simple checks.
    """
    count = int(irregular) + int(hyperandrogenism) + int(pco_morphology)
    return (count >= 2, count)

# ---------- User-facing wrapper ----------

def pcos_screen(
    avg_cycle_len_days: float,
    cycles_per_year: int,
    hirsutism: bool = False,
    acne: bool = False,
    hair_thinning: bool = False,
    known_pc_ovaries: bool = False,
    amh_high: bool = False,
    weight_kg: float = 0.0,
    height_m: float = 0.0
) -> dict:
    """
    Orchestrates the helper functions and returns a structured result dict.
    """
    irregular = cycle_irregularity(avg_cycle_len_days, cycles_per_year)
    hyper = hyperandrogenism_flags(hirsutism, acne, hair_thinning)
    pco = ovarian_appearance(known_pc_ovaries, amh_high)
    meets, tally = rotterdam_criteria(irregular, hyper, pco)
    bmi_cat = bmi_category(weight_kg, height_m)

    return {
        "cycle_irregularity": irregular,
        "hyperandrogenism": hyper,
        "pco_morphology_proxy": pco,
        "rotterdam_count_true": tally,
        "meets_2_of_3_screen": meets,
        "bmi_category": bmi_cat,
        "note": (
            "Educational only — not a diagnosis. See a clinician for proper evaluation."
        )
    }
# ---------- Quick demo (you can replace with your own values) ----------

def demo():
    result = pcos_screen(
        avg_cycle_len_days=35.5,
        cycles_per_year=9,
        hirsutism=True,
        acne=False,
        hair_thinning=False,
        known_pc_ovaries=False,
        amh_high=True,     # if unknown, set False
        weight_kg=62,
        height_m=1.54
    )
    print("=== PCOS Screening Helper (Demo) ===")
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    demo()