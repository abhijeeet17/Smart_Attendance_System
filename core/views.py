from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from .models import Student, Course, AttendanceSession, Attendance
from .forms import (
    StudentRegistrationForm, CourseForm, AttendanceSessionForm,
    FaceRecognitionUploadForm, ManualAttendanceForm
)
from .face_recognition_utils import get_face_service
import json


def home(request):
    """Home page view"""
    context = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_courses': Course.objects.count(),
        'today_sessions': AttendanceSession.objects.filter(
            session_date=timezone.now().date()
        ).count(),
        'recent_sessions': AttendanceSession.objects.all()[:5],
    }
    return render(request, 'core/home.html', context)


def student_list(request):
    """List all students"""
    students = Student.objects.filter(is_active=True).select_related('course')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filter by course
    course_id = request.GET.get('course', '')
    if course_id:
        students = students.filter(course_id=course_id)
    
    courses = Course.objects.all()
    
    context = {
        'students': students,
        'courses': courses,
        'search_query': search_query,
        'selected_course': course_id,
    }
    return render(request, 'core/student_list.html', context)


def student_register(request):
    """Register a new student with face encoding"""
    if request.method == 'POST':
        # Check if image was captured via webcam
        captured_image_data = request.POST.get('captured_image_data', '')
        
        if captured_image_data:
            # Handle webcam captured image
            import base64
            from io import BytesIO
            from django.core.files.uploadedfile import InMemoryUploadedFile
            import sys
            from PIL import Image as PILImage
            
            # Remove the data URL prefix
            image_data = captured_image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            # Convert to PIL Image and then to InMemoryUploadedFile
            image = PILImage.open(BytesIO(image_bytes))
            output = BytesIO()
            image.save(output, format='JPEG', quality=90)
            output.seek(0)
            
            # Create a file object
            photo_file = InMemoryUploadedFile(
                output,
                'ImageField',
                f'student_{timezone.now().strftime("%Y%m%d_%H%M%S")}.jpg',
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
            
            # Create a mutable copy of POST data
            post_data = request.POST.copy()
            post_data['photo'] = photo_file
            
            # Create form with captured image
            form = StudentRegistrationForm(post_data, {'photo': photo_file})
        else:
            form = StudentRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            student = form.save(commit=False)
            
            # Handle captured image
            if captured_image_data and not student.photo:
                import base64
                from io import BytesIO
                from django.core.files.base import ContentFile
                from PIL import Image as PILImage
                
                # Remove the data URL prefix
                image_data = captured_image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                
                # Save the image
                student.photo.save(
                    f'student_{student.registration_number}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.jpg',
                    ContentFile(image_bytes),
                    save=False
                )
            
            # Generate face encoding
            if student.photo:
                student.save()  # Save first to get the file path
                face_service = get_face_service()
                encoding = face_service.encode_face(student.photo.path)
                
                if encoding:
                    student.face_encoding = face_service.encoding_to_string(encoding)
                    student.save()
                    messages.success(request, f'Student {student.name} registered successfully with face recognition!')
                    return redirect('student_list')
                else:
                    messages.error(request, 'No face detected in the captured photo. Please try again with a clearer image.')
                    student.delete()  # Remove student if face encoding fails
            else:
                messages.error(request, 'Please capture your face photo.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'core/student_register.html', {'form': form})


def student_detail(request, pk):
    """View student details and attendance history"""
    student = get_object_or_404(Student, pk=pk)
    
    # Get attendance records
    attendances = Attendance.objects.filter(student=student).select_related(
        'session', 'session__course'
    ).order_by('-session__session_date')
    
    # Calculate statistics
    total_sessions = attendances.count()
    present_count = attendances.filter(status='present').count()
    absent_count = attendances.filter(status='absent').count()
    
    attendance_percentage = student.get_attendance_percentage()
    
    context = {
        'student': student,
        'attendances': attendances[:20],  # Show last 20 records
        'total_sessions': total_sessions,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'core/student_detail.html', context)


def course_list(request):
    """List all courses"""
    courses = Course.objects.annotate(
        student_count=Count('students')
    ).select_related('faculty')
    
    context = {
        'courses': courses,
    }
    return render(request, 'core/course_list.html', context)


def course_create(request):
    """Create a new course"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course {course.course_name} created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'core/course_create.html', {'form': form})


def session_list(request):
    """List all attendance sessions"""
    sessions = AttendanceSession.objects.select_related(
        'course', 'faculty'
    ).order_by('-session_date', '-session_time')
    
    # Filter by date
    date_filter = request.GET.get('date', '')
    if date_filter:
        sessions = sessions.filter(session_date=date_filter)
    
    # Filter by course
    course_id = request.GET.get('course', '')
    if course_id:
        sessions = sessions.filter(course_id=course_id)
    
    courses = Course.objects.all()
    
    context = {
        'sessions': sessions,
        'courses': courses,
        'date_filter': date_filter,
        'selected_course': course_id,
    }
    return render(request, 'core/session_list.html', context)


def session_create(request):
    """Create a new attendance session"""
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            if request.user.is_authenticated:
                session.faculty = request.user
            session.save()
            
            # Create attendance records for all students in the course
            students = Student.objects.filter(course=session.course, is_active=True)
            for student in students:
                Attendance.objects.create(
                    session=session,
                    student=student,
                    status='absent',
                    marked_by='system'
                )
            
            messages.success(request, f'Attendance session created for {session.course.course_name}!')
            return redirect('mark_attendance', session_id=session.id)
    else:
        form = AttendanceSessionForm()
    
    return render(request, 'core/session_create.html', {'form': form})


def mark_attendance(request, session_id):
    """Mark attendance for a session"""
    session = get_object_or_404(AttendanceSession, pk=session_id)
    attendances = Attendance.objects.filter(session=session).select_related('student')
    
    context = {
        'session': session,
        'attendances': attendances,
        'summary': session.get_attendance_summary(),
    }
    return render(request, 'core/mark_attendance.html', context)


def mark_attendance_manual(request, session_id):
    """Manually mark attendance"""
    session = get_object_or_404(AttendanceSession, pk=session_id)
    
    if request.method == 'POST':
        present_student_ids = request.POST.getlist('students')
        
        # Update attendance
        attendances = Attendance.objects.filter(session=session)
        for attendance in attendances:
            if str(attendance.student.id) in present_student_ids:
                attendance.status = 'present'
                attendance.marked_by = 'faculty'
            else:
                attendance.status = 'absent'
                attendance.marked_by = 'faculty'
            attendance.save()
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('mark_attendance', session_id=session.id)
    
    form = ManualAttendanceForm(course=session.course)
    
    context = {
        'session': session,
        'form': form,
    }
    return render(request, 'core/mark_attendance_manual.html', context)


def mark_attendance_face(request, session_id):
    """Mark attendance using face recognition with webcam capture"""
    session = get_object_or_404(AttendanceSession, pk=session_id)
    
    if request.method == 'POST':
        # Check if image was captured via webcam
        captured_image_data = request.POST.get('captured_image_data', '')
        
        if captured_image_data:
            # Handle webcam captured image
            import base64
            from io import BytesIO
            
            try:
                # Remove the data URL prefix
                image_data = captured_image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                
                # Get face service
                face_service = get_face_service()
                
                # Encode uploaded face from bytes
                uploaded_encoding = face_service.encode_face_from_bytes(image_bytes)
                
                if not uploaded_encoding:
                    messages.error(request, 'No face detected in the captured image. Please ensure your face is clearly visible and try again.')
                    return redirect('mark_attendance_face', session_id=session.id)
                
                # Get all students in this course with face encodings
                students = Student.objects.filter(
                    course=session.course, 
                    is_active=True
                ).exclude(face_encoding='')
                
                if not students.exists():
                    messages.warning(request, 'No students with face encodings found for this course. Please ensure students have registered with face photos.')
                    return redirect('mark_attendance', session_id=session.id)
                
                student_encodings = {}
                for student in students:
                    encoding = face_service.string_to_encoding(student.face_encoding)
                    if encoding:
                        student_encodings[student.id] = encoding
                
                if not student_encodings:
                    messages.warning(request, 'No valid face encodings found. Please ensure students have registered properly.')
                    return redirect('mark_attendance', session_id=session.id)
                
                # Find matching student
                matched_student_id, confidence = face_service.find_matching_student(
                    uploaded_encoding, 
                    student_encodings
                )
                
                if matched_student_id:
                    # Update attendance
                    attendance = Attendance.objects.get(
                        session=session, 
                        student_id=matched_student_id
                    )
                    
                    # Check if already marked present
                    if attendance.status == 'present':
                        student = Student.objects.get(id=matched_student_id)
                        messages.info(
                            request, 
                            f'Attendance already marked for {student.name}!'
                        )
                    else:
                        attendance.status = 'present'
                        attendance.marked_by = 'face_recognition'
                        attendance.confidence_score = confidence
                        attendance.marked_at = timezone.now()
                        
                        # Save the captured image
                        from django.core.files.base import ContentFile
                        attendance.photo_captured.save(
                            f'attendance_{session.id}_{matched_student_id}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.jpg',
                            ContentFile(image_bytes),
                            save=False
                        )
                        attendance.save()
                        
                        student = Student.objects.get(id=matched_student_id)
                        messages.success(
                            request, 
                            f'✓ Attendance marked for {student.name} (Confidence: {confidence:.1f}%)'
                        )
                    
                    return redirect('mark_attendance', session_id=session.id)
                else:
                    messages.error(request, 'Face not recognized. Please ensure you are registered for this course or try again with better lighting.')
                    return redirect('mark_attendance_face', session_id=session.id)
                    
            except Exception as e:
                messages.error(request, f'Error processing image: {str(e)}. Please try again.')
                return redirect('mark_attendance_face', session_id=session.id)
        else:
            # Handle traditional file upload (backward compatibility)
            form = FaceRecognitionUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_image = form.cleaned_data['image']
                
                # Get face service
                face_service = get_face_service()
                
                # Encode uploaded face
                uploaded_encoding = face_service.encode_face_from_bytes(uploaded_image.read())
                
                if not uploaded_encoding:
                    messages.error(request, 'No face detected in the uploaded image. Please try again.')
                    return redirect('mark_attendance_face', session_id=session.id)
                
                # Get all students in this course with face encodings
                students = Student.objects.filter(
                    course=session.course, 
                    is_active=True
                ).exclude(face_encoding='')
                
                student_encodings = {}
                for student in students:
                    encoding = face_service.string_to_encoding(student.face_encoding)
                    if encoding:
                        student_encodings[student.id] = encoding
                
                # Find matching student
                matched_student_id, confidence = face_service.find_matching_student(
                    uploaded_encoding, 
                    student_encodings
                )
                
                if matched_student_id:
                    # Update attendance
                    attendance = Attendance.objects.get(
                        session=session, 
                        student_id=matched_student_id
                    )
                    attendance.status = 'present'
                    attendance.marked_by = 'face_recognition'
                    attendance.confidence_score = confidence
                    attendance.photo_captured = uploaded_image
                    attendance.save()
                    
                    student = Student.objects.get(id=matched_student_id)
                    messages.success(
                        request, 
                        f'Attendance marked for {student.name} (Confidence: {confidence}%)'
                    )
                else:
                    messages.error(request, 'No matching student found. Please try again or mark manually.')
                
                return redirect('mark_attendance', session_id=session.id)
    else:
        form = FaceRecognitionUploadForm()
    
    context = {
        'session': session,
        'form': form,
    }
    return render(request, 'core/mark_attendance_face.html', context)


def attendance_report(request):
    """Generate attendance report"""
    courses = Course.objects.all()
    students = Student.objects.filter(is_active=True)
    
    # Get filters
    course_id = request.GET.get('course', '')
    student_id = request.GET.get('student', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Build query
    attendances = Attendance.objects.select_related(
        'student', 'session', 'session__course'
    )
    
    if course_id:
        attendances = attendances.filter(session__course_id=course_id)
        students = students.filter(course_id=course_id)
    
    if student_id:
        attendances = attendances.filter(student_id=student_id)
    
    if date_from:
        attendances = attendances.filter(session__session_date__gte=date_from)
    
    if date_to:
        attendances = attendances.filter(session__session_date__lte=date_to)
    
    attendances = attendances.order_by('-session__session_date')
    
    context = {
        'courses': courses,
        'students': students,
        'attendances': attendances,
        'selected_course': course_id,
        'selected_student': student_id,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'core/attendance_report.html', context)


def dashboard(request):
    """Main dashboard view"""
    # Statistics
    total_students = Student.objects.filter(is_active=True).count()
    total_courses = Course.objects.count()
    today_sessions = AttendanceSession.objects.filter(
        session_date=timezone.now().date()
    ).count()
    
    # Recent sessions
    recent_sessions = AttendanceSession.objects.select_related(
        'course', 'faculty'
    ).order_by('-session_date', '-session_time')[:5]
    
    # Low attendance students
    low_attendance_students = []
    for student in Student.objects.filter(is_active=True)[:10]:
        percentage = student.get_attendance_percentage()
        if percentage < 75:
            low_attendance_students.append({
                'student': student,
                'percentage': percentage
            })
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'today_sessions': today_sessions,
        'recent_sessions': recent_sessions,
        'low_attendance_students': low_attendance_students,
    }
    return render(request, 'core/dashboard.html', context)
