"""
main.py
--------
Console interface for the Student Management module.
Handles menus and user input/output only — all data logic
lives in student.py, all input-format checks live in validators.py.
"""

from database import initialize_database
import student
import validators


def print_menu():
    print("\n===== CAMPUS STUDENT MANAGEMENT SYSTEM =====")
    print(" 1. Add Student")
    print(" 2. View All Students")
    print(" 3. Search by Name")
    print(" 4. Search by Roll Number")
    print(" 5. Search by Department")
    print(" 6. Search by Year")
    print(" 7. Update Student")
    print(" 8. Delete Student")
    print(" 9. Student Statistics")
    print("10. Export Student Records to CSV")
    print("11. Exit")


def print_student_row(row):
    student_id, name, roll_number, department, year, email, phone, cgpa = row
    cgpa_display = cgpa if cgpa is not None else "N/A"
    print(f"ID: {student_id} | Name: {name} | Roll: {roll_number} | "
          f"Dept: {department} | Year: {year} | Email: {email or 'N/A'} | "
          f"Phone: {phone or 'N/A'} | CGPA: {cgpa_display}")


def print_rows_or_none(rows):
    if not rows:
        print("No matching students found.")
        return
    for row in rows:
        print_student_row(row)


# ---------------------------------------------------------------
# FLOWS
# ---------------------------------------------------------------

def add_student_flow():
    print("\n-- Add New Student --")
    name = input("Name: ").strip()
    roll_number = input("Roll Number: ").strip()
    department = input("Department: ").strip()
    year_str = input("Year (1-4): ").strip()
    email = input("Email (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    cgpa_str = input("CGPA (optional, 0-10): ").strip()

    if not name or not roll_number or not department:
        print("Error: Name, Roll Number, and Department are required.")
        return

    year_ok, year_err, year_val = validators.validate_year(year_str)
    if not year_ok:
        print(f"Error: {year_err}")
        return

    email_ok, email_err = validators.validate_email(email)
    if not email_ok:
        print(f"Error: {email_err}")
        return

    phone_ok, phone_err = validators.validate_phone(phone)
    if not phone_ok:
        print(f"Error: {phone_err}")
        return

    cgpa_ok, cgpa_err, cgpa_val = validators.validate_cgpa(cgpa_str)
    if not cgpa_ok:
        print(f"Error: {cgpa_err}")
        return

    success, message = student.add_student(
        name, roll_number, department, year_val,
        email=email or None, phone=phone or None, cgpa=cgpa_val
    )
    print(message)


def view_all_flow():
    print("\n-- All Students --")
    print_rows_or_none(student.get_all_students())


def search_by_name_flow():
    name = input("\nEnter name (partial ok): ").strip()
    print_rows_or_none(student.search_by_name(name))


def search_by_roll_flow():
    roll = input("\nEnter exact roll number: ").strip()
    print_rows_or_none(student.search_by_roll_number(roll))


def search_by_department_flow():
    dept = input("\nEnter department: ").strip()
    print_rows_or_none(student.search_by_department(dept))


def search_by_year_flow():
    year_str = input("\nEnter year (1-4): ").strip()
    year_ok, year_err, year_val = validators.validate_year(year_str)
    if not year_ok:
        print(f"Error: {year_err}")
        return
    print_rows_or_none(student.search_by_year(year_val))


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
    year_str = input(f"Year [{existing[4]}]: ").strip()
    email = input(f"Email [{existing[5] or ''}]: ").strip()
    phone = input(f"Phone [{existing[6] or ''}]: ").strip()
    cgpa_str = input(f"CGPA [{existing[7] if existing[7] is not None else ''}]: ").strip()

    year_val = None
    if year_str:
        year_ok, year_err, year_val = validators.validate_year(year_str)
        if not year_ok:
            print(f"Error: {year_err}")
            return

    if email:
        email_ok, email_err = validators.validate_email(email)
        if not email_ok:
            print(f"Error: {email_err}")
            return

    if phone:
        phone_ok, phone_err = validators.validate_phone(phone)
        if not phone_ok:
            print(f"Error: {phone_err}")
            return

    cgpa_val = None
    if cgpa_str:
        cgpa_ok, cgpa_err, cgpa_val = validators.validate_cgpa(cgpa_str)
        if not cgpa_ok:
            print(f"Error: {cgpa_err}")
            return

    success, message = student.update_student(
        int(student_id),
        name=name or None,
        department=department or None,
        year=year_val,
        email=email or None,
        phone=phone or None,
        cgpa=cgpa_val
    )
    print(message)


def delete_flow():
    student_id = input("\nEnter Student ID to delete: ").strip()
    if not student_id.isdigit():
        print("Invalid ID.")
        return
    success, message = student.delete_student(int(student_id))
    print(message)


def statistics_flow():
    print("\n-- Student Statistics --")
    stats = student.get_statistics()
    print(f"Total Students: {stats['total_students']}")

    print("\nBy Department:")
    if stats["by_department"]:
        for dept, count in stats["by_department"].items():
            print(f"  {dept}: {count}")
    else:
        print("  No data.")

    print("\nBy Year:")
    if stats["by_year"]:
        for year, count in stats["by_year"].items():
            print(f"  Year {year}: {count}")
    else:
        print("  No data.")

    avg = stats["average_cgpa"]
    print(f"\nAverage CGPA: {avg if avg is not None else 'N/A'}")

    top = stats["top_student"]
    if top:
        print(f"Top Student: {top[1]} (Roll: {top[2]}, CGPA: {top[7]})")
    else:
        print("Top Student: N/A")


def export_flow():
    filepath = input("\nEnter filename for export [students_export.csv]: ").strip()
    filepath = filepath or "students_export.csv"
    success, message = student.export_to_csv(filepath)
    print(message)


# ---------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------

def main():
    initialize_database()

    actions = {
        "1": add_student_flow,
        "2": view_all_flow,
        "3": search_by_name_flow,
        "4": search_by_roll_flow,
        "5": search_by_department_flow,
        "6": search_by_year_flow,
        "7": update_flow,
        "8": delete_flow,
        "9": statistics_flow,
        "10": export_flow,
    }

    while True:
        print_menu()
        choice = input("Enter your choice (1-11): ").strip()

        if choice == "11":
            print("Exiting Student Management System. Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please enter a number between 1 and 11.")


if __name__ == "__main__":
    main()
