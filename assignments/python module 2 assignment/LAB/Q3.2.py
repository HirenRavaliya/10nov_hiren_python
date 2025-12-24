#sorting a list using both sort() and sorted()
numbers_a = [5, 2, 9, 1, 5, 6]
numbers_b = [5, 2, 9, 1, 5, 6]

# sorted() 
sorted_list = sorted(numbers_a)
print("Original List A:", numbers_a)
print("New list from sorted():", sorted_list)

# sort() 
numbers_b.sort()
print("List B after .sort():", numbers_b)