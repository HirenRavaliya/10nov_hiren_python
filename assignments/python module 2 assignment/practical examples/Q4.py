#removing elements from a list using pop() and remove()
numbers = [10, 20, 30, 40, 50]

popped_item = numbers.pop()
print(f"Popped item: {popped_item}")
print("List after pop:", numbers)

numbers.remove(20)
print("List after remove(20):", numbers)