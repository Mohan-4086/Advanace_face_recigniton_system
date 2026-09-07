# Modified: repository cleanup and reliability fixes, September 2026.
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
from datetime import datetime

from config import DATASET_DIR
from student_metadata import read_student

def refresh_table(tree, teacher=None):
    # Clear table
    for row in tree.get_children():
        tree.delete(row)

    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)

    students = []
    for student in os.listdir(DATASET_DIR):
        # Parse student directory name
        folder = os.path.join(DATASET_DIR, student)
        if not os.path.isdir(folder):
            continue
        info = read_student(folder)
        name, student_teacher, date_added = info["name"], info["teacher"], info["created"]

        # If teacher is specified, only show their students
        if teacher and student_teacher != teacher:
            continue
            
        students.append((name, student_teacher, date_added, student))

    # Sort by name
    students.sort(key=lambda x: x[0])

    for i, (name, student_teacher, date_added, full_name) in enumerate(students, start=1):
        tree.insert("", "end", values=(i, name, student_teacher, date_added), iid=full_name, tags=("evenrow" if i % 2 == 0 else "oddrow",))

def delete_student(tree, parent=None, teacher=None):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete.", parent=parent)
        return

    # Keep the directory identity separate from presentation tags
    full_name = selected[0]
    student_name = tree.item(selected[0], "values")[1]
    
    confirm = messagebox.askyesno("Confirm", 
                                 f"Are you sure you want to delete '{student_name}'?", 
                                 parent=parent)
    if confirm:
        folder = os.path.join(DATASET_DIR, full_name)
        try:
            shutil.rmtree(folder)
            messagebox.showinfo("Deleted", 
                              f"Student '{student_name}' removed successfully.", 
                              parent=parent)
            refresh_table(tree, teacher)
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Could not delete student: {e}", 
                               parent=parent)

def manage_students(parent=None, teacher=None):
    win = tk.Toplevel(parent)
    win.title("Manage Students")
    win.geometry("800x600")  # Increased size for more columns
    win.configure(bg="#f4f6f9")
    
    # Make window modal
    win.transient(parent)
    win.grab_set()
    win.focus_set()

    # Center window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

    # Title Frame
    title_frame = ttk.Frame(win)
    title_frame.pack(pady=10, fill="x")
    
    title = "All Students" if not teacher else f"Students Added by {teacher}"
    ttk.Label(title_frame, 
             text=title,
             font=("Helvetica", 16, "bold")).pack(side="left", padx=20)

    # Table Frame
    table_frame = ttk.Frame(win)
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Table
    columns = ("#", "Student Name", "Added By", "Date Added")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                       yscrollcommand=scrollbar.set)
    
    # Configure columns
    tree.heading("#", text="#")
    tree.heading("Student Name", text="Student Name")
    tree.heading("Added By", text="Added By")
    tree.heading("Date Added", text="Date Added")
    
    tree.column("#", width=50, anchor="center")
    tree.column("Student Name", width=200, anchor="w")
    tree.column("Added By", width=150, anchor="w")
    tree.column("Date Added", width=150, anchor="w")

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    # Buttons Frame
    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=20, padx=20)

    # Style for buttons
    style = ttk.Style()
    style.configure("Action.TButton", padding=10)

    ttk.Button(btn_frame, 
              text="🔄 Refresh", 
              style="Action.TButton",
              command=lambda: refresh_table(tree, teacher)).pack(side="left", padx=10)

    ttk.Button(btn_frame, 
              text="❌ Delete Selected", 
              style="Action.TButton",
              command=lambda: delete_student(tree, win, teacher)).pack(side="left", padx=10)

    # Load initial data
    refresh_table(tree, teacher)

    # Alternate row colors
    tree.tag_configure('oddrow', background='#f0f0f0')
    tree.tag_configure('evenrow', background='#ffffff')
    
    def alternate_row_colors():
        for idx, item in enumerate(tree.get_children()):
            if idx % 2 == 0:
                tree.item(item, tags=('evenrow',))
            else:
                tree.item(item, tags=('oddrow',))
    
    # Bind refresh to also update row colors
    def refresh_and_color():
        refresh_table(tree, teacher)
        alternate_row_colors()
    
    # Update initial row colors
    alternate_row_colors()



if __name__ == "__main__":
    manage_students()
