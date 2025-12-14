#custom iterator to iterate over a list of integers
class NumberIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.numbers):
            val = self.numbers[self.index]
            self.index += 1
            return val
        else:
            raise StopIteration

nums = [1, 2, 3, 4]
my_iter = NumberIterator(nums)

for n in my_iter:
    print(n)