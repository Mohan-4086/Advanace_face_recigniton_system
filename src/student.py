import os, re, cv2, datetime
from tkinter import simpledialog, messagebox
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
        if student.startswith(name + "_") or student == name:
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
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if teacher:
        person_dir = os.path.join(DATASET_DIR, f"{name}_{teacher}_{timestamp}")
    else:
        person_dir = os.path.join(DATASET_DIR, f"{name}_{timestamp}")
    
    os.makedirs(person_dir, exist_ok=True)

    # Start photo capture
    if capture_photos(person_dir, num_photos, parent):
        messagebox.showinfo("Success", 
                          f"Successfully added {name} with {num_photos} photos", 
                          parent=parent)
    else:
        # Cleanup if failed
        try:
            os.rmdir(person_dir)
        except:
            pass

def capture_photos(person_dir, num_photos, parent=None):
    """Capture photos for a student"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera. Please check your camera connection.", parent=parent)
        return False

    photos_taken = 0
    
    # Create window
    cv2.namedWindow("Capture Photos", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capture Photos", 800, 600)

    while photos_taken < num_photos:
        ret, frame = cap.read()
        if not ret:
            continue

        # Create copy for display
        display_frame = frame.copy()
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Process detected faces
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(display_frame, (x,y), (x+w,y+h), (0,255,0), 2)

            # Save face image
            face = gray[y:y+h, x:x+w]
            try:
                face = cv2.resize(face, PHOTO_SIZE)
                filename = os.path.join(person_dir, f"photo_{photos_taken+1}.jpg")
                cv2.imwrite(filename, face)
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

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

    # Return success if we got at least one photo
    return photos_taken > 0

if __name__ == "__main__":
    # Test the module
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
    add_student()