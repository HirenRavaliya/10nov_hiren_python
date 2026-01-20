# Practical Question 17: Show hybrid inheritance
class A:
    def showA(self):
        print("A")

class B(A):
    def showB(self):
        print("B")

class C(A):
    def showC(self):
        print("C")

class D(B, C):
    pass

obj = D()
obj.showA()
obj.showB()
obj.showC()
