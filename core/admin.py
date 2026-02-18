from django.contrib import admin
from .models import Course, Student, AttendanceSession, Attendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'faculty', 'created_at']
    search_fields = ['course_code', 'course_name']
    list_filter = ['faculty', 'created_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'name', 'email', 'course', 'is_active', 'created_at']
    search_fields = ['registration_number', 'name', 'email']
    list_filter = ['course', 'is_active', 'created_at']
    readonly_fields = ['face_encoding']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('registration_number', 'name', 'email', 'phone', 'course')
        }),
        ('Face Recognition', {
            'fields': ('photo', 'face_encoding', 'is_active'),
            'description': 'Upload a clear photo for face recognition. Face encoding will be generated automatically.'
        }),
    )


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['course', 'session_date', 'session_time', 'session_type', 'faculty', 'is_active']
    search_fields = ['course__course_name', 'course__course_code']
    list_filter = ['session_type', 'session_date', 'course', 'is_active']
    date_hierarchy = 'session_date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'marked_by', 'confidence_score', 'marked_at']
    search_fields = ['student__name', 'student__registration_number']
    list_filter = ['status', 'marked_by', 'session__session_date']
    date_hierarchy = 'marked_at'
    readonly_fields = ['marked_at', 'confidence_score']
