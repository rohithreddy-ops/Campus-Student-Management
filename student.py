"""
student.py
-----------
Contains all CRUD (Create, Read, Update, Delete) operations
for the 'students' table. main.py calls these functions;
this file never talks to the user directly (no input()/print()
for prompts) except for displaying results — that keeps logic
and interface separated, which is a clean design habit.
"""

import sqlite3
from database import get_connection


def add_student(name, roll_number, department, year, email):
    """Insert a new student record. Returns (success, message)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (name, roll_number, department, year, email)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_number, department, year, email))
        conn.commit()
        return True, f"Student '{name}' added successfully (ID: {cursor.lastrowid})."
    except sqlite3.IntegrityError:
        return False, f"Error: Roll number '{roll_number}' already exists."
    finally:
        conn.close()


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


def search_students(keyword):
    """Search students by name or roll number (partial match)."""
    conn = get_connection()
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR roll_number LIKE ?
    """, (pattern, pattern))
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_student(student_id, name=None, department=None, year=None, email=None):
    """
    Update one or more fields for a student.
    Only fields that are passed in (not None) get updated —
    this lets main.py support 'leave blank to keep current value'.
    """
    existing = get_student_by_id(student_id)
    if not existing:
        return False, f"No student found with ID {student_id}."

    name = name if name else existing[1]
    department = department if department else existing[3]
    year = year if year else existing[4]
    email = email if email else existing[5]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, department = ?, year = ?, email = ?
        WHERE student_id = ?
    """, (name, department, year, email, student_id))
    conn.commit()
    conn.close()
    return True, f"Student ID {student_id} updated successfully."


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

