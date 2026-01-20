# Practical Question 13: Show single inheritance
class Parent:
    def display(self):
        print("Parent class")

class Child(Parent):
    pass

obj = Child()
obj.display()
