from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'enrolled_class', 'enrollment_date', 'biometric_id']
    list_filter = ['enrolled_class', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'biometric_id']
    date_hierarchy = 'enrollment_date'

