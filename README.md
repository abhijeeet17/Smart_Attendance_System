# Smart AI-Enabled Attendance System with Face Recognition

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern, AI-powered attendance management system built with Django that uses face recognition technology to automate attendance marking. Designed specifically for LPU Campus Management System requirements.

## 🎯 Project Overview

This Smart Attendance System leverages cutting-edge face recognition technology to provide seamless, contactless attendance management. The system eliminates manual attendance marking, reduces time spent on administrative tasks, and provides real-time attendance tracking with detailed analytics.

## ✨ Key Features

### 1. **AI-Powered Face Recognition**
- Automatic face encoding generation during student registration
- High-accuracy face matching using `face_recognition` library
- Confidence score reporting for each recognition
- Support for multiple detection models (HOG/CNN)

### 2. **Smart Attendance Management**
- **One-Click Marking**: Faculty can mark attendance with a single click
- **Face Recognition Mode**: Upload photo to automatically identify and mark students
- **Manual Mode**: Traditional checkbox-based attendance marking
- **Instant Updates**: Real-time attendance status updates
- **Automated Notifications**: System-ready for student/parent notification integration

### 3. **Comprehensive Dashboard**
- Real-time statistics (total students, courses, sessions)
- Low attendance alerts for students below 75%
- Recent session tracking
- Quick action buttons for common tasks

### 4. **Student Management**
- Easy student registration with photo upload
- Automatic face encoding generation
- Search and filter functionality
- Individual student attendance history
- Attendance percentage calculation

### 5. **Course & Session Management**
- Multiple course support
- Flexible session types (Lecture, Lab, Tutorial)
- Date and time scheduling
- Faculty assignment
- Session-wise attendance tracking

### 6. **Detailed Reports**
- Attendance reports with filtering options
- Course-wise attendance analysis
- Student-wise attendance history
- Date range filtering
- Export-ready format

## 🛠️ Technology Stack

- **Backend Framework**: Django 4.2+
- **Programming Language**: Python 3.8+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Face Recognition**: face_recognition library (dlib-based)
- **Image Processing**: OpenCV, Pillow
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Outfit, JetBrains Mono)

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- CMake (required for dlib/face_recognition)
- Visual Studio Build Tools (Windows) or build-essential (Linux)

### Installing CMake and Build Tools

**Windows:**
```bash
# Download and install CMake from: https://cmake.org/download/
# Install Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
```

**macOS:**
```bash
brew install cmake
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd smart_attendance_system
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Installing `face_recognition` may take some time as it compiles dlib. If you encounter issues:
- On Windows: Ensure Visual Studio Build Tools are installed
- On Linux: Install development libraries: `sudo apt-get install python3-dev`
- Alternative: Use `pip install face_recognition-models` first

### 4. Configure Database
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your web browser.

## 📁 Project Structure

```
smart_attendance_system/
│
├── attendance_system/          # Main project directory
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
│
├── core/                      # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Django forms
│   ├── admin.py              # Admin configuration
│   ├── face_recognition_utils.py  # Face recognition service
│   ├── signals.py            # Django signals
│   │
│   ├── templates/core/       # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── student_list.html
│   │   ├── student_register.html
│   │   ├── mark_attendance.html
│   │   ├── mark_attendance_face.html
│   │   └── session_create.html
│   │
│   └── migrations/           # Database migrations
│
├── media/                    # User-uploaded files
│   ├── student_photos/       # Student face photos
│   └── attendance_photos/    # Attendance verification photos
│
├── staticfiles/              # Collected static files
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
└── README.md                # This file
```

## 💡 How to Use

### 1. Initial Setup
1. Access admin panel at `http://127.0.0.1:8000/admin/`
2. Log in with superuser credentials
3. Create courses from the admin panel or web interface

### 2. Register Students
1. Navigate to "Students" → "Add Student"
2. Fill in student details
3. **Important**: Upload a clear, well-lit face photo
4. Submit - face encoding is automatically generated

### 3. Create Attendance Session
1. Go to "Sessions" → "New Session"
2. Select course, date, time, and type
3. Submit - attendance records are auto-created for all enrolled students

### 4. Mark Attendance

**Option A: Face Recognition**
1. Click "Mark Attendance" on a session
2. Select "Face Recognition"
3. Upload a photo containing student's face
4. System automatically identifies and marks attendance

**Option B: Manual Marking**
1. Click "Mark Attendance" on a session
2. Select "Manual Selection"
3. Check boxes for present students
4. Submit

### 5. View Reports
1. Navigate to "Reports" → "Attendance"
2. Apply filters (course, student, date range)
3. View detailed attendance records

## 🔧 Configuration

### Face Recognition Settings

Edit `attendance_system/settings.py`:

```python
# Adjust recognition tolerance (lower = more strict)
FACE_RECOGNITION_TOLERANCE = 0.6  # Range: 0.0 to 1.0

# Choose detection model
FACE_RECOGNITION_MODEL = 'hog'  # 'hog' (faster) or 'cnn' (more accurate)
```

### Database Configuration

For production, switch to PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎨 UI Design Philosophy

The interface features a modern, professional design with:
- **Bold Typography**: Outfit font family for clean, readable text
- **Vibrant Gradients**: Purple-to-indigo gradients for visual appeal
- **Card-based Layout**: Organized information in elegant cards
- **Smooth Animations**: Subtle hover and transition effects
- **Responsive Design**: Mobile-friendly and adaptive layouts
- **Intuitive Icons**: Font Awesome icons for better UX

## 🧪 Testing Face Recognition

### Test Photos Requirements:
- **Resolution**: At least 640x480 pixels
- **Lighting**: Even, natural lighting
- **Face Position**: Centered, facing camera directly
- **Background**: Clean, uncluttered
- **Expression**: Neutral or slight smile
- **Obstructions**: No glasses, hats, or face coverings

### Expected Accuracy:
- **Same conditions**: 95%+ accuracy
- **Different lighting**: 85-90% accuracy
- **Different angles**: 80-85% accuracy

## 🔐 Security Considerations

1. **Face Encodings**: Stored as mathematical vectors (not reversible to images)
2. **Photo Storage**: Secure media file handling
3. **Access Control**: Admin authentication required
4. **CSRF Protection**: Enabled by default in Django
5. **Password Hashing**: Django's built-in secure hashing

### Production Checklist:
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure proper file permissions
- [ ] Set up regular backups
- [ ] Implement rate limiting
- [ ] Add logging and monitoring

## 📊 Database Models

### Student
- Registration number, name, email, phone
- Course association
- Face photo and encoding
- Active status

### Course
- Course code and name
- Faculty assignment
- Creation timestamp

### AttendanceSession
- Course and faculty references
- Session date, time, and type
- Active status

### Attendance
- Session and student references
- Status (present/absent)
- Marking method and confidence score
- Captured photo (optional)

## 🚧 Troubleshooting

### Face Recognition Not Working
- Ensure photo is clear and well-lit
- Check if face encoding was generated (admin panel)
- Verify CMake and dlib are properly installed
- Try different FACE_RECOGNITION_MODEL setting

### Import Errors
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- Check Python version (3.8+)

### Database Errors
- Delete `db.sqlite3` and rerun migrations
- Check for migration conflicts
- Ensure proper database permissions

### Performance Issues
- Use 'hog' model instead of 'cnn' for faster processing
- Optimize images before upload
- Consider PostgreSQL for better performance
- Add database indexes for frequently queried fields

## 🔮 Future Enhancements

- [ ] Real-time webcam capture for attendance
- [ ] Batch face recognition from classroom photos
- [ ] SMS/Email notifications to students and parents
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics and visualizations
- [ ] Facial recognition with mask detection
- [ ] Integration with LMS platforms
- [ ] Multi-language support
- [ ] Biometric device integration
- [ ] API for third-party integrations

## 📝 Contributing

This is a university project, but contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is created for educational purposes as part of LPU coursework.


## 🙏 Acknowledgments

- LPU Faculty for project guidance
- Face Recognition library by Adam Geitgey
- Django community for excellent documentation
- Font Awesome for icons
- Google Fonts for typography

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Contact: sharmaabhijeet317@gmail.com

---

**Made with ❤️ for LPU Project II**

*Smart Attendance System - Leveraging AI for Efficient Campus Management*
