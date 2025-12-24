#create a calculator using functions
def add(x, y): return x + y
def subtract(x, y): return x - y
def multiply(x, y): return x * y
def divide(x, y):
   

 print("select operation: 1.Add 2.Subtract 3.Multiply 4.Divide")
choice = input("enter choice(1/2/3/4): ")
n1 = float(input("enter first number: "))
n2 = float(input("enter second number: "))

if choice == '1': print("result:", add(n1, n2))
elif choice == '2': print("result:", subtract(n1, n2))
elif choice == '3': print("result:", multiply(n1, n2))
elif choice == '4': print("result:", divide(n1, n2))
else: print("invalid input")