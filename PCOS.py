# Ovulation Predictor Based on Cycle Lengths
# Author : Basrah 
# Date : July 2025 

# Open and read CSV file 
filename = "menstrual_cycle_log.csv"

try:
    with open(filename, "r") as file:
        lines = file.readlines()

    # Remove header 
    data = lines[1:]

    menstrual_cycle_lengths = []
    months = []

    for line in data:
        line = line.strip()
        if line == "":
            continue
        month, length = line.split(",")
        months.append(month)
        menstrual_cycle_lengths.append(float(length))

    # Calculate average cycle length
    total = sum(menstrual_cycle_lengths)
    count = len(menstrual_cycle_lengths)
    average_cycle = total / count

    # Predict ovulation: ~14 days before next period 
    predicted_ovulation = average_cycle - 14

    # Measure cycle variability
    max_cycle = max(menstrual_cycle_lengths)
    min_cycle = min(menstrual_cycle_lengths)
    variability = max_cycle - min_cycle

    print("\n📅 Menstrual Cycle Report (Last", count, "Months)")
    print("-" * 40)
    print("Average Cycle Length: {:.1f} days".format(average_cycle))
    print("Predicted Ovulation (avg): Day {:.0f}".format(predicted_ovulation))
    print("Shortest Cycle: {:.0f} days ({})".format(min_cycle, months[menstrual_cycle_lengths.index(min_cycle)]))
    print("Longest Cycle: {:.0f} days ({})".format(max_cycle, months[menstrual_cycle_lengths.index(max_cycle)]))
    print("Cycle Variability: {:.1f} days".format(variability))

    # Basic Interpretation
    if average_cycle < 21 or average_cycle > 35:
        print("\n⚠️ Note: Your average cycle length is outside the typical 21–35 day range.")
    if variability >= 10:
        print("⚠️ Your cycles vary widely. Ovulation may be unpredictable.")

    print("\n✅ Tip: Ovulation usually occurs ~14 days before your next period. Consider using LH strips or BBT for more accuracy.\n")

except FileNotFoundError:
    print("❌ Error: File 'menstrual_cycle_log.csv' not found. Please make sure it exists in the same folder.")
except Exception as e:
    print("❌ An error occurred:", str(e))