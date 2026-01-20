# Practical Question 12: Demonstrate local and global variables
x = 10

class Test:
    def show(self):
        x = 5
        print("Local x:", x)

obj = Test()
obj.show()
print("Global x:", x)
