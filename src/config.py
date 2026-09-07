# Modified: repository cleanup and reliability fixes, September 2026.
import os
import cv2

# Base directory (parent of src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory paths
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ASSETS_DIR = os.path.join(BASE_DIR, "src", "assets")

# Ensure all directories exist
for dir_path in [DATASET_DIR, ATTENDANCE_DIR, LOGS_DIR, ASSETS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Image and photo settings
PHOTO_SIZE = (200, 200)
DEFAULT_PHOTOS = 15

# Haar cascade path
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Window settings
WIN_W, WIN_H = 900, 600

# Button settings
BTN_FONT = ("Segoe UI", 13, "bold")
BTN_BG = "#0078D7"
BTN_ACTIVE = "#005a9e"
BTN_FG = "white"
BTN_W = 22
BTN_H = 2

# Login settings
LOGIN_FILE = os.path.join(BASE_DIR, "users.json")

# Attendance settings
ATTENDANCE_COLUMNS = ["Name", "Time", "Teacher", "Status"]

# File paths
def get_asset_path(filename):
    """Get full path for an asset file"""
    return os.path.join(ASSETS_DIR, filename)

def get_attendance_path(date):
    """Get full path for an attendance file"""
    return os.path.join(ATTENDANCE_DIR, f"attendance_{date}.csv")

def get_student_path(name, teacher=None):
    """Get full path for a student's directory"""
    if teacher:
        return os.path.join(DATASET_DIR, f"{name}_{teacher}")
    return os.path.join(DATASET_DIR, name)

# GUI Theme settings
THEME = {
    'primary': '#0078D7',
    'primary_dark': '#005a9e',
    'background': '#f4f6f9',
    'text': '#333333',
    'text_light': '#ffffff',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545'
}

# Recognition settings
FACE_RECOGNITION_SETTINGS = {
    'scale_factor': 1.1,
    'min_neighbors': 5,
    'confidence_threshold': 80,
    'frame_resize_factor': 0.25
}

# Logging settings
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOGS_DIR, 'attendance_system.log')

# Export settings
EXCEL_SETTINGS = {
    'default_sheet': 'Attendance',
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S'
}

# System messages
MESSAGES = {
    'no_camera': "Could not access camera. Please check your camera connection.",
    'no_face': "No face detected. Please ensure proper lighting and positioning.",
    'training_error': "Error during training. Please check the dataset.",
    'success': "Operation completed successfully.",
    'unknown_error': "An unexpected error occurred. Please try again."
}

# Version info
VERSION = "1.0.0"
SYSTEM_NAME = "Smart Face Recognition Attendance System"

def init():
    """Initialize configuration and create necessary directories"""
    # Create required directories
    for dir_path in [DATASET_DIR, ATTENDANCE_DIR, LOGS_DIR, ASSETS_DIR]:
        os.makedirs(dir_path, exist_ok=True)

    # Verify Haar cascade file
    if not os.path.exists(HAAR_PATH):
        raise FileNotFoundError(f"Haar cascade file not found at {HAAR_PATH}")

    return True

# Initialize configuration when module is imported
if __name__ != "__main__":
    init()
