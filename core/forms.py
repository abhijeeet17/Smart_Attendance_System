from django import forms
from .models import Student, Course, AttendanceSession, Attendance
from django.core.exceptions import ValidationError


class StudentRegistrationForm(forms.ModelForm):
    """Form for registering new students"""
    
    class Meta:
        model = Student
        fields = ['registration_number', 'name', 'email', 'phone', 'course', 'photo']
        widgets = {
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter registration number'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make photo field not required since we're using webcam capture
        self.fields['photo'].required = False
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError("Image file size should not exceed 5MB")
            
            # Check file type
            if not photo.content_type.startswith('image/'):
                raise ValidationError("Please upload a valid image file")
        
        return photo


class CourseForm(forms.ModelForm):
    """Form for creating courses"""
    
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'faculty']
        widgets = {
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CSE101'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python Programming'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class AttendanceSessionForm(forms.ModelForm):
    """Form for creating attendance sessions"""
    
    class Meta:
        model = AttendanceSession
        fields = ['course', 'session_date', 'session_time', 'session_type']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'session_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'session_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'session_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class FaceRecognitionUploadForm(forms.Form):
    """Form for uploading images for face recognition"""
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'face-upload'
        }),
        help_text="Upload a clear image containing student faces"
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError("Image file size should not exceed 10MB")
            
            # Check file type
            if not image.content_type.startswith('image/'):
                raise ValidationError("Please upload a valid image file")
        
        return image


class ManualAttendanceForm(forms.Form):
    """Form for manually marking attendance"""
    students = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        if course:
            students = Student.objects.filter(course=course, is_active=True)
            self.fields['students'].choices = [
                (student.id, f"{student.registration_number} - {student.name}") 
                for student in students
            ]
