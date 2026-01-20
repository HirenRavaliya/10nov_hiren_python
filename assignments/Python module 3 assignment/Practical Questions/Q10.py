# Practical Question 10: Print custom exceptions
try:
    age = int(input("Enter age: "))
    if age < 18:
        raise Exception("Sorry you cannot vote!")
    else:
        print("Elidigible for voting")
except Exception as e:
    print(e)
