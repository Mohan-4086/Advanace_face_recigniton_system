# Face Recognition Attendance System

A smart attendance management system using facial recognition technology. This system allows administrators to manage teachers and students, while enabling automated attendance tracking through face detection and recognition.

##Important Notes


Ensure proper lighting for accurate face detection
Keep face straight while capturing photos
Multiple photos per student recommended for better accuracy
Regular updates to student photos recommended
Troubleshooting
If camera not detected, check device connections
For recognition issues, try updating student photos
Ensure all required libraries are properly installed
Check file permissions if getting access errors
Security Features
Password-protected access
Role-based permissions
Secure password storage
Session management
System Requirements
Windows/Linux/MacOS
Webcam or USB camera
Minimum 4GB RAM
Processor: Intel i3 or equivalent
Storage: 1GB free space

## Features

### Admin Panel
- Add and manage teachers
- Reset teacher passwords
- View and manage system users
- Access attendance records
- Change admin password

### Teacher Features
- Add new students
- Take attendance using face recognition
- View attendance records
- Generate attendance reports

### System Features
- Real-time face detection
- Automated attendance marking
- Secure login system
- User-friendly interface
- Attendance history tracking

## Installation

### Prerequisites
- Python 3.9 or higher
- OpenCV
- face_recognition library
- tkinter (usually comes with Python)
- PIL (Python Imaging Library)

### Required Libraries
```bash
pip install opencv-python
pip install face-recognition
pip install Pillow
pip install numpy
pip install pandas

Directory Structure

─Advance_face_Recognition
    ├───assets
    ├───attendance
    ├───data
    │   └───attendance
    ├───dataset
    │   ├───ITESH_PAL
    │   ├───mohan 1
    │   └───MOHAN_PAL
    ├───logs
    ├───readme
    ├───src
    │   attendance.csv
    │   attendance.py
    │   config.py
    │   dlib-19.22.99-cp39-cp39-win_amd64.whl
    │   face_utils.py
    │   login.py
    │   main.py
    │   manage_students.py
    │   student.py
    │   users.json
    │   window_utils.py
    │
    ├───assets
    │       background.jpg
    │       banner.png
    │       logo.png
    │
    ├───attendance
    ├───dataset
    ├───test
    └───venv
        


Running the System

Navigate to the project directory
Run the main script:
Bash

python src/main.py
Default Login Credentials
text

Admin:
Username: admin
Password: admin123

Teacher:
Username: teacher1
Password: teacher123

Basic Workflow

Admin logs in and adds teachers

Teachers can then log in and:

Add students
Take attendance
View records
System automatically marks attendance using face recognition



Contributing
Feel free to fork this project and submit pull requests for any improvements.



Acknowledgments
OpenCV team for computer vision library
face_recognition library developers
Python community for various tools and libraries
text



