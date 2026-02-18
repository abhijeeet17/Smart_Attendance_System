# Troubleshooting Guide - Common Setup Errors

## Error 1: "You have 19 unapplied migration(s)"

### The Error
```
You have 19 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, attendance, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

### What This Means
Django needs to create database tables for the application to work. Without migrations, the database is empty and the app won't function.

### Solution
Open your terminal in the project directory and run:

```bash
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying core.0001_initial... OK
```

### After Running Migrations
- Restart your server: `python manage.py runserver 2000`
- The 404 error should be fixed
- You can now access the application

---

## Error 2: "Page not found (404)"

### The Error
```
Page not found (404)
Request URL: http://127.0.0.1:2000/
```

### Common Causes

#### Cause 1: Migrations Not Applied
**Check**: Have you run `python manage.py migrate`?

**Solution**: Run migrations first (see Error 1 above)

#### Cause 2: Server Not Running Properly
**Check**: Is the server running without errors?

**Solution**: 
1. Stop the server (Ctrl+C)
2. Run migrations: `python manage.py migrate`
3. Restart server: `python manage.py runserver 2000`

#### Cause 3: Wrong URL
**Check**: Are you using the correct URL?

**Correct URLs**:
- Homepage: `http://127.0.0.1:2000/`
- Dashboard: `http://127.0.0.1:2000/dashboard/`
- Students: `http://127.0.0.1:2000/students/`
- Admin: `http://127.0.0.1:2000/admin/`

---

## Error 3: Course Dropdown Empty

### The Problem
When trying to register a student, the Course dropdown shows no options.

### Why This Happens
No courses have been created in the database yet.

### Solution

**Option 1: Using Web Interface**
1. Run migrations if you haven't: `python manage.py migrate`
2. Start server: `python manage.py runserver 2000`
3. Go to: `http://127.0.0.1:2000/courses/`
4. Click "Create Course"
5. Fill in:
   - Course Code (e.g., CS101)
   - Course Name (e.g., Introduction to Programming)
   - Faculty (select a user)
6. Click Save
7. Now go to student registration - courses should appear

**Option 2: Using Django Admin**
1. Create superuser: `python manage.py createsuperuser`
2. Go to: `http://127.0.0.1:2000/admin/`
3. Login with superuser credentials
4. Click on "Courses"
5. Click "Add Course"
6. Fill in details and save

**Option 3: Using Django Shell (Quick)**
```bash
python manage.py shell
```

Then run:
```python
from core.models import Course
from django.contrib.auth.models import User

# Create a user first (if none exists)
user = User.objects.create_user(username='admin', password='admin123')

# Create a course
Course.objects.create(
    course_code='CS101',
    course_name='Introduction to Programming',
    faculty=user
)

# Verify
print(Course.objects.all())
# Exit
exit()
```

---

## Error 4: "No module named 'PIL'" or "No module named 'face_recognition'"

### The Error
```
ModuleNotFoundError: No module named 'PIL'
```
or
```
ModuleNotFoundError: No module named 'face_recognition'
```

### Solution
Install required packages:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Django
pip install Pillow
pip install face-recognition
pip install opencv-python-headless
```

---

## Error 5: Camera Access Issues

### Problem: Camera Won't Start

#### Cause 1: Browser Permissions
**Solution**: 
1. Click the camera icon in browser address bar
2. Allow camera access
3. Refresh the page

#### Cause 2: Camera In Use
**Solution**: 
- Close other applications using camera (Zoom, Skype, etc.)
- Try again

#### Cause 3: No HTTPS
**Solution**: 
- Use `localhost` or `127.0.0.1` (these work without HTTPS)
- Or set up HTTPS for your development server

#### Cause 4: Browser Compatibility
**Solution**: 
- Use Chrome, Firefox, or Edge (latest versions)
- Avoid Internet Explorer

---

## Error 6: "CSRF verification failed"

### The Error
```
CSRF verification failed. Request aborted.
```

### Solution
This usually happens if you're trying to submit a form without the CSRF token.

**Fix**: 
1. Clear browser cookies
2. Refresh the page
3. Try submitting again

If still an issue:
1. Check that `{% csrf_token %}` is present in forms
2. Ensure `django.middleware.csrf.CsrfViewMiddleware` is in `MIDDLEWARE` in settings.py

---

## Error 7: Static Files Not Loading

### Problem
CSS and JavaScript files aren't loading, page looks broken.

### Solution

**Step 1**: Check DEBUG setting
In `attendance_system/settings.py`:
```python
DEBUG = True  # Make sure this is True for development
```

**Step 2**: Collect static files
```bash
python manage.py collectstatic
```

**Step 3**: Check STATIC_URL in settings
```python
STATIC_URL = '/static/'
```

**Step 4**: Restart server
```bash
python manage.py runserver 2000
```

---

## Error 8: "Face not detected" During Registration

### Problem
When capturing photo, system says "No face detected"

### Causes and Solutions

#### Cause 1: Poor Lighting
**Solution**: 
- Move to well-lit area
- Face a window or lamp
- Avoid backlighting

#### Cause 2: Face Not Visible
**Solution**: 
- Remove hat, mask, sunglasses
- Face camera directly
- Move closer to camera

#### Cause 3: Camera Quality
**Solution**: 
- Use better quality webcam
- Clean camera lens
- Ensure camera is working (test in other apps)

---

## Error 9: Database Locked

### The Error
```
sqlite3.OperationalError: database is locked
```

### Solution
1. Close all terminal windows running the server
2. Make sure no other process is using the database
3. Delete `db.sqlite3.lock` if it exists
4. Restart the server

---

## Error 10: Port Already In Use

### The Error
```
Error: That port is already in use.
```

### Solution

**Option 1**: Use different port
```bash
python manage.py runserver 3000
```

**Option 2**: Kill process using port 2000
```bash
# Windows
netstat -ano | findstr :2000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:2000 | xargs kill -9
```

---

## Complete Setup Checklist

Use this checklist to ensure proper setup:

- [ ] Python installed (3.8 or higher)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Static files collected (if needed)
- [ ] At least one course created
- [ ] Server running without errors
- [ ] Can access homepage at `http://127.0.0.1:2000/`
- [ ] Camera permissions granted in browser

---

## Quick Commands Reference

### Setup Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver 2000
```

### Useful Commands
```bash
# Check migrations status
python manage.py showmigrations

# Create new migrations (if models changed)
python manage.py makemigrations

# Access Django shell
python manage.py shell

# Check for issues
python manage.py check
```

---

## Getting More Help

### Check These Files
1. `QUICKSTART.md` - Quick setup guide
2. `SETUP_GUIDE.md` - Detailed setup instructions
3. `IMPLEMENTATION_GUIDE.md` - Developer guide
4. `README.md` - Project overview

### Common Questions

**Q: Where is the database file?**
A: It's `db.sqlite3` in your project root directory.

**Q: How do I reset the database?**
A: Delete `db.sqlite3` and run `python manage.py migrate` again.

**Q: How do I change the port?**
A: Run `python manage.py runserver PORT_NUMBER`

**Q: Can I use a real database instead of SQLite?**
A: Yes, configure PostgreSQL or MySQL in `settings.py`

**Q: How do I access admin panel?**
A: Go to `http://127.0.0.1:2000/admin/` after creating a superuser.

---

## Still Having Issues?

If you're still experiencing problems:

1. **Check the terminal output** for error messages
2. **Check browser console** (F12 → Console tab)
3. **Verify all files are present** in the project directory
4. **Try deleting db.sqlite3** and running migrations again
5. **Check if all dependencies are installed**: `pip list`
6. **Ensure Python version** is 3.8 or higher: `python --version`

---

Last Updated: February 12, 2026
