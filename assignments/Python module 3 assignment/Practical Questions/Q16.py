# Practical Question 16: Show hierarchical inheritance
class Parent:
    def show(self):
        print("Parent class")

class Child1(Parent):
    pass

class Child2(Parent):
    pass

Child1().show()
Child2().show()
