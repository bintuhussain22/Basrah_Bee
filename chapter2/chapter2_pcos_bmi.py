#BMI Calculator for PCOS: 

weight= input('Enter Your Weight in Kg:')
height= input ('Enter Your Height in Metres:')

weight = float(weight)
height = float(height)

BMI = (weight/(height)**2)

print("Your BMI is:", round(BMI,1))