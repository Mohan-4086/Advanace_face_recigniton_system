# Modified: repository cleanup and reliability fixes, September 2026.
# main.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import threading
import os
import time
import sys

# Your modules (make sure these import without errors)
from config import ASSETS_DIR
from student import add_student
from manage_students import manage_students
from attendance import view_attendance as show_attendance
from face_utils import start_recognition

class MainApp:
    def __init__(self, username, teacher_name):
        self.username = username
        self.teacher_name = teacher_name
        
        # -----------------------
        # Config
        # -----------------------
        self.ASSETS = ASSETS_DIR
        self.WIN_W, self.WIN_H = 900, 600

        # Create root
        self.root = tk.Tk()
        self.root.title(f"Smart Face Recognition System - {teacher_name}")
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.root.resizable(False, False)

        # Load images
        try:
            bg_img = self.load_image("background.jpg", size=(self.WIN_W, self.WIN_H))
            bg_img = ImageEnhance.Brightness(bg_img).enhance(0.72)
            self.bg_photo = ImageTk.PhotoImage(bg_img)

            banner_img = self.load_image("banner.png", size=(self.WIN_W, 100))
            self.banner_photo = ImageTk.PhotoImage(banner_img)

            logo_img = self.load_image("logo.png", size=(90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

        self.setup_gui()

    def load_image(self, filename, size=None):
        path = os.path.join(self.ASSETS, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required asset missing: {path}")
        img = Image.open(path).convert("RGBA")
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return img

    def setup_gui(self):
        # Background
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Banner
        banner_label = tk.Label(self.root, image=self.banner_photo, bd=0)
        banner_label.place(x=0, y=0)

        # Logo
        logo_label = tk.Label(self.root, image=self.logo_photo, bd=0)
        logo_label.place(x=18, y=8)

        # Teacher name
        teacher_label = tk.Label(self.root, 
                               text=f"Teacher: {self.teacher_name}", 
                               font=("Segoe UI", 11, "bold"), 
                               bg="#000000", 
                               fg="white")
        teacher_label.place(x=self.WIN_W - 300, y=35)

        # Time
        self.time_label = tk.Label(self.root, 
                                 font=("Segoe UI", 11, "bold"), 
                                 bg="#000000", 
                                 fg="white")
        self.time_label.place(x=self.WIN_W - 160, y=75)
        self.update_time()

        # Setup buttons
        self.setup_buttons()

    def update_time(self):
        self.time_label.config(text=time.strftime("%d-%m-%Y  %H:%M:%S"))
        self.root.after(1000, self.update_time)

    def setup_buttons(self):
        # Button specifications
        buttons = [
            ("➕  Add Student", lambda: add_student(self.root, self.username), {"use_main_thread": True}),
            ("🧑‍🎓  Manage Students", lambda: manage_students(self.root, self.username), {"use_main_thread": True}),
            ("📷  Start Recognition", lambda: start_recognition(self.root, self.username), {"use_main_thread": True}),
            ("📑  Show Attendance", lambda: show_attendance(self.root, self.username), {"use_main_thread": True}),
            ("❌  Logout", self.logout, {})
        ]

        # Button layout calculations
        button_width = 200
        button_height = 50
        h_padding = 60
        v_padding = 20

        total_width = (2 * button_width) + h_padding
        total_height = (3 * button_height) + (2 * v_padding)

        start_x = (self.WIN_W - total_width) // 2
        start_y = (self.WIN_H - total_height) // 2 + 50

        # Create and position buttons
        for idx, (text, func, opts) in enumerate(buttons):
            row = idx // 2
            col = idx % 2
            
            x = start_x + (col * (button_width + h_padding))
            y = start_y + (row * (button_height + v_padding))
            
            if idx == len(buttons) - 1:  # Center the last button (Logout)
                x = (self.WIN_W - button_width) // 2
                y = y + v_padding

            btn = self.make_button(text, func,
                                 use_main_thread=opts.get("use_main_thread", False),
                                 start_thread=opts.get("start_thread", False),
                                 thread_daemon=opts.get("thread_daemon", True))
            btn.place(x=x, y=y)

    def make_button(self, text, command, use_main_thread=False, start_thread=False, thread_daemon=True):
        def cmd_wrapper():
            if use_main_thread:
                self.run_on_main_thread(command)
            elif start_thread:
                self.start_in_thread(command, thread_daemon)
            else:
                try:
                    command()
                except Exception:
                    import traceback; traceback.print_exc()

        BTN_FONT = ("Segoe UI", 13, "bold")
        BTN_BG = "#0078D7"
        BTN_ACTIVE = "#005a9e"
        BTN_FG = "white"
        BTN_W = 22
        BTN_H = 2

        btn = tk.Button(self.root, text=text, font=BTN_FONT,
                       fg=BTN_FG, bg=BTN_BG, activebackground=BTN_ACTIVE,
                       activeforeground=BTN_FG, width=BTN_W, height=BTN_H,
                       bd=0, relief="flat", command=cmd_wrapper)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_ACTIVE))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG))
        return btn

    def run_on_main_thread(self, func):
        self.root.after(0, func)

    def start_in_thread(self, func, daemon=True):
        t = threading.Thread(target=lambda: self._thread_wrapper(func), daemon=daemon)
        t.start()
        return t

    def _thread_wrapper(self, func):
        try:
            func()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def logout(self):
        self.root.destroy()
        from login import LoginSystem
        login = LoginSystem()
        login.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    from login import LoginSystem
    login = LoginSystem()
    login.run()
