"""
PCOS Screening CLI — Chapter 5 (Loops & Iteration)
NOTE: Educational practice only — not a medical diagnosis.
This script lets you run multiple screenings in one session using loops.
"""

# --- Reuse the core logic from Chapter 4 (kept inline for simplicity) ---

def cycle_irregularity(avg_cycle_len_days: float, cycles_per_year: int) -> bool:
    if avg_cycle_len_days <= 0 or cycles_per_year <= 0:
        return False
    return (avg_cycle_len_days > 35) or (avg_cycle_len_days < 21) or (cycles_per_year < 8)

def hyperandrogenism_flags(hirsutism: bool, acne: bool, hair_thinning: bool) -> bool:
    return bool(hirsutism or acne or hair_thinning)

def ovarian_appearance(known_pc_ovaries: bool = False, amh_high: bool = False) -> bool:
    return bool(known_pc_ovaries or amh_high)

def bmi_value(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        return 0.0
    return weight_kg / (height_m ** 2)

def bmi_category_from_value(bmi: float) -> str:
    if bmi == 0.0:
        return "unknown"
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"

def rotterdam_criteria(irregular: bool, hyperandrogenism: bool, pco_morphology: bool) -> tuple[bool, int]:
    count = int(irregular) + int(hyperandrogenism) + int(pco_morphology)
    return (count >= 2, count)

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
    irregular = cycle_irregularity(avg_cycle_len_days, cycles_per_year)
    hyper = hyperandrogenism_flags(hirsutism, acne, hair_thinning)
    pco = ovarian_appearance(known_pc_ovaries, amh_high)
    meets, tally = rotterdam_criteria(irregular, hyper, pco)
    bmi = bmi_value(weight_kg, height_m)
    bmi_cat = bmi_category_from_value(bmi)

    return {
        "cycle_irregularity": irregular,
        "hyperandrogenism": hyper,
        "pco_morphology_proxy": pco,
        "rotterdam_count_true": tally,
        "meets_2_of_3_screen": meets,
        "bmi": round(bmi, 1) if bmi else 0.0,
        "bmi_category": bmi_cat,
        "note": "Educational only — not a diagnosis. See a clinician for proper evaluation."
    }

# --- Chapter 5: Input loops, validation, and a session loop ---

def ask_yes_no(prompt: str) -> bool:
    """Loop until user answers y/n. Returns True for yes, False for no."""
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type 'y' or 'n'.")

def ask_float(prompt: str, min_val: float | None = None, max_val: float | None = None) -> float:
    """Loop until a valid float within optional bounds is entered."""
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            val = float(raw)
            if (min_val is not None and val < min_val):
                print(f"Value must be ≥ {min_val}. Try again.")
                continue
            if (max_val is not None and val > max_val):
                print(f"Value must be ≤ {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("Please enter a number (e.g., 28 or 28.5).")

def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Loop until a valid int within optional bounds is entered."""
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            val = int(raw)
            if (min_val is not None and val < min_val):
                print(f"Value must be ≥ {min_val}. Try again.")
                continue
            if (max_val is not None and val > max_val):
                print(f"Value must be ≤ {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("Please enter a whole number (e.g., 10, 12).")

def print_result(result: dict) -> None:
    print("\n=== PCOS Screening Result ===")
    print(f"- Cycle irregularity flag : {result['cycle_irregularity']}")
    print(f"- Hyperandrogenism flag   : {result['hyperandrogenism']}")
    print(f"- PCO morphology proxy    : {result['pco_morphology_proxy']}")
    print(f"- Rotterdam tally (0–3)   : {result['rotterdam_count_true']}")
    print(f"- Meets 2 of 3?           : {result['meets_2_of_3_screen']}")
    print(f"- BMI                     : {result['bmi']} ({result['bmi_category']})")
    print(f"- Note                    : {result['note']}")
    print("==============================\n")

def run_once():
    print("\n--- New Screening ---")
    avg_cycle = ask_float("Average cycle length in days", min_val=10, max_val=120)
    cycles_yr = ask_int("Estimated cycles per year", min_val=0, max_val=24)

    print("\nClinical signs (answer y/n)")
    hirsutism = ask_yes_no("Hirsutism (unwanted coarse hair growth)?")
    acne = ask_yes_no("Persistent acne?")
    thinning = ask_yes_no("Hair thinning?")

    print("\nOvarian morphology proxies (answer y/n if known)")
    pco_u_s = ask_yes_no("Ultrasound previously reported polycystic ovaries?")
    amh_high = ask_yes_no("Known high AMH?")

    print("\nAnthropometrics")
    weight = ask_float("Weight (kg)", min_val=20, max_val=300)
    height = ask_float("Height (meters, e.g., 1.54)", min_val=1.0, max_val=2.5)

    result = pcos_screen(
        avg_cycle_len_days=avg_cycle,
        cycles_per_year=cycles_yr,
        hirsutism=hirsutism,
        acne=acne,
        hair_thinning=thinning,
        known_pc_ovaries=pco_u_s,
        amh_high=amh_high,
        weight_kg=weight,
        height_m=height
    )
    print_result(result)

def main():
    print("PCOS Screening CLI — Chapter 5 Loops\n(educational practice only)\n")
    # Session loop: keep running new screenings until user quits
    while True:
        run_once()
        if not ask_yes_no("Run another screening"):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
