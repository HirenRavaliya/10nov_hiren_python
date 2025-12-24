#removing elements from a list using pop() and remove().
numbers = [10, 20, 30, 40, 50, 20]

popped_val = numbers.pop() 
print(f"Popped value: {popped_val}")
print("List after pop():", numbers)

numbers.remove(20)
print("List after remove(20):", numbers)