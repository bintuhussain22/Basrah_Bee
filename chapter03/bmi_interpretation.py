# chapter3/bmi_interpretation.py
# 🌸 PCOS BMI Calculator with Interpretation & Tips

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))

# Calculate BMI
bmi = weight / (height ** 2)
bmi = round(bmi, 1)

print("\nYour BMI is:", bmi)

# Interpret the result using conditionals (Chapter 3 skill)
if bmi < 18.5:
    print("Category: Underweight 🟠")
    print("➡️ Being underweight may affect ovulation and hormone balance.")
    print("💡 Tip: Focus on nutrient-dense meals and strength training.")
elif bmi < 25:
    print("Category: Normal weight 🟢")
    print("✅ Supports balanced hormones and regular cycles.")
    print("💡 Tip: Maintain weight with balanced diet, activity, and good sleep.")
elif bmi < 30:
    print("Category: Overweight 🔴")
    print("⚠️ Higher BMI may contribute to irregular cycles and insulin resistance.")
    print("💡 Tip: Even 5–10% weight loss can improve ovulation and fertility.")
else:
    print("Category: Obese ❌")
    print("❗ Linked to more severe PCOS symptoms and metabolic risks.")
    print("💡 Tip: Start small — gradual changes in diet and activity can help.")