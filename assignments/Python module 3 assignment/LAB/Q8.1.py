#Method Overloading
class Math:
    def add(self, a=0, b=0):
        return a + b

obj = Math()
print(obj.add(5))
print(obj.add(5, 10))
