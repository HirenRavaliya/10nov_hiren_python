#check  blood donation eligibility
age = int(input("enter age"))
weight = int(input("enter wieght: "))

if age >= 18:
    if weight >= 50:
        print("You are eligible to donate blood.")
    else:
        print("You are not eligible: Weight must be at least 50kg.")
else:
    print("You are not eligible: You must be at least 18 years old.")