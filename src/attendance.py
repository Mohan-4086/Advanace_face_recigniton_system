# Modified: repository cleanup and reliability fixes, September 2026.
import os
import datetime
import csv
import threading
import pandas as pd
from tkinter import messagebox, Toplevel, ttk, filedialog
import tkinter as tk
from config import ATTENDANCE_DIR

# Ensure attendance directory exists
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

def get_attendance_file(date=None):
    """Get attendance file path for specific date or today"""
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_DIR, f"attendance_{date}.csv")

_write_lock = threading.Lock()


def mark_attendance(name, teacher=None, student_id=None):
    """Write once per student and teacher per day, including across restarts."""
    file_path = get_attendance_file()
    teacher = teacher or "Unknown"
    student_id = student_id or name
    with _write_lock:
        exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
        fields = ["Name", "Time", "Teacher", "Status", "StudentID"]
        if exists:
            with open(file_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                fields = reader.fieldnames
                for row in reader:
                    identity = row.get("StudentID") or row["Name"]
                    wanted = student_id if "StudentID" in fields else name
                    if identity == wanted and row["Teacher"] == teacher:
                        return False
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
            if not exists:
                writer.writeheader()
            writer.writerow({"Name": name, "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                             "Teacher": teacher, "Status": "Present", "StudentID": student_id})
        return True

class AttendanceViewer:
    def __init__(self, parent, teacher=None):
        self.window = Toplevel(parent)
        self.window.title("View Attendance")
        self.window.geometry("1000x600")
        self.teacher = teacher
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

        self.setup_gui()

    def setup_gui(self):
        # Control Frame
        control_frame = ttk.Frame(self.window, padding="10")
        control_frame.pack(fill='x')

        # Date Selection
        ttk.Label(control_frame, text="Select Date:").pack(side='left', padx=5)
        
        # Get available dates
        dates = []
        for file in os.listdir(ATTENDANCE_DIR):
            if file.startswith("attendance_") and file.endswith(".csv"):
                date = file.replace("attendance_", "").replace(".csv", "")
                dates.append(date)
        dates.sort(reverse=True)  # Most recent first

        self.date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        date_combo = ttk.Combobox(control_frame, textvariable=self.date_var, values=dates, state="readonly")
        date_combo.pack(side='left', padx=5)
        date_combo.bind('<<ComboboxSelected>>', self.load_attendance)

        # Export Button
        ttk.Button(control_frame, text="Export to Excel", 
                  command=self.export_to_excel).pack(side='right', padx=5)

        # Table Frame
        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create Treeview
        columns = ("Name", "Time", "Teacher", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=150)

        # Add Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Pack everything
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Statistics Frame
        self.stats_frame = ttk.LabelFrame(self.window, text="Statistics", padding="10")
        self.stats_frame.pack(fill='x', padx=10, pady=5)

        # Load initial data
        self.load_attendance()

    def load_attendance(self, event=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        date = self.date_var.get()
        file_path = get_attendance_file(date)

        if not os.path.exists(file_path):
            messagebox.showinfo("Info", "No attendance records for selected date", 
                              parent=self.window)
            return

        try:
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
            
            # Filter by teacher if specified
            if self.teacher:
                df = df[df['Teacher'] == self.teacher]

            # Update statistics
            self.update_statistics(df)

            # Add to treeview
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=tuple(row[c] for c in ("Name", "Time", "Teacher", "Status")))

            # Alternate row colors
            for i, item in enumerate(self.tree.get_children()):
                if i % 2 == 0:
                    self.tree.item(item, tags=('evenrow',))
                else:
                    self.tree.item(item, tags=('oddrow',))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading attendance: {str(e)}", 
                               parent=self.window)

    def update_statistics(self, df):
        # Clear existing statistics
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Calculate statistics
        total_students = len(df)
        unique_students = df['StudentID' if 'StudentID' in df else 'Name'].nunique()
        teachers = df['Teacher'].unique()

        # Display statistics
        ttk.Label(self.stats_frame, 
                 text=f"Total Entries: {total_students}").pack(side='left', padx=10)
        ttk.Label(self.stats_frame, 
                 text=f"Unique Students: {unique_students}").pack(side='left', padx=10)
        ttk.Label(self.stats_frame, 
                 text=f"Teachers: {', '.join(teachers)}").pack(side='left', padx=10)

    def sort_treeview(self, col):
        """Sort treeview when column header is clicked"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort()
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)

    def export_to_excel(self):
        date = self.date_var.get()
        file_path = get_attendance_file(date)
        
        if not os.path.exists(file_path):
            messagebox.showinfo("Info", "No attendance records to export", 
                              parent=self.window)
            return

        try:
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
            if self.teacher:
                df = df[df['Teacher'] == self.teacher]

            # Ask for save location
            export_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"attendance_{date}_export.xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                parent=self.window
            )

            if export_path:
                df.to_excel(export_path, index=False)
                messagebox.showinfo("Success", 
                                  f"Attendance exported to {export_path}", 
                                  parent=self.window)

        except Exception as e:
            messagebox.showerror("Error", 
                               f"Error exporting attendance: {str(e)}", 
                               parent=self.window)

def view_attendance(parent=None, teacher=None):
    AttendanceViewer(parent, teacher)
