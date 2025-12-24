from modules import inventory, sales

def main_menu():
    while True:
        print("\n=== MEDITRACK  APP ===")
        print("1. View Inventory")
        print("2. Add / Update Medicine")
        print("3. Process Sale")
        print("4. Exit")
        
        choice = input("Select Option (1-4): ")

        if choice == '1':
            inventory.view_inventory()
        elif choice == '2':
            inventory.add_update_medicine()
        elif choice == '3':
            sales.process_sale()
        elif choice == '4':
            print("Exiting")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main_menu()