# Q4 - Conditional Statements

#Practical Example 5: Find greater and less using if-else
print("find greater and less")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if num1 > num2:
    print("Greater number:", num1)
    print("Smaller number:", num2)
elif num2 > num1:
    print("Greater number:", num2)
    print("Smaller number:", num1)
else:
    print("Both numbers are equal.")

#Practical Example 6: Check if a number is prime
n = int(input("\nEnter a number to check if it is prime: "))

if n <= 1:
    print(n, "is not a prime number.")
else:
    is_prime = True
    # check divisibility from 2 to sqrt(n)
    i = 2
    while i * i <= n:
        if n % i == 0:
            is_prime = False
            break
        i += 1

    if is_prime:
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")

#Practical Example 7: Grade calculation using percentage
print("percentage calculator")
percentage = float(input("\nEnter your percentage: "))

if percentage >= 90:
    grade = "A+"
elif percentage >= 80:
    grade = "A"
elif percentage >= 70:
    grade = "B"
elif percentage >= 60:
    grade = "C"
elif percentage >= 50:
    grade = "D"
else:
    grade = "Fail"

print("Your grade is:", grade)

#Practical Example 8: Blood donation eligibility nested if
print("blood donation eligibility")
age = int(input("\nEnter your age: "))
weight = float(input("Enter your weight (kg): "))

if age >= 18:
    if weight >= 50:
        print("You are eligible to donate blood.")
    else:
        print("You are not eligible to donate blood (weight should be >= 50kg).")
else:
    print("You are not eligible to donate blood (age should be >= 18).")
