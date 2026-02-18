# 🚀 Quick Setup Guide - Smart Attendance System

This guide will help you set up and run the Smart Attendance System on your local machine.

## ⚡ Prerequisites Check

Before starting, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Git (optional, for version control)
- ✅ 2GB free disk space
- ✅ Internet connection (for initial setup)

### Check Python Version

Open terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

## 📦 Step-by-Step Installation

### Step 1: Extract the Project

Extract the zip file to a location of your choice:
```
C:\Projects\smart_attendance_system  (Windows)
~/Projects/smart_attendance_system   (macOS/Linux)
```

### Step 2: Open Terminal

Navigate to the project directory:

**Windows:**
- Open Command Prompt or PowerShell
- Run: `cd C:\Projects\smart_attendance_system`

**macOS/Linux:**
- Open Terminal
- Run: `cd ~/Projects/smart_attendance_system`

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

⚠️ **IMPORTANT**: The face_recognition library requires some system dependencies.

#### Windows:
1. Install Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
2. Install CMake from: https://cmake.org/download/
3. Then run:
```bash
pip install cmake
pip install dlib
pip install face-recognition
pip install -r requirements.txt
```

#### macOS:
```bash
brew install cmake
pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install python3-dev
pip install -r requirements.txt
```

**Note**: Installing face_recognition may take 5-10 minutes as it compiles dlib.

### Step 5: Setup Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User

```bash
python manage.py createsuperuser
```

Enter your details:
- Username: admin (or your choice)
- Email: your.email@example.com
- Password: (choose a strong password)

### Step 7: Run the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 8: Access the Application

Open your web browser and visit:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🎯 First Steps After Installation

### 1. Login to Admin Panel
- Go to http://127.0.0.1:8000/admin/
- Login with your superuser credentials

### 2. Create a Faculty User (Optional)
- In admin panel, go to Users
- Add a new user with faculty role

### 3. Create Your First Course
- From main app, go to "Courses" → "Add Course"
- Fill in: Course Code (e.g., CSE101), Course Name, Faculty

### 4. Register Students
- Go to "Students" → "Add Student"
- Fill in student details
- **Upload a clear face photo** (very important for face recognition)
- The system will automatically generate face encoding

### 5. Create an Attendance Session
- Go to "Sessions" → "New Session"
- Select course, date, time, and type
- Submit to create session

### 6. Mark Attendance
- Click "Mark Attendance" on your session
- Try both methods:
  - **Face Recognition**: Upload a photo of the student
  - **Manual Selection**: Check boxes for present students

## 🔧 Troubleshooting Common Issues

### Issue 1: Cannot install face_recognition

**Error**: "Could not find a version that satisfies the requirement face_recognition"

**Solution**:
1. Install CMake first: `pip install cmake`
2. Install dlib separately: `pip install dlib`
3. Then install face_recognition: `pip install face-recognition`

### Issue 2: ModuleNotFoundError

**Error**: "No module named 'django'"

**Solution**: Make sure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue 3: Port 8000 already in use

**Error**: "That port is already in use"

**Solution**: Run on a different port
```bash
python manage.py runserver 8080
```

### Issue 4: Face not detected in photo

**Reasons**:
- Photo quality too low
- Face not clearly visible
- Poor lighting
- Multiple faces in photo

**Solution**:
- Use a high-quality, well-lit photo
- Face should be centered and looking at camera
- Only one person in the photo
- Remove glasses if possible

### Issue 5: Database is locked

**Error**: "database is locked"

**Solution**: Close any other instances of the app and try again

## 📱 Testing Face Recognition

### Good Test Photos:
1. **Resolution**: At least 640x480 pixels
2. **Lighting**: Even, natural lighting
3. **Background**: Plain, uncluttered
4. **Face**: Centered, looking directly at camera
5. **Expression**: Neutral or slight smile

### Test Workflow:
1. Register a student with a good quality photo
2. Create an attendance session
3. Take another photo of the same student (different angle/lighting)
4. Upload via "Face Recognition" method
5. System should identify the student with confidence score

## 🎨 Customization Tips

### Change Recognition Tolerance
Edit `attendance_system/settings.py`:
```python
FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = more strict (0.0-1.0)
```

### Change Detection Model
Edit `attendance_system/settings.py`:
```python
FACE_RECOGNITION_MODEL = 'hog'  # 'hog' (faster) or 'cnn' (accurate)
```

### Change Colors
Edit `core/templates/core/base.html` CSS variables:
```css
:root {
    --primary: #6366f1;  /* Change primary color */
    --secondary: #10b981;  /* Change secondary color */
}
```

## 📊 Sample Data (Optional)

Want to test with sample data?

### Create Sample Course:
- Course Code: CSE101
- Course Name: Python Programming
- Faculty: Admin

### Create Sample Students:
1. Registration: 12345678, Name: John Doe
2. Registration: 12345679, Name: Jane Smith
3. Registration: 12345680, Name: Bob Johnson

Make sure to upload clear photos for each!

## 🚀 Production Deployment

For production use:

1. **Set Debug to False**
   ```python
   DEBUG = False
   ```

2. **Use PostgreSQL** instead of SQLite
3. **Configure Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Use Gunicorn/uWSGI** as WSGI server
5. **Setup Nginx** as reverse proxy
6. **Enable HTTPS** with SSL certificate
7. **Setup Backup System** for database

## 📞 Need Help?

- Check README.md for detailed documentation
- Review code comments for implementation details
- Test with sample data first
- Make sure all prerequisites are installed

## 🎓 Project Submission Checklist

- [ ] Code runs without errors
- [ ] Face recognition working
- [ ] All features tested
- [ ] README.md completed
- [ ] Comments added to code
- [ ] Screenshots taken
- [ ] Video recorded (OBS Studio)
- [ ] Blog written (Medium)
- [ ] GitHub repository created
- [ ] All files committed

## 💡 Tips for Success

1. **Start Early**: Don't wait until the deadline
2. **Test Thoroughly**: Try all features multiple times
3. **Document Everything**: Take screenshots of each feature
4. **Understand the Code**: Don't just copy-paste
5. **Ask Questions**: If stuck, ask faculty for help

---

**Happy Coding! 🎉**

Made with ❤️ for LPU Project II
