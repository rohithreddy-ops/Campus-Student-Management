"""
main.py
--------
Entry point for the Student Management module.
Handles the console menu loop and user input/output.
All actual data logic lives in student.py — this file
is intentionally "thin".
"""

from database import initialize_database
import student


def print_menu():
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")


def print_student_row(row):
    student_id, name, roll_number, department, year, email = row
    print(f"ID: {student_id} | Name: {name} | Roll: {roll_number} | "
          f"Dept: {department} | Year: {year} | Email: {email}")


def add_student_flow():
    print("\n-- Add New Student --")
    name = input("Name: ").strip()
    roll_number = input("Roll Number: ").strip()
    department = input("Department: ").strip()
    year = input("Year (1-4): ").strip()
    email = input("Email (optional): ").strip()

    if not name or not roll_number or not department or not year:
        print("Error: Name, Roll Number, Department, and Year are required.")
        return

    success, message = student.add_student(name, roll_number, department, int(year), email)
    print(message)


def view_all_flow():
    print("\n-- All Students --")
    rows = student.get_all_students()
    if not rows:
        print("No students found.")
        return
    for row in rows:
        print_student_row(row)


def search_flow():
    keyword = input("\nEnter name or roll number to search: ").strip()
    rows = student.search_students(keyword)
    if not rows:
        print("No matching students found.")
        return
    for row in rows:
        print_student_row(row)


def update_flow():
    student_id = input("\nEnter Student ID to update: ").strip()
    if not student_id.isdigit():
        print("Invalid ID.")
        return

    existing = student.get_student_by_id(int(student_id))
    if not existing:
        print(f"No student found with ID {student_id}.")
        return

    print("Leave a field blank to keep its current value.")
    name = input(f"Name [{existing[1]}]: ").strip()
    department = input(f"Department [{existing[3]}]: ").strip()
    year = input(f"Year [{existing[4]}]: ").strip()
    email = input(f"Email [{existing[5]}]: ").strip()

    success, message = student.update_student(
        int(student_id),
        name=name or None,
        department=department or None,
        year=int(year) if year else None,
        email=email or None
    )
    print(message)


def delete_flow():
    student_id = input("\nEnter Student ID to delete: ").strip()
    if not student_id.isdigit():
        print("Invalid ID.")
        return
    success, message = student.delete_student(int(student_id))
    print(message)


def main():
    initialize_database()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student_flow()
        elif choice == "2":
            view_all_flow()
        elif choice == "3":
            search_flow()
        elif choice == "4":
            update_flow()
        elif choice == "5":
            delete_flow()
        elif choice == "6":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
