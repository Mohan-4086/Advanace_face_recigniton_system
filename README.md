# Face Recognition Attendance System

A Python desktop project for enrolling students from a webcam and recording attendance with OpenCV's LBPH recognizer. Includes a Tkinter interface, administrator and teacher accounts, daily CSV records, and Excel export.

## Features

- First-run administrator setup and salted PBKDF2 password hashing.
- Administrator tools to add teachers, reset passwords and manage accounts.
- Student enrollment with full names and explicit teacher ownership.
- Webcam face detection with Haar cascades and LBPH recognition.
- One attendance record per student, teacher and day, including after restarting recognition.
- Date-based attendance viewer and Excel export.

## Setup

Use Python **3.11** with Tkinter, a desktop display and a working webcam. Python's Windows installer normally includes Tkinter. Linux may require your distribution's `python3-tk` package. Other Python versions and operating systems have not been validated here.

```sh
git clone --depth 1 https://github.com/Mohan-4086/Advanace_face_recigniton_system.git
cd Advanace_face_recigniton_system
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```sh
source .venv/bin/activate
```

Install and launch:

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/login.py
```

Install into a fresh environment. The application needs **opencv-contrib-python** for `cv2.face`; do not install multiple OpenCV variants together. Neither dlib nor the `face_recognition` package is used.

## First use

1. Choose your own administrator password at the first-run prompt. The username is `admin`; there are no default passwords.
2. Sign in and use **Add New Teacher** to create an account.
3. Log out and sign in as that teacher.
4. Select **Add Student**, enter the full name and capture the requested photos with only one person in view.
5. Select **Start Recognition**. Press **q** to stop the camera session.
6. Open **Show Attendance** to view or export daily records.

Use varied poses and good lighting during enrollment. Enrollment is cancelled if the requested number of photos is not captured. Each teacher recognizes and manages their own enrolled students. The administrator's attendance dashboard uses its own account scope.

## Project layout

| Path | Purpose |
| --- | --- |
| `src/login.py` | Login, first-run setup and administrator tools |
| `src/main.py` | Attendance dashboard |
| `src/student.py`, `src/student_metadata.py` | Enrollment and student identity |
| `src/manage_students.py` | Student listing and deletion |
| `src/face_utils.py` | Training and webcam recognition |
| `src/attendance.py` | Daily records, viewer and export |
| `src/auth.py` | Password hashing and verification |
| `src/config.py` | Portable paths and settings |
| `src/assets/` | Existing interface images |
| `tests/` | Automated regression tests |

The app creates local `dataset/`, `attendance/`, `logs/` and `users.json` as needed. These are ignored by Git. The repository intentionally includes no enrolled faces or live accounts. Legacy root-level plaintext passwords are upgraded on login startup. Old student folders without `student.json` retain their full folder names but have unknown ownership; re-enroll those students under the correct teacher. Back up local data before switching to the cleanup branch.

## Testing and limitations

```sh
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

Automated tests cover password verification, student metadata and attendance recording without a webcam. Camera accuracy, lighting, real GUI interactions and Excel export still need a desktop smoke test. No recognition accuracy percentage is claimed. The threshold is a heuristic and LBPH distance is not a probability.

Camera operations run on the UI thread to avoid unsafe Tkinter calls from background threads; dashboard interaction pauses while a camera session runs. This is a local educational prototype, with no liveness detection or protection against someone who can directly edit local files. It is not ready for high-stakes identity verification.

## Data and repository cleanup

Face photos, account records, attendance exports, virtual environments, caches and bundled wheels must stay out of commits. Removing previously tracked files in this branch does **not** erase earlier Git history, existing clones or copies. A history rewrite is a separate coordinated operation. A shallow clone avoids downloading the old history after these changes are merged.

## License

[Apache License 2.0](LICENSE). Uses OpenCV, NumPy, pandas, Pillow, openpyxl and Python/Tkinter.
