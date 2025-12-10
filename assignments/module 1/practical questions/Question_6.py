# Q6 - Generators and Iterators

# Lab Task 1: Generator for first 10 even numbers
def even_numbers_generator(limit):
   
    num = 2
    while num <= limit:
        yield num
        num += 2


print("First 10 even numbers using generator:")
for even in even_numbers_generator(20):  
    print(even, end=" ")
print()

# Lab Task 2: Custom iterator for list of integers
class IntegerListIterator:
    
    #Custom iterator to iterate over a list of integers.

    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.numbers):
            value = self.numbers[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration


nums = [10, 20, 30, 40, 50]
print("\nIterating over list using custom iterator:")
iterator = IntegerListIterator(nums)
for value in iterator:
    print(value)
