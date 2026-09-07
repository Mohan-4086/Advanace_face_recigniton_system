# Modified: repository cleanup and reliability fixes, September 2026.
import os
import cv2
import numpy as np
from tkinter import messagebox
from config import DATASET_DIR, PHOTO_SIZE, HAAR_PATH
from attendance import mark_attendance
from student_metadata import read_student

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(HAAR_PATH)

# ------------------- Training -------------------
def train_recognizer(teacher=None):
    """Train LBPH recognizer on dataset"""
    faces, labels, label_map = [], [], {}
    label_id = 0

    for person in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person)
        if not os.path.isdir(person_dir):
            continue
        if teacher and read_student(person_dir)["teacher"] != teacher:
            continue
        before = len(faces)
        for file in os.listdir(person_dir):
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(person_dir, file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            try:
                img = cv2.resize(img, PHOTO_SIZE)
                faces.append(img)
                labels.append(label_id)
            except Exception as e:
                print(f"Skipping {path}: {e}")
                continue
        if len(faces) > before:  # Only map a label with valid images
            label_map[label_id] = person
            label_id += 1

    if not faces:
        messagebox.showerror("Training Error", "No training data found!\nPlease add students first.")
        return None, {}

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    return recognizer, label_map

# ------------------- Recognition -------------------
def start_recognition(parent=None, teacher=None):
    """Start webcam face recognition"""
    print("[INFO] Starting recognition...")
    recognizer, label_map = train_recognizer(teacher)
    if not recognizer:
        print("[ERROR] Training failed. No recognizer created.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Could not open webcam.", parent=parent)
        return

    messagebox.showinfo("Recognition", "Press 'q' to quit recognition.", parent=parent)
    marked = set()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Camera Error", "Camera stopped providing frames.", parent=parent)
                break
    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
            for (x, y, w, h) in faces:
                face = cv2.resize(gray[y:y+h, x:x+w], PHOTO_SIZE)
                label, conf = recognizer.predict(face)
                name = label_map.get(label, "Unknown")
    
                # Extract student name from directory name (remove teacher prefix if exists)
                display_name = read_student(os.path.join(DATASET_DIR, name))["name"]
    
                if conf < 80:  # Lower conf = better match
                    cv2.putText(frame, f"{display_name} ({int(conf)})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
                    # Mark attendance only once per session
                    if name not in marked:
                        mark_attendance(display_name, teacher, student_id=name)
                        marked.add(name)
                        print(f"[INFO] Attendance marked for {display_name}")
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
            # Add teacher name to frame if provided
            if teacher:
                cv2.putText(frame, f"Teacher: {teacher}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
            cv2.imshow("Face Recognition", frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

    print("[INFO] Recognition stopped.")

def get_face_encoding(image_path):
    """Get face encoding from image path"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces) == 0:
            return None
        x, y, w, h = faces[0]
        face = cv2.resize(gray[y:y+h, x:x+w], PHOTO_SIZE)
        return face
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None
