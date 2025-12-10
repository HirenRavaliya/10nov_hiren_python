# Q5 - Looping (for, while)


list1 = ["apple", "banana", "mango"]

# Practical Example 1: Print each fruit
print("All fruits in list:")
for fruit in list1:
    print(fruit)

# Practical Example 2: Length of each string
print("\nLength of each fruit name:")
for fruit in list1:
    print(fruit, "=", len(fruit))

# Practical Example 3: Find specific string in list
target = input("\nEnter fruit name to search in list1: ")

found = False
for fruit in list1:
    if fruit.lower() == target.lower():
        found = True
        break

if found:
    print(target, "found in the list.")
else:
    print(target, "not found in the list.")

# Practical Example 4: Print pattern using nested for loop
print("\nStar pattern:")
rows = 5
for i in range(1, rows + 1):
    # print i stars in each row
    print("*" * i)

# while looop
print("\nWhile loop to iterate untill condition match")
count = 1
while count <= 5:
    print("Count:", count)
    count += 1