# Modified: repository cleanup and reliability fixes, September 2026.
import os, re, cv2, datetime
import json
import shutil
import uuid
from tkinter import simpledialog, messagebox
from student_metadata import read_student
from config import DATASET_DIR, PHOTO_SIZE, DEFAULT_PHOTOS, HAAR_PATH

face_cascade = cv2.CascadeClassifier(HAAR_PATH)

def sanitize_name(name: str) -> str:
    """Clean and format the student name"""
    return re.sub(r"[^\w\- ]", "", name.strip()).replace(" ", "_")

def add_student(parent=None, teacher=None):
    """Add a new student with photos"""
    raw_name = simpledialog.askstring("Add Student", "Enter student name:", parent=parent)
    if not raw_name: 
        return

    name = sanitize_name(raw_name)
    if not name:
        messagebox.showerror("Invalid", "Name cannot be empty", parent=parent)
        return

    # Check if student already exists
    existing_students = os.listdir(DATASET_DIR)
    for student in existing_students:
        folder = os.path.join(DATASET_DIR, student)
        if not os.path.isdir(folder):
            continue
        info = read_student(folder)
        if info["name"].casefold() == raw_name.strip().casefold() and info["teacher"] == (teacher or "Unknown"):
            if not messagebox.askyesno("Warning", 
                                     f"Student '{name}' already exists. Add another entry?",
                                     parent=parent):
                return

    num_photos = simpledialog.askinteger("Photos", 
                                        "How many photos? (5-50)", 
                                        initialvalue=DEFAULT_PHOTOS,
                                        minvalue=5, 
                                        maxvalue=50,
                                        parent=parent)
    if not num_photos: 
        return

    # Create directory for new student
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    person_dir = os.path.join(DATASET_DIR, uuid.uuid4().hex)
    
    os.makedirs(person_dir, exist_ok=False)
    with open(os.path.join(person_dir, "student.json"), "w", encoding="utf-8") as file:
        json.dump({"name": raw_name.strip(), "teacher": teacher or "Unknown", "created": timestamp}, file)

    # Start photo capture
    if capture_photos(person_dir, num_photos, parent):
        messagebox.showinfo("Success", 
                          f"Successfully added {name} with {num_photos} photos", 
                          parent=parent)
    else:
        # Cleanup if failed
        try:
            shutil.rmtree(person_dir)
        except:
            pass

def capture_photos(person_dir, num_photos, parent=None):
    """Capture photos for a student"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera. Please check your camera connection.", parent=parent)
        return False

    photos_taken = 0
    
    try:
        # Create window
        cv2.namedWindow("Capture Photos", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Capture Photos", 800, 600)
    
        while photos_taken < num_photos:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Camera Error", "Camera stopped providing frames.", parent=parent)
                break
    
            # Create copy for display
            display_frame = frame.copy()
            
            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
            # Process detected faces
            for (x, y, w, h) in (faces if len(faces) == 1 else []):
                # Draw rectangle around face
                cv2.rectangle(display_frame, (x,y), (x+w,y+h), (0,255,0), 2)
    
                # Save face image
                face = gray[y:y+h, x:x+w]
                try:
                    face = cv2.resize(face, PHOTO_SIZE)
                    filename = os.path.join(person_dir, f"photo_{photos_taken+1}.jpg")
                    if cv2.imwrite(filename, face):
                        photos_taken += 1
                except Exception as e:
                    print(f"Error saving photo: {e}")
                    continue
    
            # Show progress
            cv2.putText(display_frame, 
                        f"Photos: {photos_taken}/{num_photos}", 
                        (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (0, 255, 0), 
                        2)
            
            # Show instructions
            cv2.putText(display_frame,
                        "Press 'q' to quit", 
                        (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2)
    
            # Show frame
            cv2.imshow("Capture Photos", display_frame)
    
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

    # Only retain complete enrollment sessions
    return photos_taken == num_photos

if __name__ == "__main__":
    # Test the module
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
    add_student()
