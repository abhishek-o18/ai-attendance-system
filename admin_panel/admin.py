from django.contrib import admin
from .models import Subject, Class


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'subject_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['subject_code', 'subject_name']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_code', 'class_name', 'subject', 'room', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['class_code', 'class_name']
    filter_horizontal = ['teachers']

