from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'date', 'status', 'marked_by', 'created_at']
    list_filter = ['status', 'date', 'class_obj']
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name', 'class_obj__class_code']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

