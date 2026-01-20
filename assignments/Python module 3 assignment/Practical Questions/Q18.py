# Practical Question 18: Demonstrate use of super() in inheritance
class Parent:
    def __init__(self):
        print("Parent constructor")

class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child constructor")

Child()
