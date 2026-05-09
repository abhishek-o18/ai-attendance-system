from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    user = request.user
    
    if user.is_admin_user():
        from teachers.models import Teacher
        from students.models import Student, Class
        from attendance.models import Attendance

        total_teachers = Teacher.objects.count()
        total_classes = Class.objects.count()
        total_students = Student.objects.count()
        total_attendance_records = Attendance.objects.count()
        
        context = {
            'user': user,
            'total_teachers': total_teachers,
            'total_classes': total_classes,
            'total_students': total_students,
            'total_attendance_records': total_attendance_records,
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    
    elif user.is_teacher_user():
        from teachers.models import Teacher
        try:
            teacher = Teacher.objects.get(user=user)
            assigned_classes = teacher.classes.all()
            
            context = {
                'user': user,
                'teacher': teacher,
                'assigned_classes': assigned_classes,
            }
            return render(request, 'accounts/teacher_dashboard.html', context)
        except Teacher.DoesNotExist:
            messages.warning(request, 'Teacher profile not found. Please contact admin.')
            return render(request, 'accounts/teacher_dashboard.html', {'user': user})
    
    elif user.is_student_user():
        from students.models import Student
        from attendance.models import Attendance

        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            messages.warning(request, 'Student profile not found. Please contact admin.')
            return render(request, 'accounts/dashboard.html', {'user': user})

        # Full queryset (no slicing here)
        attendance_qs = Attendance.objects.filter(student=student)

        # Last 30 records only for display
        attendance_records = attendance_qs.order_by('-date')[:30]

        # Statistics from full queryset
        total_days = attendance_qs.count()
        present_days = attendance_qs.filter(status='present').count()
        absent_days = attendance_qs.filter(status='absent').count()

        attendance_percentage = (
            (present_days / total_days) * 100
            if total_days > 0 else 0
        )

        context = {
            'user': user,
            'student': student,
            'attendance_records': attendance_records,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': round(attendance_percentage, 2),
        }

        return render(request, 'accounts/student_dashboard.html', context)

    
    return render(request, 'accounts/dashboard.html', {'user': user})


