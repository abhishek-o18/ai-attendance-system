from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, date
from .models import Attendance
from students.models import Student
from admin_panel.models import Class
from teachers.models import Teacher
import time
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from students.models import Student
from attendance.models import Attendance
from django.utils import timezone




@csrf_exempt
def biometric_receive(request):

    print("🔥 MACHINE HIT DJANGO 🔥")
    print("METHOD:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)

    if request.method == "POST":
        device_id = request.POST.get("device_id")
        user_id = request.POST.get("user_id")

        try:
            student = Student.objects.get(biometric_id=user_id)

            Attendance.objects.update_or_create(
                student=student,
                date=timezone.now().date(),
                defaults={
                    "status": "present",
                    "attendance_source": "biometric"
                }
            )

            print("✅ Attendance Saved:", user_id)

            return JsonResponse({"status": "success"})

        except Student.DoesNotExist:
            print("❌ Student not found:", user_id)
            return JsonResponse({"status": "student not found"})

    return JsonResponse({"status": "invalid request"})


@login_required
def mark_attendance(request):
    if not request.user.is_teacher_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('accounts:dashboard')
    
    assigned_classes = teacher.classes.all()
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    students = None
    selected_class = None
    selected_date = None
    
    if class_id and date:
        selected_class = get_object_or_404(Class, id=class_id)
        if selected_class in assigned_classes:
            try:
                selected_date = datetime.strptime(date, '%Y-%m-%d').date()
                if selected_date <= timezone.now().date():
                    students = Student.objects.filter(enrolled_class=selected_class)
                    
                    existing_attendance = Attendance.objects.filter(
                        class_obj=selected_class,
                        date=selected_date
                    ).exists()
                    
                    if existing_attendance:
                        messages.warning(request, f'Attendance for {selected_class.class_name} on {date} already exists. Use update option.')
                        return redirect('attendance:update', class_id=class_id, date=date)
                    else:
                        # continue your normal attendance logic here
                        pass

            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect('attendance:mark')

            except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
                return redirect('attendance:mark')


    
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        attendance_date = request.POST.get('date')
        
        if not class_id or not attendance_date:
            messages.error(request, 'Please select class and date.')
            return redirect('attendance:mark')
        
        class_obj = get_object_or_404(Class, id=class_id)
        
        if class_obj not in assigned_classes:
            messages.error(request, 'You are not assigned to this class.')
            return redirect('attendance:mark')
        
        try:
            attendance_date_obj = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('attendance:mark')
        
        if attendance_date_obj > timezone.now().date():
            messages.error(request, 'Cannot mark attendance for future dates.')
            return redirect('attendance:mark')
        
        existing_attendance = Attendance.objects.filter(
            class_obj=class_obj,
            date=attendance_date_obj
        ).exists()
        
        if existing_attendance:
            messages.warning(request, f'Attendance for {class_obj.class_name} on {attendance_date} already exists. Use update option.')
            return redirect('attendance:update', class_id=class_id, date=attendance_date)
        
        students = Student.objects.filter(enrolled_class=class_obj)
        
        attendance_data = []
        for student in students:
            student_key = f'student_{student.id}'
            status = request.POST.get(student_key, 'absent')
            Attendance.objects.create(
                student=student,
                class_obj=class_obj,
                date=attendance_date_obj,
                status=status,
                marked_by=request.user
            )
            attendance_data.append({
                'student': student,
                'status': status
            })
        
        messages.success(request, f'Attendance marked successfully for {class_obj.class_name} on {attendance_date}.')
        return redirect('attendance:history')
    
    context = {
        'assigned_classes': assigned_classes,
        'today': timezone.now().date(),
        'students': students,
        'selected_class': selected_class,
        'selected_date': selected_date,
        'class_id': class_id,
        'date': date,
    }
    return render(request, 'attendance/mark.html', context)


@login_required
def update_attendance(request, class_id, date):
    if not request.user.is_teacher_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('accounts:dashboard')
    
    class_obj = get_object_or_404(Class, id=class_id)
    
    if class_obj not in teacher.classes.all():
        messages.error(request, 'You are not assigned to this class.')
        return redirect('accounts:dashboard')
    
    try:
        attendance_date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('attendance:history')
    
    students = Student.objects.filter(enrolled_class=class_obj)
    attendance_records = Attendance.objects.filter(
        class_obj=class_obj,
        date=attendance_date_obj
    )
    
    attendance_dict = {record.student.id: record for record in attendance_records}
    
    if request.method == 'POST':
        updated_count = 0
        for student in students:
            new_status = request.POST.get(f'student_{student.id}', 'absent')
            
            if student.id in attendance_dict:
                record = attendance_dict[student.id]
                if record.status != new_status:
                    record.status = new_status
                    record.marked_by = request.user
                    record.save()
                    updated_count += 1
            else:
                Attendance.objects.create(
                    student=student,
                    class_obj=class_obj,
                    date=attendance_date_obj,
                    status=new_status,
                    marked_by=request.user
                )
                updated_count += 1
        
        messages.success(request, f'Attendance updated successfully. {updated_count} records modified.')
        return redirect('attendance:history')
    
    context = {
        'class_obj': class_obj,
        'date': attendance_date_obj,
        'students': students,
        'attendance_dict': attendance_dict,
    }
    return render(request, 'attendance/update.html', context)


@login_required
def attendance_history(request):
    if not request.user.is_teacher_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('accounts:dashboard')
    
    assigned_classes = teacher.classes.all()
    class_id = request.GET.get('class_id')
    date_filter = request.GET.get('date')
    
    attendance_records = Attendance.objects.filter(class_obj__in=assigned_classes)
    
    if class_id:
        attendance_records = attendance_records.filter(class_obj_id=class_id)
    
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(date=date_obj)
        except ValueError:
            pass
    
    attendance_records = attendance_records.order_by('-date', '-created_at')
    
    grouped_attendance = {}
    for record in attendance_records:
        key = (record.class_obj.id, record.date)
        if key not in grouped_attendance:
            grouped_attendance[key] = {
                'class_obj': record.class_obj,
                'date': record.date,
                'records': [],
                'present_count': 0,
                'absent_count': 0,
            }
        
        grouped_attendance[key]['records'].append(record)
        if record.status == 'present':
            grouped_attendance[key]['present_count'] += 1
        else:
            grouped_attendance[key]['absent_count'] += 1
    
    context = {
        'assigned_classes': assigned_classes,
        'selected_class_id': int(class_id) if class_id else None,
        'date_filter': date_filter,
        'grouped_attendance': grouped_attendance.values(),
    }
    return render(request, 'attendance/history.html', context)


@login_required
def view_attendance(request, class_id, date):
    if not request.user.is_teacher_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('accounts:dashboard')
    
    class_obj = get_object_or_404(Class, id=class_id)
    
    if class_obj not in teacher.classes.all():
        messages.error(request, 'You are not assigned to this class.')
        return redirect('accounts:dashboard')
    
    try:
        attendance_date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('attendance:history')
    
    students = Student.objects.filter(enrolled_class=class_obj)
    attendance_records = Attendance.objects.filter(
        class_obj=class_obj,
        date=attendance_date_obj
    )
    
    attendance_dict = {record.student.id: record for record in attendance_records}
    
    present_count = sum(1 for r in attendance_records if r.status == 'present')
    absent_count = sum(1 for r in attendance_records if r.status == 'absent')
    total_count = students.count()
    
    students_with_attendance = []
    for student in students:
        record = attendance_dict.get(student.id)
        students_with_attendance.append({
            'student': student,
            'attendance_record': record,
        })
    
    context = {
        'class_obj': class_obj,
        'date': attendance_date_obj,
        'students_with_attendance': students_with_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'total_count': total_count,
    }
    return render(request, 'attendance/view.html', context)

import cv2
from deepface import DeepFace
import os
import time

@login_required
def start_face_attendance(request, class_id):

    # 🔐 Teacher check
    if not request.user.is_teacher_user():
        return redirect('accounts:dashboard')

    teacher = Teacher.objects.get(user=request.user)
    class_obj = get_object_or_404(Class, id=class_id)

    if class_obj not in teacher.classes.all():
        return redirect('accounts:dashboard')

    face_db_path = "faces"
    cap = cv2.VideoCapture(0)

    start_time = time.time()
    MAX_DURATION = 300  # 5 minutes

    marked = set()
    last_mark_time = {}
    COOLDOWN = 10

    while True:
        ret, frame = cap.read()
        # ⏰ Auto stop after 5 minutes
        if time.time() - start_time > MAX_DURATION:
            print("⏰ Camera auto stopped after 5 minutes")
            break

        if cv2.waitKey(1) == 27:
            print("🛑 Stopped by ESC")
            break

        name_to_show = "Unknown"
        status_text = ""

        try:
            for file in os.listdir(face_db_path):
                path = os.path.join(face_db_path, file)

                result = DeepFace.verify(path, frame, enforce_detection=True)

                print("Checking:", file, "Distance:", result["distance"])

                if result["verified"] and result["distance"] < 0.4:
                    name = file.split(".")[0]
                    name_to_show = name

                    current_time = time.time()

                    if name not in last_mark_time or (current_time - last_mark_time[name]) > COOLDOWN:

                        if name not in marked:
                            try:
                                student = Student.objects.get(student_id=name)

                                # ✅ SAME LOGIC AS YOUR PROJECT
                                Attendance.objects.get_or_create(
                                    student=student,
                                    class_obj=class_obj,
                                    date=timezone.now().date(),
                                    defaults={
                                        "status": "present",
                                        "marked_by": request.user
                                    }
                                )

                                print("🎯 Attendance Marked:", name)
                                marked.add(name)
                                status_text = f"Marked: {name}"

                            except Student.DoesNotExist:
                                print("Student not found")

                        last_mark_time[name] = current_time

                    break

        except Exception as e:
            print("Error:", e)

        # show on screen
        cv2.putText(frame, f"Name: {name_to_show}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

        cv2.putText(frame, status_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

        cv2.imshow("Face Attendance", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return redirect('attendance:history')