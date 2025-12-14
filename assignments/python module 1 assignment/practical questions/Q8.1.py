#skipping 'banana' in a list using the continue statement
list1 = ['apple', 'banana', 'mango']

for fruit in list1:
    if fruit == 'banana':
        continue
    print(fruit)