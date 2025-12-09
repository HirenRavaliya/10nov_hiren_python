# Q8 - Control Statements (break, continue, pass)

fruits = ["apple", "banana", "mango", "banana", "orange"]

# Practical Example 1: skip 'banana' using continue
print("Example 1: Skipping 'banana' using continue:")
for fruit in fruits:
    if fruit == "banana":
        continue  # skip the rest of this iteration
    print(fruit)

# Practical Example 2: stop when 'banana' is found using break
print("\nExample 2: Stopping when first 'banana' is found using break:")
for fruit in fruits:
    if fruit == "banana":
        print("Found 'banana', stopping the loop.")
        break
    print(fruit)
