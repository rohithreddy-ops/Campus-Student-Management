"""
validators.py
--------------
Standalone input-validation functions. Kept separate from
student.py and main.py because validation rules are pure logic
with no database or I/O involvement — easy to unit test on
their own, and reusable later by auth.py, results.py, etc.

Each function returns (is_valid: bool, error_message: str).
An empty error_message means the input is valid.
"""

import re

EMAIL_PATTERN = re.compile(r"^[\w\.\+-]+@[\w-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")  # 10-digit Indian mobile format


def validate_email(email):
    """Email is optional — blank is allowed. If provided, must match pattern."""
    if not email:
        return True, ""
    if EMAIL_PATTERN.match(email):
        return True, ""
    return False, "Invalid email format (expected e.g. name@example.com)."


def validate_phone(phone):
    """Phone is optional — blank is allowed. If provided, must be 10 digits, starting 6-9."""
    if not phone:
        return True, ""
    if PHONE_PATTERN.match(phone):
        return True, ""
    return False, "Invalid phone number (expected 10 digits, starting with 6-9)."


def validate_cgpa(cgpa_str):
    """
    CGPA is optional — blank is allowed. If provided, must be a number
    between 0.0 and 10.0 inclusive.
    Returns (is_valid, error_message, parsed_value_or_None).
    """
    if not cgpa_str:
        return True, "", None
    try:
        value = float(cgpa_str)
    except ValueError:
        return False, "CGPA must be a number (e.g. 8.5).", None

    if 0.0 <= value <= 10.0:
        return True, "", value
    return False, "CGPA must be between 0.0 and 10.0.", None


def validate_year(year_str):
    """Year must be an integer between 1 and 4."""
    if not year_str.isdigit():
        return False, "Year must be a number (1-4).", None
    value = int(year_str)
    if 1 <= value <= 4:
        return True, "", value
    return False, "Year must be between 1 and 4.", None
