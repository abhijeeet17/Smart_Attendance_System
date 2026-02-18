from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class Course(models.Model):
    """Model for academic courses"""
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['course_name']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Student(models.Model):
    """Model for student information"""
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='students')
    photo = models.ImageField(upload_to='student_photos/', help_text="Upload a clear face photo for recognition")
    face_encoding = models.TextField(blank=True, help_text="Stored face encoding for recognition")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.registration_number} - {self.name}"
    
    def get_attendance_percentage(self, course=None):
        """Calculate attendance percentage for a student"""
        if course:
            total_sessions = AttendanceSession.objects.filter(course=course).count()
            attended = Attendance.objects.filter(student=self, session__course=course, status='present').count()
        else:
            total_sessions = AttendanceSession.objects.all().count()
            attended = Attendance.objects.filter(student=self, status='present').count()
        
        if total_sessions == 0:
            return 0
        return round((attended / total_sessions) * 100, 2)


class AttendanceSession(models.Model):
    """Model for attendance sessions"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    faculty = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    session_date = models.DateField(default=timezone.now)
    session_time = models.TimeField(default=timezone.now)
    session_type = models.CharField(
        max_length=20,
        choices=[
            ('lecture', 'Lecture'),
            ('lab', 'Lab'),
            ('tutorial', 'Tutorial'),
        ],
        default='lecture'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-session_date', '-session_time']
        unique_together = ['course', 'session_date', 'session_time']
    
    def __str__(self):
        return f"{self.course.course_code} - {self.session_date} {self.session_time}"
    
    def get_attendance_summary(self):
        """Get attendance summary for this session"""
        total = self.attendances.count()
        present = self.attendances.filter(status='present').count()
        absent = self.attendances.filter(status='absent').count()
        
        return {
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': round((present / total * 100), 2) if total > 0 else 0
        }


class Attendance(models.Model):
    """Model for individual attendance records"""
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(
        max_length=10,
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
        ],
        default='absent'
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.CharField(max_length=50, default='system')  # 'faculty', 'face_recognition', 'system'
    confidence_score = models.FloatField(null=True, blank=True, help_text="Face recognition confidence")
    photo_captured = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)
    
    class Meta:
        ordering = ['-marked_at']
        unique_together = ['session', 'student']
    
    def __str__(self):
        return f"{self.student.name} - {self.session} - {self.status}"
