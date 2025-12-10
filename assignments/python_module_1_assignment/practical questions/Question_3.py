# Q3 - Core Python Concepts

#  Lab Task: variables and different data types:
integer_num = 10           # int
float_num = 3.14           # float
string_text = "Python"     # str
list_data = [1, 2, 3]      # list
tuple_data = (4, 5, 6)     # tuple
set_data = {1, 2, 2, 3}    # set (duplicates not allowed)
dict_data = {"a": 1, "b": 2}  # dictionary(to store key value pairs)
bool= True                 #boolean (contains only true or false)

print("Integer:", integer_num)
print("Float:", float_num)
print("String:", string_text)
print("List:", list_data)
print("Tuple:", tuple_data)
print("Set:", set_data)
print("Dictionary:", dict_data)

# Practical Example 1: How does Python code structure work?
def main():
    """Main function to show basic Python program structure."""
    print("\nInside main() function - basic Python structure demo")


# runs when file is executed directly
if __name__ == "__main__":
    main()

    # Practical Example 2: How to create variables in Python
    x = 5
    y = "Hello"
    z = 2.5
    print("\nVariables created:")
    print("x =", x)
    print("y =", y)
    print("z =", z)

    #Practical Example 3: Take user input using input()
    user_name = input("\nEnter your name: ")
    user_age = input("Enter your age: ")
    print("You entered name:", user_name, "and age:", user_age)

    # Practical Example 4: Check variable type using type()
    print("\nType of user_name:", type(user_name))
    print("Type of user_age (string because of input()):", type(user_age))

    # to make  age datatype  as integer:
    user_age_int = int(user_age)
    print("Type of user_age_int after conversion:", type(user_age_int))
