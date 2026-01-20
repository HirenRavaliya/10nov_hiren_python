# Practical Question 9: Handle file exceptions and use finally block
try:
    file = open("test.txt", "r")
    print(file.read())
except FileNotFoundError:
    print("File not found")
finally:
    print("Program ended")
