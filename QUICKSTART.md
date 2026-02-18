# Quick Setup Instructions for Smart Attendance System

## Step 1: Run Database Migrations

First, you need to apply the database migrations. Run these commands in your terminal:

```bash
# Navigate to your project directory
cd C:\Users\LENOVO\OneDrive\Desktop\smart\smartattnd

# Apply migrations
python manage.py migrate
```

This will create all the necessary database tables.

## Step 2: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: (enter your username)
- Email: (enter your email)
- Password: (enter password)
- Password (again): (confirm password)

## Step 3: Start the Development Server

```bash
python manage.py runserver 2000
```

The server will start at: http://127.0.0.1:2000/

## Step 4: Access the Application

Open your browser and go to:
- **Homepage**: http://127.0.0.1:2000/
- **Admin Panel**: http://127.0.0.1:2000/admin/
- **Dashboard**: http://127.0.0.1:2000/dashboard/
- **Register Students**: http://127.0.0.1:2000/students/register/

## Step 5: Create Initial Data

### Option A: Using Django Admin
1. Go to http://127.0.0.1:2000/admin/
2. Login with your superuser credentials
3. Create:
   - Faculty users (if needed)
   - Courses (required before registering students)

### Option B: Using the Web Interface
1. Go to http://127.0.0.1:2000/
2. Navigate to "Courses"
3. Click "Create Course"
4. Fill in course details and save

## Common Issues and Solutions

### Issue 1: Migrations Error
**Error**: "You have 19 unapplied migration(s)"

**Solution**:
```bash
python manage.py migrate
```

### Issue 2: Page Not Found (404)
**Error**: "Page not found (404)"

**Solution**: Make sure you've run migrations and are accessing the correct URL:
- Root URL: http://127.0.0.1:2000/ (should work after migrations)
- If still issues, check that the server is running

### Issue 3: No Courses in Dropdown
**Problem**: Course dropdown is empty when registering students

**Solution**: Create courses first:
1. Go to http://127.0.0.1:2000/courses/
2. Click "Create Course"
3. Add course details
4. Then try registering students

### Issue 4: Static Files Not Loading
**Problem**: CSS/JS not loading properly

**Solution**:
```bash
python manage.py collectstatic
```

Then restart the server.

### Issue 5: Camera Not Working
**Problem**: Webcam doesn't start

**Solution**:
- Check browser permissions (allow camera access)
- Use HTTPS or localhost
- Try a different browser (Chrome recommended)
- Check if camera is being used by another application

## Quick Test Workflow

After setup, test the system:

1. **Create a Course**:
   - Go to Courses → Create Course
   - Fill in: Course Code, Course Name, Faculty
   - Save

2. **Register a Student**:
   - Go to Students → Register
   - Fill in student details
   - Click "Start Camera"
   - Capture photo
   - Submit

3. **Create Attendance Session**:
   - Go to Sessions → Create Session
   - Select course, date, time
   - Save

4. **Mark Attendance**:
   - Go to Sessions → Select session
   - Click "Face Recognition"
   - Start camera
   - Capture photo
   - Click "Recognize & Mark Attendance"

## Directory Structure

Your project should look like this:

```
smartattnd/
├── manage.py
├── attendance_system/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── media/
│   ├── student_photos/
│   └── attendance_photos/
└── db.sqlite3 (created after migrations)
```

## Important Notes

1. **Always run migrations** after extracting the project:
   ```bash
   python manage.py migrate
   ```

2. **Create superuser** to access admin:
   ```bash
   python manage.py createsuperuser
   ```

3. **Create courses first** before registering students

4. **Grant camera permissions** in browser when prompted

5. **Use good lighting** for better face recognition accuracy

## Next Steps

Once setup is complete:
1. Create faculty accounts (if needed)
2. Create courses
3. Register students with webcam
4. Create attendance sessions
5. Mark attendance using face recognition

## Support

If you encounter any issues:
1. Check the terminal for error messages
2. Check browser console for JavaScript errors
3. Verify all migrations are applied: `python manage.py showmigrations`
4. Ensure courses exist before registering students
5. Refer to documentation files in the project

## Documentation Files

- `README.md` - Project overview
- `SETUP_GUIDE.md` - Detailed setup instructions
- `UPDATED_FEATURES.md` - Webcam registration features
- `WEBCAM_ATTENDANCE_GUIDE.md` - Attendance marking guide
- `IMPLEMENTATION_GUIDE.md` - Developer guide
- `CHANGES_SUMMARY.md` - Complete changelog

---

For detailed information, refer to the documentation files included in the project.
