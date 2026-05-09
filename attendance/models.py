from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from students.models import Student
from admin_panel.models import Class
from accounts.models import User


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'class_obj', 'date']
        ordering = ['-date', 'student']
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['class_obj', 'date']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.class_obj} - {self.date} - {self.status}"
    
    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError('Cannot mark attendance for future dates.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

