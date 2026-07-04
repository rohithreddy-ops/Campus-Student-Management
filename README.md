# 🎓 Smart Campus Management System

A console-based Student Management System developed using **Python** and **SQLite**. The application helps manage student records with features such as adding, updating, searching, deleting, and exporting student information.

##  Features

- Add new students
- View all student records
- Search students by name or roll number
- Search students by department
- Search students by year
- Update student information
- Delete student records
- Input validation
- Student statistics
- Export student records to CSV
- SQLite database integration

##  Technologies Used

- Python 3
- SQLite3
- CSV Module
- Regular Expressions (Regex)

##  Project Structure

```
Smart_Campus_Management_System/
│
├── main.py
├── student.py
├── database.py
├── validators.py
├── README.md
├── LICENSE
└── .gitignore
```

##  Database

The project uses SQLite as the backend database.

Table: **students**

Fields:

- Student ID
- Name
- Roll Number
- Department
- Year
- Gender
- Phone Number
- Email
- Date of Birth
- CGPA

##  How to Run

1. Clone the repository

```bash
git clone https://github.com/rohithreddy-ops/Campus-Student-Management.git
```

2. Move into the project folder

```bash
cd Campus-Student-Management
```

3. Run the program

```bash
python main.py
```

##  Menu

```
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Search by Department
7. Search by Year
8. Student Statistics
9. Export to CSV
10. Exit
```

##  Future Improvements

- Student Login
- Faculty Login
- Attendance Management
- Marks Management
- Report Generation
- Flask Web Interface
- Dashboard
- Password Authentication

## Sample Output

```
===== SMART CAMPUS MANAGEMENT SYSTEM =====

1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Search by Department
7. Search by Year
8. Student Statistics
9. Export to CSV
10. Exit
```

## Author

**Rohith Reddy**

GitHub:
https://github.com/rohithreddy-ops

---

If you found this project useful, consider giving it a ⭐ on GitHub.