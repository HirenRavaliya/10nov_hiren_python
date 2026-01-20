# Practical question 19: Show method overloading
class Math:
    def add(self, a=0, b=0):
        print(a + b)

obj = Math()
obj.add(5)
obj.add(5, 10)
