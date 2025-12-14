#calculating grades based on percentage
percentage = int(input("enter percentage: "))

if percentage >= 90:
    grade = 'A'
elif percentage >= 80:
    grade = 'B'
elif percentage >= 70:
    grade = 'C'
elif percentage >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Percentage: {percentage}%, Grade: {grade}")