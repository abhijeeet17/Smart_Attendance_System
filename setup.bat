@echo off
echo ========================================
echo Smart Attendance System - Quick Setup
echo ========================================
echo.

echo Step 1: Applying database migrations...
python manage.py migrate
echo.

if %errorlevel% neq 0 (
    echo ERROR: Migration failed!
    echo Please check if Python is installed and you're in the correct directory.
    pause
    exit /b 1
)

echo ========================================
echo Migrations completed successfully!
echo ========================================
echo.

echo Step 2: Would you like to create a superuser account? (y/n)
set /p create_superuser=Enter choice: 

if /i "%create_superuser%"=="y" (
    echo.
    echo Creating superuser account...
    python manage.py createsuperuser
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.

echo Next steps:
echo 1. Start the server: python manage.py runserver 2000
echo 2. Open browser: http://127.0.0.1:2000/
echo 3. Create courses before registering students
echo.

echo Would you like to start the server now? (y/n)
set /p start_server=Enter choice: 

if /i "%start_server%"=="y" (
    echo.
    echo Starting server at http://127.0.0.1:2000/
    echo Press Ctrl+C to stop the server
    echo.
    python manage.py runserver 2000
) else (
    echo.
    echo Setup complete! Run 'python manage.py runserver 2000' when ready.
    pause
)
