# Setup Guide - Online Attendance Management System

This guide will help you set up and run the Attendance Management System on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- A code editor (VS Code, PyCharm, etc.)

## Step-by-Step Setup

### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd path/to/attendance_system
```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Django (web framework)
- Pillow (image processing library)

### Step 4: Run Database Migrations

Django uses migrations to create database tables. Run these commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database file (`db.sqlite3`) and all necessary tables.

### Step 5: Create Admin Account

Create a superuser (admin) account:

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: (enter a username, e.g., `admin`)
- Email: (optional, press Enter to skip)
- Password: (enter a secure password, e.g., `admin123`)
- Password confirmation: (re-enter the password)

### Step 6: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 7: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

You should see the login page.

## Initial Setup After First Login

### As Admin:

1. **Login** with your superuser credentials

2. **Add a Subject**:
   - Click on "Admin" → "Subjects" → "Add Subject"
   - Enter Subject Code (e.g., `CS101`)
   - Enter Subject Name (e.g., `Computer Science`)
   - Click "Add Subject"

3. **Add a Teacher**:
   - Click on "Admin" → "Teachers" → "Add Teacher"
   - Fill in:
     - Username (e.g., `teacher1`)
     - Password (e.g., `teacher123`)
     - First Name, Last Name
     - Teacher ID (e.g., `T001`)
     - Department (e.g., `Computer Science`)
   - Click "Add Teacher"

4. **Add a Class**:
   - Click on "Admin" → "Classes" → "Add Class"
   - Enter Class Code (e.g., `CS101-A`)
   - Enter Class Name (e.g., `CS101 Section A`)
   - Select Subject
   - Assign Teacher(s)
   - Enter Room and Schedule (optional)
   - Click "Add Class"

5. **Add Students**:
   - Click on "Admin" → "Students" → "Add Student"
   - Fill in:
     - Student ID (e.g., `S001`)
     - First Name, Last Name
     - Select Enrolled Class
     - Other details (optional)
   - Click "Add Student"

### As Teacher:

1. **Login** with teacher credentials

2. **View Dashboard**:
   - See assigned classes
   - Quick access to attendance features

3. **Mark Attendance**:
   - Click "Mark Attendance"
   - Select Class and Date
   - Click "Load Students"
   - Mark each student as Present/Absent
   - Click "Submit Attendance"

## Common Commands

### Stop the Server
Press `CTRL+C` in the terminal where the server is running.

### Create Additional Users
```bash
python manage.py createsuperuser
```

### Access Django Admin Panel
Navigate to: `http://127.0.0.1:8000/admin/`
Login with superuser credentials.

### Reset Database (if needed)
```bash
# Delete db.sqlite3 file
# Then run migrations again
python manage.py migrate
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

### Issue: "Migration errors"
**Solution**: Delete `db.sqlite3` and migration files in each app's `migrations` folder (except `__init__.py`), then:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Template not found"
**Solution**: Ensure `templates` folder is in the correct location and `TEMPLATES` setting in `settings.py` points to it.

### Issue: "CSRF verification failed"
**Solution**: Make sure `{% csrf_token %}` is included in all forms.

## Project Structure Overview

```
attendance_system/
├── accounts/              # Authentication app
│   ├── models.py         # User model
│   ├── views.py          # Login, logout, dashboard
│   └── urls.py           # URL routing
├── teachers/             # Teacher management
│   └── models.py         # Teacher model
├── students/             # Student management
│   └── models.py         # Student model
├── attendance/           # Attendance marking
│   ├── models.py         # Attendance model
│   └── views.py          # Mark, update, view attendance
├── admin_panel/          # Admin functionality
│   ├── models.py         # Subject, Class models
│   └── views.py          # CRUD operations
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Auth templates
│   ├── admin_panel/      # Admin templates
│   └── attendance/       # Attendance templates
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── attendance_system/    # Main project settings
    ├── settings.py       # Django settings
    └── urls.py           # Main URL configuration
```

## Next Steps

1. Add more teachers, classes, and students
2. Mark attendance for different dates
3. View attendance reports
4. Explore all features

## Support

For issues or questions:
1. Check the README.md file
2. Review Django documentation: https://docs.djangoproject.com/
3. Check error messages in the terminal

## Notes

- The default database is SQLite (file-based, no setup required)
- For production, consider using PostgreSQL or MySQL
- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` for production deployment

Happy coding!

