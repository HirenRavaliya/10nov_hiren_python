#Even Number Generator
def even_generator():
    num = 0
    count = 0
    while count < 10:
        if num % 2 == 0:
            yield num
            count += 1
        num += 1

print("First 10 even numbers:")
for n in even_generator():
    print(n, end=" ")