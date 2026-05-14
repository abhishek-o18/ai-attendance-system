# AI-Based Smart Attendance Management System

A complete AI-powered Attendance Management System built with Django that enables teachers to manage attendance using manual, biometric, and real-time face recognition methods. The system integrates DeepFace and OpenCV for automated attendance marking through webcam-based face verification, along with role-based authentication for Admins, Teachers, and Students.

---

# Features

## Authentication & Role-Based Access
- Secure login and logout functionality
- Role-based authentication system
- Admin, Teacher, and Student dashboards
- Session-based authentication using Django
- Password hashing and security using Django authentication system

---

# Admin Module
- Admin dashboard with statistics
- Add, edit, and delete teachers
- Add, edit, and delete students
- Add, edit, and delete classes
- Add, edit, and delete subjects
- Assign teachers to classes
- View attendance reports and records
- Manage student details and attendance history

---

# Teacher Module
- Teacher dashboard with assigned classes
- Manual attendance marking
- Real-time face recognition attendance
- View and update attendance records
- Attendance history with filters
- One-click webcam attendance system

---

# Student Module
- Student login system
- View personal attendance history
- Attendance percentage tracking
- Dashboard with recent attendance records

---

# AI Face Recognition Attendance
- Real-time face detection using OpenCV
- Face verification using DeepFace
- Webcam-based attendance marking
- Automatic attendance storage in SQLite database
- Duplicate attendance prevention logic
- Auto-stop camera after fixed duration
- ESC-based manual camera stop
- Student face dataset stored locally for recognition
- Automatic attendance matching using student ID

---

# Biometric Attendance Support
- Biometric machine integration endpoint
- API-based attendance receiving system
- Biometric attendance storage in database
- Support for machine-generated attendance records

---

# Attendance Logic
- One attendance entry per student per class per day
- Prevents duplicate attendance entries
- Automatically calculates attendance records
- Stores attendance with proper database relationships
- Supports manual, biometric, and face recognition attendance

---

# Frontend
- Responsive UI using Bootstrap 5
- Mobile-friendly design
- Interactive dashboard
- Attendance tables and reports
- Face attendance trigger button for teachers

---

# Tech Stack

- **Backend:** Django 4.2+
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** SQLite
- **Programming Language:** Python
- **AI / Face Recognition:** DeepFace, OpenCV
- **Authentication:** Django Authentication System
- **Version Control:** Git & GitHub

---

# Project Structure

```bash
attendance_system/
├── accounts/              # Authentication and role management
├── teachers/              # Teacher management app
├── students/              # Student management app
├── attendance/            # Attendance management app
├── admin_panel/           # Admin functionality
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── faces/                 # Stored student face dataset
├── capture_faces.py       # Face capture utility script
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── attendance_system/     # Main project settings
```

---

# Installation & Setup

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Webcam for face recognition attendance

---

# Step 1: Clone the Repository

```bash
git clone <repository-url>
cd attendance_system
```

---

# Step 2: Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If DeepFace dependencies are missing:

```bash
pip install deepface opencv-python tf-keras
```

---

# Step 4: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

---

# Step 6: Run Development Server

```bash
python manage.py runserver
```

Application will run at:

```bash
http://127.0.0.1:8000/
```

---

# How Face Recognition Attendance Works

1. Teacher logs into the system
2. Teacher selects class and attendance date
3. Teacher clicks "Start Face Attendance"
4. Webcam opens using OpenCV
5. DeepFace verifies faces against stored dataset
6. Recognized student attendance is automatically marked
7. Attendance is stored in SQLite database
8. Duplicate attendance entries are prevented
9. Camera automatically closes after fixed duration or by pressing ESC

---

# How to Store Student Faces

Run the face capture script:

```bash
python capture_faces.py
```

Enter the student ID when prompted.

Example:

```bash
S001
```

The system stores the image inside:

```bash
faces/S001.jpg
```

The image filename must match the student's `student_id` in the database.

---

# Database Models

## User Model
- Role-based authentication
- Admin / Teacher / Student roles
- Secure password handling

## Teacher Model
- Linked with User model
- Assigned classes
- Department information

## Student Model
- Student ID
- Biometric ID
- Personal details
- Enrolled class

## Attendance Model
- Student relation
- Class relation
- Date and attendance status
- Attendance source tracking
- Marked by teacher information

---

# Security Features

- Password hashing
- CSRF protection
- Session-based authentication
- Role-based authorization
- Duplicate attendance prevention
- Protected attendance routes

---

# Attendance Types Supported

| Attendance Type | Status |
|----------------|--------|
| Manual Attendance | ✅ |
| Face Recognition Attendance | ✅ |
| Biometric Attendance | ✅ |

---

# Usage Guide

## Admin

1. Login with admin credentials
2. Add teachers, classes, and subjects
3. Add students and assign classes
4. View attendance reports and records

---

## Teacher

1. Login with teacher credentials
2. Open assigned class attendance page
3. Mark attendance manually OR use face attendance
4. Start webcam attendance using face recognition
5. View and update attendance history

---

## Student

1. Login using student credentials
2. View attendance percentage
3. Check attendance history

---

# Screenshots

Add screenshots of:
- Login page
- Admin dashboard
- Teacher dashboard
- Face recognition attendance
- Attendance history
- Student dashboard

---

# Future Enhancements

- Browser-based webcam attendance
- Cloud deployment support
- Mobile compatibility
- Attendance analytics dashboard
- PDF/Excel attendance export
- Live attendance tracking
- Advanced AI recognition models
- Multi-face attendance detection

---

# Troubleshooting

## Migration Errors

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Static Files Issue

```bash
python manage.py collectstatic
```

---

## Port Already in Use

```bash
python manage.py runserver 8001
```

---

## DeepFace Import Error

```bash
pip install deepface tf-keras
```

---

# License

This project is created for educational and learning purposes.

---

## Contact

For queries or issues, please contact the development team.

#Student Login Info

What you need to do now
Create migrations and migrate (because models changed: User and Student):
   python manage.py makemigrations accounts students   python manage.py migrate
Add new students via Admin panel (recommended way)
Login as Admin.
Go to Admin → Students → Add Student.
Fill student details and submit.
The system will automatically:
Create a User with:
Username = student ID
Password = student ID
Role = Student
Link it to the Student record.
Student login flow
Go to the same login page (/login/).
Enter:
Username = student_id
Password = student_id (initially, you can change later via Django admin if needed).
After login:
Student is redirected to Student Dashboard showing:
Basic info
Recent attendance
Attendance percentage
In navbar, student sees “My Attendance” link, which opens the full attendance history page (students:detail).
This gives you a clean, role-based student login where each student can securely see only their own attendance marked by teachers.

---

# Developer

Developed by Abhishek Gupta.

