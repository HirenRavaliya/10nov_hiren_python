#Create a class and access its properties
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("Hiren", 22)
print(s1.name)
print(s1.age)
