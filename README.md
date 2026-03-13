# Smart AI-Enabled Attendance System with Face Recognition

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern, AI-powered attendance management system built with Django that uses face recognition technology to automate attendance marking. Designed for campus attendance management systems.

---

## 🎯 Project Overview

This Smart Attendance System leverages face recognition technology to provide seamless, contactless attendance management.
The system eliminates manual attendance marking, reduces administrative workload, and provides real-time attendance tracking.

---

## ✨ Key Features

### 1️⃣ AI-Powered Face Recognition

* Automatic face encoding generation during student registration
* High-accuracy face matching using `face_recognition`
* Confidence score reporting
* Support for HOG/CNN detection models

### 2️⃣ Smart Attendance Management

* One-click attendance marking
* Face recognition attendance mode
* Manual attendance marking option
* Real-time attendance updates

### 3️⃣ Dashboard

* Total students
* Courses
* Sessions
* Recent attendance sessions

### 4️⃣ Student Management

* Student registration with photo upload
* Face encoding generation
* Student attendance history
* Attendance percentage tracking

### 5️⃣ Course & Session Management

* Multiple courses
* Lecture/Lab/Tutorial sessions
* Faculty assignment
* Session-wise attendance

### 6️⃣ Reports

* Course-wise attendance
* Student attendance history
* Date filtering
* Export-ready reports

---

## 🛠 Technology Stack

Backend: Django 4.2
Language: Python 3.8+
Database: SQLite / PostgreSQL
Face Recognition: face_recognition (dlib)
Image Processing: OpenCV, Pillow
Frontend: HTML, CSS, JavaScript

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/abhijeeet17/Smart_Attendance_System.git
cd smart_attendance_system
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create admin

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

---

## 📁 Project Structure

```
smart_attendance_system
│
├── attendance_system
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── core
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── face_recognition_utils.py
│
├── media
├── staticfiles
├── requirements.txt
├── manage.py
```

---

## 🔐 Security

* Face encodings stored as vectors
* CSRF protection enabled
* Django password hashing
* Admin authentication

---

## 📊 Future Improvements

* Live webcam recognition
* Mobile app
* SMS/email notifications
* Advanced analytics
* LMS integration

---

## 📄 License

Educational project for university coursework.

---

## ✍️ Articles & Project Blogs

Smart Food Pre-Ordering System
https://medium.com/@sharmaabhijeet317/️-smart-food-pre-ordering-system-revolutionizing-the-lpu-campus-dining-experience-e1693d9ae748

Campus Resource Platform
https://medium.com/@sharmaabhijeet317/0d24e7df43e0

Building Make-up Class System
https://medium.com/@sharmaabhijeet317/8382d1016c4a

ASCII Art Generator (Python)
https://medium.com/@sharmaabhijeet317/ascii-art-generator-using-python-raw-arrays-approach-3944fc482f77

Smart AI Attendance System
https://medium.com/@sharmaabhijeet317/smart-ai-enabled-attendance-system-with-face-recognition-452898941fb3

IVY League Analysis
https://medium.com/@sharmaabhijeet317/7341575bf70e

---

Made with ❤️ by **Abhijeet Sharma**
