"""
student.py
-----------
Contains all CRUD operations, targeted search functions,
statistics, and CSV export for the 'students' table.

Row shape (index reference used throughout this file):
0: student_id  1: name  2: roll_number  3: department
4: year        5: email 6: phone        7: cgpa
"""

import sqlite3
import csv
from database import get_connection


# ---------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------

def add_student(name, roll_number, department, year, email=None, phone=None, cgpa=None):
    """Insert a new student record. Returns (success, message)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (name, roll_number, department, year, email, phone, cgpa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, roll_number, department, year, email, phone, cgpa))
        conn.commit()
        return True, f"Student '{name}' added successfully (ID: {cursor.lastrowid})."
    except sqlite3.IntegrityError:
        return False, f"Error: Roll number '{roll_number}' already exists."
    finally:
        conn.close()


# ---------------------------------------------------------------
# READ
# ---------------------------------------------------------------

def get_all_students():
    """Return a list of all student rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY student_id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_student_by_id(student_id):
    """Return a single student row by ID, or None if not found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------
# SEARCH (one focused function per field, plus a general one)
# ---------------------------------------------------------------

def search_students(keyword):
    """General search: matches name OR roll number (partial, case-insensitive)."""
    conn = get_connection()
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ? COLLATE NOCASE OR roll_number LIKE ? COLLATE NOCASE
    """, (pattern, pattern))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_name(name):
    """Partial, case-insensitive match on name only."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ? COLLATE NOCASE", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_roll_number(roll_number):
    """Exact match on roll number (roll numbers are unique, so at most one result)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE roll_number = ? COLLATE NOCASE", (roll_number,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_department(department):
    """Exact, case-insensitive match on department."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE department = ? COLLATE NOCASE", (department,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_year(year):
    """Exact match on year (1-4)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE year = ?", (year,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------

def update_student(student_id, name=None, department=None, year=None,
                    email=None, phone=None, cgpa=None):
    """
    Update one or more fields for a student.
    Only fields passed in (not None) overwrite the existing value —
    this supports "leave blank to keep current value" in the UI.
    Note: to intentionally clear a value, pass an empty string "" rather
    than None (None here specifically means "no change requested").
    """
    existing = get_student_by_id(student_id)
    if not existing:
        return False, f"No student found with ID {student_id}."

    name = name if name is not None else existing[1]
    department = department if department is not None else existing[3]
    year = year if year is not None else existing[4]
    email = email if email is not None else existing[5]
    phone = phone if phone is not None else existing[6]
    cgpa = cgpa if cgpa is not None else existing[7]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, department = ?, year = ?, email = ?, phone = ?, cgpa = ?
        WHERE student_id = ?
    """, (name, department, year, email, phone, cgpa, student_id))
    conn.commit()
    conn.close()
    return True, f"Student ID {student_id} updated successfully."


# ---------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------

def delete_student(student_id):
    """Delete a student record by ID."""
    existing = get_student_by_id(student_id)
    if not existing:
        return False, f"No student found with ID {student_id}."

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return True, f"Student ID {student_id} deleted successfully."


# ---------------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------------

def get_statistics():
    """
    Returns a dictionary summarizing the student data:
    - total_students
    - by_department: {dept: count}
    - by_year: {year: count}
    - average_cgpa (across students who have a CGPA recorded)
    - highest_cgpa_student: row with the max CGPA (or None)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT department, COUNT(*) FROM students GROUP BY department")
    by_department = dict(cursor.fetchall())

    cursor.execute("SELECT year, COUNT(*) FROM students GROUP BY year ORDER BY year")
    by_year = dict(cursor.fetchall())

    cursor.execute("SELECT AVG(cgpa) FROM students WHERE cgpa IS NOT NULL")
    avg_cgpa = cursor.fetchone()[0]

    cursor.execute("""
        SELECT * FROM students
        WHERE cgpa IS NOT NULL
        ORDER BY cgpa DESC LIMIT 1
    """)
    top_student = cursor.fetchone()

    conn.close()

    return {
        "total_students": total,
        "by_department": by_department,
        "by_year": by_year,
        "average_cgpa": round(avg_cgpa, 2) if avg_cgpa is not None else None,
        "top_student": top_student,
    }


# ---------------------------------------------------------------
# EXPORT
# ---------------------------------------------------------------

def export_to_csv(filepath="students_export.csv"):
    """
    Writes all student records to a CSV file.
    Returns (success, message).
    """
    rows = get_all_students()
    if not rows:
        return False, "No student records to export."

    headers = ["student_id", "name", "roll_number", "department", "year", "email", "phone", "cgpa"]

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return True, f"Exported {len(rows)} student record(s) to '{filepath}'."
    except OSError as e:
        return False, f"Failed to write CSV file: {e}"
