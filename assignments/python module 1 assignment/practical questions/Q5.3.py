#search string inside the list
list1 = ['apple', 'banana', 'mango']
target = str(input("enter string to search: "))
found = False

for fruit in list1:
    if fruit == target:
        found = True
        break

if found:
    print(f"Found {target} in the list.")
else:
    print(f"{target} not found.")