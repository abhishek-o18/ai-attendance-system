from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from admin_panel.models import Class


@login_required
def student_list(request):
    class_id = request.GET.get('class_id')
    
    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)
        students = Student.objects.filter(enrolled_class=class_obj)
    else:
        students = Student.objects.all()
        class_obj = None
    
    classes = Class.objects.all()
    
    context = {
        'students': students,
        'classes': classes,
        'selected_class': class_obj,
    }
    return render(request, 'students/list.html', context)


@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.user.is_student_user():
        if not student.user or student.user != request.user:
            messages.error(request, 'You can only view your own attendance.')
            if hasattr(request.user, 'student_profile'):
                return redirect('students:detail', student_id=request.user.student_profile.id)
            return redirect('accounts:dashboard')
    
    from attendance.models import Attendance
    attendance_qs = Attendance.objects.filter(student=student)

    # Slice only for display
    attendance_records = attendance_qs.order_by('-date')[:30]

    # Calculate stats from full queryset
    total_days = attendance_qs.count()
    present_days = attendance_qs.filter(status='present').count()
    absent_days = attendance_qs.filter(status='absent').count()

    attendance_percentage = (
        (present_days / total_days) * 100
        if total_days > 0 else 0
    )

    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    return render(request, 'students/detail.html', context)

