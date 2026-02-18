from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/register/', views.student_register, name='student_register'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    
    # Attendance Session URLs
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:session_id>/mark/', views.mark_attendance, name='mark_attendance'),
    path('sessions/<int:session_id>/mark/manual/', views.mark_attendance_manual, name='mark_attendance_manual'),
    path('sessions/<int:session_id>/mark/face/', views.mark_attendance_face, name='mark_attendance_face'),
    
    # Reports
    path('reports/attendance/', views.attendance_report, name='attendance_report'),
]
