<p align="center">
  <img src="docs/banner.svg" alt="Face Recognition Attendance System" width="100%">
</p>

<p align="center">
  <strong>A desktop attendance application built with Python and OpenCV.</strong><br>
  Student enrollment, webcam recognition and daily reports in one interface.
</p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="docs/SETUP.md">Full setup guide</a> ·
  <a href="#project-structure">Project structure</a>
</p>

---

## Overview

This project brings student enrollment and face-based attendance into a desktop workflow. Administrators manage teacher accounts; teachers capture student photos, run webcam recognition, and review or export attendance records.

**Built by [Mohan](https://github.com/Mohan-4086)** · Python desktop project · [Apache 2.0 license](LICENSE)

## Features

| Feature | What it does |
| --- | --- |
| **Account management** | Administrator setup, teacher accounts and password management |
| **Student enrollment** | Webcam photo capture with full names and teacher ownership |
| **Face recognition** | Haar cascade detection and OpenCV LBPH recognition |
| **Attendance tracking** | Daily CSV records with duplicate prevention |
| **Student management** | Browse and remove enrolled students |
| **Reports & export** | View attendance by date and export to Excel |

## Technology

| Layer | Tools |
| --- | --- |
| Application | Python |
| Desktop interface | Tkinter, Pillow |
| Computer vision | OpenCV contrib, NumPy |
| Reports | pandas, openpyxl |
| Local storage | JSON, CSV and student images |

## Quick start

You need Python with Tkinter, a desktop display and a webcam. See the [full setup guide](docs/SETUP.md) for environment activation and troubleshooting.

```sh
git clone --depth 1 https://github.com/Mohan-4086/Advanace_face_recigniton_system.git
cd Advanace_face_recigniton_system
python -m venv .venv
```

Activate the environment:

| System | Command |
| --- | --- |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

```sh
python -m pip install -r requirements.txt
python src/login.py
```

At first launch, choose a password for the **admin** account. Use the admin panel to create teacher accounts.

## Using the application

1. **Sign in** — create teacher accounts from the admin panel.
2. **Enroll students** — enter each student's full name and capture photos.
3. **Start recognition** — keep the face visible and press **q** to stop.
4. **Review attendance** — select a date, inspect records and export to Excel.

## Project structure

| Location | Contents |
| --- | --- |
| `src/` | Application code |
| `src/assets/` | Interface images |
| `docs/` | Setup guide and README banner |
| `tests/` | Automated regression tests |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Rules excluding local and generated files |

Accounts, enrolled photos and attendance records are created locally and excluded from commits.

## Validation

Regression tests and Python compilation pass. Dependency installation, module imports, cascade loading, synthetic LBPH training/prediction and an Excel write/read check have also passed on Python 3.12.

```sh
python -m unittest discover -s tests -v
```

Live webcam accuracy and visual GUI behavior still need desktop testing. This is an educational prototype; no recognition accuracy percentage or liveness detection is claimed.

<details>
<summary><strong>Existing users: data and migration notes</strong></summary>

Back up local data before pulling the cleanup changes. Existing student folders without metadata need re-enrollment under the correct teacher. Previously committed data remains in earlier Git history.

See the [setup and limitations guide](docs/SETUP.md) for details.

</details>

## License & acknowledgments

Released under the [Apache License 2.0](LICENSE). Built using Python, OpenCV, NumPy, Tkinter, Pillow, pandas and openpyxl.
