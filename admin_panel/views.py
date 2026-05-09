from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Subject, Class
from teachers.models import Teacher
from students.models import Student
from accounts.models import User
from attendance.models import Attendance


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_attendance_records = Attendance.objects.count()
    
    today_attendance = Attendance.objects.filter(date=timezone.now().date()).count()
    
    recent_classes = Class.objects.all()[:5]
    recent_teachers = Teacher.objects.all()[:5]
    
    context = {
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_attendance_records': total_attendance_records,
        'today_attendance': today_attendance,
        'recent_classes': recent_classes,
        'recent_teachers': recent_teachers,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def teacher_list(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    teachers = Teacher.objects.all()
    return render(request, 'admin_panel/teacher_list.html', {'teachers': teachers})


@login_required
def teacher_add(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        teacher_id = request.POST.get('teacher_id')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, 'Teacher ID already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='teacher'
            )
            Teacher.objects.create(
                user=user,
                teacher_id=teacher_id,
                department=department,
                qualification=qualification
            )
            messages.success(request, 'Teacher added successfully.')
            return redirect('admin_panel:teacher_list')
    
    return render(request, 'admin_panel/teacher_add.html')


@login_required
def teacher_edit(request, teacher_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.user.email = request.POST.get('email')
        teacher.user.phone = request.POST.get('phone')
        teacher.user.save()
        
        teacher.department = request.POST.get('department')
        teacher.qualification = request.POST.get('qualification')
        teacher.save()
        
        messages.success(request, 'Teacher updated successfully.')
        return redirect('admin_panel:teacher_list')
    
    return render(request, 'admin_panel/teacher_edit.html', {'teacher': teacher})


@login_required
def teacher_delete(request, teacher_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.user.delete()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('admin_panel:teacher_list')
    
    return render(request, 'admin_panel/teacher_delete.html', {'teacher': teacher})


@login_required
def subject_list(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    subjects = Subject.objects.all()
    return render(request, 'admin_panel/subject_list.html', {'subjects': subjects})


@login_required
def subject_add(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        description = request.POST.get('description')
        
        if Subject.objects.filter(subject_code=subject_code).exists():
            messages.error(request, 'Subject code already exists.')
        else:
            Subject.objects.create(
                subject_code=subject_code,
                subject_name=subject_name,
                description=description
            )
            messages.success(request, 'Subject added successfully.')
            return redirect('admin_panel:subject_list')
    
    return render(request, 'admin_panel/subject_add.html')


@login_required
def subject_edit(request, subject_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        subject.subject_name = request.POST.get('subject_name')
        subject.description = request.POST.get('description')
        subject.save()
        messages.success(request, 'Subject updated successfully.')
        return redirect('admin_panel:subject_list')
    
    return render(request, 'admin_panel/subject_edit.html', {'subject': subject})


@login_required
def subject_delete(request, subject_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('admin_panel:subject_list')
    
    return render(request, 'admin_panel/subject_delete.html', {'subject': subject})


@login_required
def class_list(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    classes = Class.objects.all()
    return render(request, 'admin_panel/class_list.html', {'classes': classes})


@login_required
def class_add(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        class_code = request.POST.get('class_code')
        class_name = request.POST.get('class_name')
        subject_id = request.POST.get('subject')
        schedule = request.POST.get('schedule')
        room = request.POST.get('room')
        teacher_ids = request.POST.getlist('teachers')
        
        if Class.objects.filter(class_code=class_code).exists():
            messages.error(request, 'Class code already exists.')
        else:
            subject = get_object_or_404(Subject, id=subject_id)
            class_obj = Class.objects.create(
                class_code=class_code,
                class_name=class_name,
                subject=subject,
                schedule=schedule,
                room=room
            )
            if teacher_ids:
                class_obj.teachers.set(teacher_ids)
            messages.success(request, 'Class added successfully.')
            return redirect('admin_panel:class_list')
    
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'admin_panel/class_add.html', {'subjects': subjects, 'teachers': teachers})


@login_required
def class_edit(request, class_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        class_obj.class_name = request.POST.get('class_name')
        class_obj.subject_id = request.POST.get('subject')
        class_obj.schedule = request.POST.get('schedule')
        class_obj.room = request.POST.get('room')
        teacher_ids = request.POST.getlist('teachers')
        class_obj.teachers.set(teacher_ids)
        class_obj.save()
        messages.success(request, 'Class updated successfully.')
        return redirect('admin_panel:class_list')
    
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'admin_panel/class_edit.html', {
        'class_obj': class_obj,
        'subjects': subjects,
        'teachers': teachers
    })


@login_required
def class_delete(request, class_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('admin_panel:class_list')
    
    return render(request, 'admin_panel/class_delete.html', {'class_obj': class_obj})


@login_required
def student_add(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        enrolled_class_id = request.POST.get('enrolled_class')
        
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists.')
        elif User.objects.filter(username=student_id).exists():
            messages.error(request, 'A user with this student ID already exists.')
        else:
            enrolled_class = get_object_or_404(Class, id=enrolled_class_id)
            user = User.objects.create_user(
                username=student_id,
                password=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role='student',
            )
            Student.objects.create(
                user=user,
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth if date_of_birth else None,
                address=address,
                enrolled_class=enrolled_class
            )
            messages.success(request, 'Student added successfully. Login username and password are set to the student ID.')
            return redirect('admin_panel:student_list')
    
    classes = Class.objects.all()
    return render(request, 'admin_panel/student_add.html', {'classes': classes})


@login_required
def student_list(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    class_id = request.GET.get('class_id')
    
    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)
        students = Student.objects.filter(enrolled_class=class_obj)
    else:
        students = Student.objects.all()
        class_obj = None
    
    classes = Class.objects.all()
    
    return render(request, 'admin_panel/student_list.html', {
        'students': students,
        'classes': classes,
        'selected_class': class_obj
    })


@login_required
def student_edit(request, student_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth') if request.POST.get('date_of_birth') else None
        address = request.POST.get('address')
        enrolled_class_id = request.POST.get('enrolled_class')
        
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.phone = phone
        student.date_of_birth = date_of_birth
        student.address = address
        student.enrolled_class_id = enrolled_class_id
        student.save()
        
        if student.user:
            student.user.first_name = first_name
            student.user.last_name = last_name
            student.user.email = email
            student.user.phone = phone
            student.user.save()
        
        messages.success(request, 'Student updated successfully.')
        return redirect('admin_panel:student_list')
    
    classes = Class.objects.all()
    return render(request, 'admin_panel/student_edit.html', {
        'student': student,
        'classes': classes
    })


@login_required
def student_delete(request, student_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        user = student.user
        student.delete()
        if user:
            user.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('admin_panel:student_list')
    
    return render(request, 'admin_panel/student_delete.html', {'student': student})


@login_required
def attendance_reports(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    report_type = request.GET.get('type', 'daily')
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    month = request.GET.get('month')
    
    classes = Class.objects.all()
    selected_class = None
    
    if class_id:
        selected_class = get_object_or_404(Class, id=class_id)
    
    if report_type == 'daily':
        if date:
            attendance_records = Attendance.objects.filter(date=date)
            if selected_class:
                attendance_records = attendance_records.filter(class_obj=selected_class)
        else:
            attendance_records = Attendance.objects.filter(date=timezone.now().date())
            if selected_class:
                attendance_records = attendance_records.filter(class_obj=selected_class)
    
    elif report_type == 'monthly':
        if month:
            year, month_num = month.split('-')
            attendance_records = Attendance.objects.filter(
                date__year=year,
                date__month=month_num
            )
            if selected_class:
                attendance_records = attendance_records.filter(class_obj=selected_class)
        else:
            now = timezone.now()
            attendance_records = Attendance.objects.filter(
                date__year=now.year,
                date__month=now.month
            )
            if selected_class:
                attendance_records = attendance_records.filter(class_obj=selected_class)
    
    elif report_type == 'subject':
        if selected_class:
            attendance_records = Attendance.objects.filter(class_obj=selected_class)
        else:
            attendance_records = Attendance.objects.all()
    
    else:
        attendance_records = Attendance.objects.all()
    
    attendance_records = attendance_records.order_by('-date', '-created_at')
    
    context = {
        'report_type': report_type,
        'classes': classes,
        'selected_class': selected_class,
        'attendance_records': attendance_records,
        'date': date,
        'month': month,
    }
    return render(request, 'admin_panel/attendance_reports.html', context)

