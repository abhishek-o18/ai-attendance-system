# Online Attendance Management System for Teachers

A complete, production-ready web application built with Django that allows teachers to mark attendance of their classes online. The system features role-based authentication (Admin and Teacher), comprehensive admin panel, and intuitive attendance marking interface.

## Features

### Authentication & Roles
- Secure login and logout functionality
- Role-based access control (Admin and Teacher)
- Session-based authentication
- Password hashing using Django's built-in authentication

### Admin Module
- Admin dashboard with statistics
- Add, edit, and delete teachers
- Add, edit, and delete subjects
- Add, edit, and delete classes
- Assign teachers to classes
- Add, edit, and delete students
- View attendance reports (daily, monthly, subject-wise)

### Teacher Module
- Teacher dashboard showing assigned classes
- Select date and class to mark attendance
- Mark students as Present/Absent
- Update attendance if needed
- View attendance history with filters

### Student Management
- Add students to classes
- Unique student ID system
- Student list per class
- Student detail view with attendance statistics

### Attendance Logic
- One attendance entry per class per date
- Prevents duplicate attendance for the same date
- Automatically calculates attendance percentage
- Stores attendance records in database with proper relationships

### Frontend
- Clean and responsive UI using Bootstrap 5
- Mobile-friendly design
- Forms with validation
- Tables for attendance display
- Interactive dashboard

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default, MySQL compatible)
- **Authentication**: Django's built-in authentication system

## Project Structure

```
attendance_system/
├── accounts/          # Authentication app
├── teachers/          # Teacher management app
├── students/          # Student management app
├── attendance/        # Attendance marking app
├── admin_panel/       # Admin functionality app
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── manage.py          # Django management script
└── attendance_system/ # Main project settings
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd attendance_system

# Or extract the project folder
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Login Credentials

After creating a superuser, you can log in with:
- **Username**: (the username you created)
- **Password**: (the password you set)

## Usage Guide

### For Admin:

1. **Login** with admin credentials
2. **Add Teachers**:
   - Go to Admin → Teachers → Add Teacher
   - Fill in teacher details and create account

3. **Add Subjects**:
   - Go to Admin → Subjects → Add Subject
   - Enter subject code and name

4. **Add Classes**:
   - Go to Admin → Classes → Add Class
   - Select subject and assign teachers

5. **Add Students**:
   - Go to Admin → Students → Add Student
   - Assign students to classes

6. **View Reports**:
   - Go to Admin → Reports
   - Filter by date, month, or subject

### For Teachers:

1. **Login** with teacher credentials
2. **View Dashboard**:
   - See assigned classes
   - Quick access to attendance features

3. **Mark Attendance**:
   - Go to Mark Attendance
   - Select class and date
   - Mark students as Present/Absent
   - Submit

4. **View History**:
   - Go to Attendance History
   - Filter by class or date
   - View or update previous attendance

## Database Models

### User Model (Custom)
- Extends Django's AbstractUser
- Role field (admin/teacher)
- Phone number

### Teacher Model
- Linked to User
- Teacher ID (unique)
- Department and qualification

### Subject Model
- Subject code (unique)
- Subject name
- Description

### Class Model
- Class code (unique)
- Class name
- Subject (ForeignKey)
- Teachers (ManyToMany)
- Schedule and room

### Student Model
- Student ID (unique)
- Personal information
- Enrolled class (ForeignKey)

### Attendance Model
- Student (ForeignKey)
- Class (ForeignKey)
- Date
- Status (Present/Absent)
- Marked by (User)
- Unique constraint: (student, class, date)

## How Attendance is Marked and Stored

1. **Teacher selects class and date** from the mark attendance page
2. **System loads all students** enrolled in that class
3. **Teacher marks each student** as Present or Absent using radio buttons
4. **On submission**, the system:
   - Checks if attendance already exists for that class and date
   - Creates attendance records for each student
   - Links each record to the student, class, date, and marking teacher
   - Stores status (present/absent)

5. **Database Storage**:
   - Each attendance record is stored in the `Attendance` table
   - Records are linked via ForeignKeys to Student, Class, and User tables
   - Unique constraint prevents duplicate entries for same student-class-date combination

6. **Update Process**:
   - Teachers can update attendance if needed
   - System updates existing records or creates new ones
   - Tracks who made the update

## Viva Explanation Points

### Architecture
- **MVT Pattern**: Django follows Model-View-Template architecture
- **App-based Structure**: Separate apps for different functionalities
- **Database Relationships**: ForeignKey and ManyToMany relationships properly implemented

### Security
- **Password Hashing**: Django automatically hashes passwords
- **CSRF Protection**: All forms include CSRF tokens
- **Authentication Decorators**: Views protected with `@login_required`
- **Role-based Access**: Checks user role before allowing actions

### Features Implementation
- **Duplicate Prevention**: Unique constraint in Attendance model
- **Data Validation**: Form validation and model validation
- **Error Handling**: Try-except blocks and user-friendly error messages
- **Responsive Design**: Bootstrap 5 for mobile-friendly UI

### Database Design
- **Normalization**: Proper database normalization
- **Indexes**: Indexes on frequently queried fields
- **Relationships**: Proper use of ForeignKey and ManyToMany

## Screenshots

(Add screenshots of key pages here)
- Login Page
- Admin Dashboard
- Teacher Dashboard
- Mark Attendance Page
- Attendance History
- Reports Page

## Future Enhancements

- Export attendance to Excel/PDF
- Attendance analytics with charts
- Email notifications
- SMS integration
- Mobile app
- Biometric integration

## Troubleshooting

### Common Issues

1. **Migration Errors**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic
   ```

3. **Port Already in Use**:
   ```bash
   python manage.py runserver 8001
   ```

## License

This project is created for educational purposes.

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


