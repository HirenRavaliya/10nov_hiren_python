# Grade Management System Mini Project

def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

def add_student():
    name = input("Enter student name: ")
    marks = int(input("Enter marks (0-100): "))
    grade = calculate_grade(marks)
    students[name] = marks
    print("Student added successfully!")
    print("Grade:", grade)

def display_students():
    if len(students) == 0:
        print("No student records found.")
    else:
        print("\nStudent Records:")
        for name, marks in students.items():
            grade = calculate_grade(marks)
            print(name, "-> Marks:", marks, "| Grade:", grade)

def main_menu():
    print("\n--- Grade Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Exit")

students = {}

while True:
    main_menu()
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        add_student()
    elif choice == "2":
        display_students()
    elif choice == "3":
        print("Exiting program. Thank you!")
        break
    else:
        print("Invalid choice. Please try again.")
