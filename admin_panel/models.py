from django.db import models
from teachers.models import Teacher


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    
    class Meta:
        ordering = ['subject_code']


class Class(models.Model):
    class_code = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    teachers = models.ManyToManyField(Teacher, related_name='classes', blank=True)
    schedule = models.CharField(max_length=100, blank=True)
    room = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.class_name} ({self.class_code})"
    
    class Meta:
        ordering = ['class_code']
        verbose_name_plural = 'Classes'

