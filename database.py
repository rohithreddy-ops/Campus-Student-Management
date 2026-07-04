"""
database.py
------------
Handles the SQLite database connection and table creation.
Every other module imports get_connection() from here so the
whole project shares ONE database file: campus.db
"""

import sqlite3

DB_NAME = "campus.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Also enables foreign key support (useful once we add
    attendance/results tables in later modules that reference
    student IDs).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """
    Creates the 'students' table if it doesn't already exist.
    Called once when the program starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            roll_number  TEXT NOT NULL UNIQUE,
            department   TEXT NOT NULL,
            year         INTEGER NOT NULL,
            email        TEXT
        )
    """)

    conn.commit()
    conn.close()
