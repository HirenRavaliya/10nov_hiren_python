# Practical Question 11: Create a class and access properties using an object
class Student:
    def __init__(self, name):
        self.name = name

obj = Student("Hiren")
print(obj.name)
