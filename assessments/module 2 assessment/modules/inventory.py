from modules import data
from modules.utilities import get_valid_number, print_separator

def view_inventory():
    print("\n--- CURRENT INVENTORY ---")
    print(f"{'MEDICINE NAME':<20} | {'PRICE (INR)':<12} | {'QUANTITY':<10}")
    print_separator()
    
    if not data.inventory:
        print("Inventory is empty.")
    else:
        for name, details in data.inventory.items():
            print(f"{name:<20} | {details['price']:<12.2f} | {details['qty']:<10}")
    print_separator()

def add_update_medicine():
    print("\n--- ADD / UPDATE MEDICINE ---")
    name = input("Enter Medicine Name: ").strip()
    
    if not name:
        print("Error: Medicine name cannot be empty.")
        return

    price = get_valid_number("Enter Price per unit: ", float)
    qty = get_valid_number("Enter Quantity to add: ", int)

    if name in data.inventory:
        data.inventory[name]['qty'] += qty
        data.inventory[name]['price'] = price
        print(f"Success: Stock updated for '{name}'. New Qty: {data.inventory[name]['qty']}")
    else:
        data.inventory[name] = {'price': price, 'qty': qty}
        print(f"Success: '{name}' added to inventory.")