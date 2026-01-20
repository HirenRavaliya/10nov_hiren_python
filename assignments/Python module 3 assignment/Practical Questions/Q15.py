# Practical Question 15: Show multiple inheritance
class A:
    def showA(self):
        print("Class A")

class B:
    def showB(self):
        print("Class B")

class C(A, B):
    pass

obj = C()
obj.showA()
obj.showB()
