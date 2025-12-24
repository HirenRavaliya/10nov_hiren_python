import datetime
from modules import data
from modules.utilities import get_valid_number, print_separator

def process_sale():
    
    print("\n--- NEW SALE ENTRY ---")
    customer_name = input("Enter Customer Name: ").strip()
    med_name = input("Enter Medicine Name: ").strip()

    if med_name not in data.inventory:
        print(f"Error: Medicine '{med_name}' not found in inventory.")
        return

    available_qty = data.inventory[med_name]['qty']
    qty = get_valid_number(f"Enter Quantity (Available: {available_qty}): ", int)

    if qty > available_qty:
        print(f"Error: Insufficient stock! Only {available_qty} units available.")
        return
    
    if qty == 0:
        print("Sale cancelled (Quantity is 0).")
        return

    price_per_unit = data.inventory[med_name]['price']
    total_cost = price_per_unit * qty
    
    data.inventory[med_name]['qty'] -= qty

    sale_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sale_record = {
        "date": sale_date,
        "customer": customer_name,
        "medicine": med_name,
        "qty": qty,
        "total": total_cost
    }
    data.sales_history.append(sale_record)

    print("=====Meditrack Pharmacy Receipt=====")

    print(f"Date      : {sale_date}")
    print(f"Customer  : {customer_name}")
    
    print(f"Item      : {med_name}")
    print(f"Quantity  : {qty}")
    print(f"Price/Unit: {price_per_unit:.2f}")
    
    print(f"TOTAL AMOUNT : INR {total_cost:.2f}")
    