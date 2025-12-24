
def get_valid_number(prompt, data_type=int):
    
    while True:
        try:
            value = data_type(input(prompt))
            if value < 0:
                print("Error: Please enter a positive value.")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {'number' if data_type is float else 'integer'}.")

def print_separator(char='-', length=50):
    print(char * length)