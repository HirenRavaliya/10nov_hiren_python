# Q9 - String Manipulation

# Lab Task 1: String slicing demonstration
demo_str = "Python Programming"

print("Original string:", demo_str)
print("Slice [0:6]     :", demo_str[0:6])    # 'Python'
print("Slice [7:]      :", demo_str[7:])     # 'Programming'
print("Slice [::2]     :", demo_str[::2])    # characters at even indices
print("Slice [-5:]     :", demo_str[-5:])    # last 5 characters

# Lab Task 2: Using various string methods
text = "   hello world from PYTHON   "

print("\nOriginal text with spaces:", repr(text))
print("strip()        :", repr(text.strip()))
print("upper()        :", text.upper())
print("lower()        :", text.lower())
print("title()        :", text.title())
print("replace()      :", text.replace("world", "everyone"))
print("split()        :", text.split())  # split by spaces
print("count('o')     :", text.count("o"))
print("startswith('   h'):", text.startswith("   h"))
print("endswith('ON   '):", text.endswith("ON   "))
