#find greater and less than a number

number1 = input("enter first number1: ")
number2 = input("enter second number1: ")

if number1 > number2:
    print(f"{number1} is greater than {number2}")
elif number1 < number2:
    print(f"{number1} is less than {number2}")
else:
    print(f"{number1} is equal to {number2}")