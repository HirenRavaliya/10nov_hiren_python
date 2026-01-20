# Practical Question 8: Handle multiple exceptions
try:
    file = open("unknown.txt", "r")
    print(file.read())
except FileNotFoundError:
    print("File not found")
except ZeroDivisionError:
    print("Division by zero")
