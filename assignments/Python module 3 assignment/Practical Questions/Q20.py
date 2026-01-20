# Practical Question 20: Show method overriding
class Parent:
    def show(self):
        print("Parent method")

class Child(Parent):
    def show(self):
        print("Child method")

Child().show()
