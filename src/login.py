# Modified: repository cleanup and reliability fixes, September 2026.
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from PIL import Image, ImageTk
from config import LOGIN_FILE, ASSETS_DIR, init
from auth import hash_password, verify_password

class LoginSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Smart Face Recognition System - Login")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        
        init()
        
        # Center window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        self.window.geometry(f"400x600+{x}+{y}")

        self.initialize_users()
        self.setup_gui()

    def initialize_users(self):
        if os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, encoding="utf-8") as file:
                users = json.load(file)
            # Upgrade local legacy plaintext credentials without changing passwords.
            changed = False
            for user in users.values():
                if not user["password"].startswith("pbkdf2_sha256$"):
                    user["password"] = hash_password(user["password"])
                    changed = True
            if changed:
                with open(LOGIN_FILE, "w", encoding="utf-8") as file:
                    json.dump(users, file, indent=4)
            return
        password = simpledialog.askstring(
            "First-time setup", "Choose a password for the admin account:",
            show="*", parent=self.window)
        if not password:
            self.window.destroy()
            raise SystemExit("Administrator setup cancelled")
        users = {"admin": {"password": hash_password(password),
                           "name": "Administrator", "role": "admin"}}
        with open(LOGIN_FILE, "x", encoding="utf-8") as file:
            json.dump(users, file, indent=4)

    def setup_gui(self):
        # Main Frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True)

        # Try to load logo
        try:
            logo_paths = [os.path.join(ASSETS_DIR, "logo.png")]
            
            logo_loaded = False
            for logo_path in logo_paths:
                if os.path.exists(logo_path):
                    logo = Image.open(logo_path)
                    logo = logo.resize((150, 150))
                    self.logo_photo = ImageTk.PhotoImage(logo)
                    logo_label = ttk.Label(main_frame, image=self.logo_photo)
                    logo_label.pack(pady=20)
                    logo_loaded = True
                    break
                    
            if not logo_loaded:
                ttk.Label(main_frame, 
                         text="Face Recognition\nAttendance System", 
                         font=("Helvetica", 16, "bold"),
                         justify="center").pack(pady=20)
                
        except Exception as e:
            print(f"Logo loading error: {e}")
            ttk.Label(main_frame, 
                     text="Face Recognition\nAttendance System", 
                     font=("Helvetica", 16, "bold"),
                     justify="center").pack(pady=20)

        # Login Frame
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=20, padx=40)

        # Username
        ttk.Label(login_frame, text="Username:", font=("Helvetica", 12)).pack(pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=30)
        username_entry.pack(pady=5)

        # Password
        ttk.Label(login_frame, text="Password:", font=("Helvetica", 12)).pack(pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.pack(pady=5)

        # Buttons Frame
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(pady=20)

        # Login Button
        login_btn = ttk.Button(button_frame, text="Login", command=self.login, width=20)
        login_btn.pack(pady=5)

        # Status message
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(login_frame, 
                                    textvariable=self.status_var,
                                    foreground='red',
                                    font=("Helvetica", 10))
        self.status_label.pack(pady=10)

        # Bind Enter key to login
        self.window.bind('<Return>', lambda e: self.login())

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            self.status_var.set("Please enter both username and password")
            return

        try:
            with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)

            if username in users and verify_password(password, users[username]["password"]):
                print(f"Successful login: {username}")
                self.status_var.set("Login successful!")
                self.status_label.configure(foreground='green')
                
                role = users[username]["role"]
                if role == "admin":
                    self.window.after(500, lambda: self.show_admin_panel(username))
                else:
                    self.window.after(500, lambda: self.start_main_app(username, users[username]["name"]))
            else:
                print(f"Failed login attempt: {username}")
                self.status_var.set("Invalid username or password")
                self.status_label.configure(foreground='red')

        except Exception as e:
            print(f"Login error: {e}")
            self.status_var.set("Login error occurred")
            self.status_label.configure(foreground='red')

    def show_admin_panel(self, admin_username):
        try:
            self.window.withdraw()
            AdminPanel(self.window, admin_username)
        except Exception as e:
            print(f"Error showing admin panel: {e}")
            self.window.deiconify()
            messagebox.showerror("Error", "Failed to open admin panel")

    def start_main_app(self, username, teacher_name):
        try:
            self.window.destroy()
            from main import MainApp
            app = MainApp(username, teacher_name)
            app.run()
        except Exception as e:
            print(f"Error starting main app: {e}")
            messagebox.showerror("Error", "Failed to start main application")

    def run(self):
        self.window.mainloop()

class AdminPanel:
    def __init__(self, parent, admin_username):
        self.parent = parent
        self.admin_username = admin_username
        
        self.window = tk.Toplevel()
        self.window.title("Admin Panel")
        self.window.geometry("600x400")
        
        # Center window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.window.geometry(f"600x400+{x}+{y}")
        
        self.setup_gui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(main_frame, 
                 text="Admin Control Panel",
                 font=("Helvetica", 18, "bold")).pack(pady=20)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        # Admin buttons
        buttons = [
            ("Add New Teacher", self.add_teacher),
            ("Manage Teachers", self.manage_teachers),
            ("Change Password", self.change_own_password),
            ("Start Attendance System", self.start_main_app),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            ttk.Button(btn_frame, 
                      text=text,
                      command=command,
                      width=25).pack(pady=10)

    def add_teacher(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Teacher")
        dialog.geometry("300x250")
        dialog.transient(self.window)
        dialog.grab_set()

        ttk.Label(dialog, text="Username:").pack(pady=5)
        username_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=username_var).pack(pady=5)

        ttk.Label(dialog, text="Display Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)

        ttk.Label(dialog, text="Password:").pack(pady=5)
        password_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=password_var, show="*").pack(pady=5)

        def save_teacher():
            username = username_var.get().strip()
            name = name_var.get().strip()
            password = password_var.get()

            if not all([username, name, password]):
                messagebox.showerror("Error", "All fields are required", parent=dialog)
                return

            try:
                with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                    users = json.load(f)

                if username in users:
                    messagebox.showerror("Error", "Username already exists", parent=dialog)
                    return

                users[username] = {
                    "password": hash_password(password),
                    "name": name,
                    "role": "teacher"
                }

                with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=4)

                messagebox.showinfo("Success", "Teacher added successfully", parent=dialog)
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add teacher: {str(e)}", parent=dialog)

        ttk.Button(dialog, text="Add Teacher", command=save_teacher).pack(pady=20)

    def manage_teachers(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Manage Teachers")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        dialog.grab_set()

        # Create Treeview
        columns = ("Username", "Name", "Role")
        tree = ttk.Treeview(dialog, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(pady=10, padx=10, fill='both', expand=True)

        def load_teachers():
            for item in tree.get_children():
                tree.delete(item)

            with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)

            for username, data in users.items():
                if data["role"] == "teacher":
                    tree.insert("", "end", values=(username, data["name"], data["role"]))

        def reset_password():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a teacher", parent=dialog)
                return

            username = tree.item(selected[0])['values'][0]
            
            reset_dialog = tk.Toplevel(dialog)
            reset_dialog.title("Reset Password")
            reset_dialog.geometry("300x150")
            reset_dialog.transient(dialog)
            reset_dialog.grab_set()

            ttk.Label(reset_dialog, text="New Password:").pack(pady=5)
            password_var = tk.StringVar()
            ttk.Entry(reset_dialog, textvariable=password_var, show="*").pack(pady=5)

            def save_password():
                new_password = password_var.get()
                if not new_password:
                    messagebox.showerror("Error", "Password cannot be empty", parent=reset_dialog)
                    return

                try:
                    with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                        users = json.load(f)

                    users[username]["password"] = hash_password(new_password)

                    with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
                        json.dump(users, f, indent=4)

                    messagebox.showinfo("Success", "Password reset successfully", parent=reset_dialog)
                    reset_dialog.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reset password: {str(e)}", parent=reset_dialog)

            ttk.Button(reset_dialog, text="Reset Password", command=save_password).pack(pady=20)

        def delete_teacher():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a teacher", parent=dialog)
                return

            username = tree.item(selected[0])['values'][0]
            
            if messagebox.askyesno("Confirm", f"Delete teacher {username}?", parent=dialog):
                try:
                    with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                        users = json.load(f)

                    del users[username]

                    with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
                        json.dump(users, f, indent=4)

                    load_teachers()
                    messagebox.showinfo("Success", "Teacher deleted successfully", parent=dialog)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete teacher: {str(e)}", parent=dialog)

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Reset Password", command=reset_password).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Teacher", command=delete_teacher).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=load_teachers).pack(side='left', padx=5)

        # Load initial data
        load_teachers()

    def change_own_password(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Password")
        dialog.geometry("300x250")
        dialog.transient(self.window)
        dialog.grab_set()

        ttk.Label(dialog, text="Current Password:").pack(pady=5)
        current_pass_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=current_pass_var, show="*").pack(pady=5)

        ttk.Label(dialog, text="New Password:").pack(pady=5)
        new_pass_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=new_pass_var, show="*").pack(pady=5)

        ttk.Label(dialog, text="Confirm New Password:").pack(pady=5)
        confirm_pass_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=confirm_pass_var, show="*").pack(pady=5)

        def save_password():
            current_pass = current_pass_var.get()
            new_pass = new_pass_var.get()
            confirm_pass = confirm_pass_var.get()

            if not all([current_pass, new_pass, confirm_pass]):
                messagebox.showerror("Error", "All fields are required", parent=dialog)
                return

            if new_pass != confirm_pass:
                messagebox.showerror("Error", "New passwords do not match", parent=dialog)
                return

            try:
                with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                    users = json.load(f)

                if not verify_password(current_pass, users[self.admin_username]["password"]):
                    messagebox.showerror("Error", "Current password is incorrect", parent=dialog)
                    return

                users[self.admin_username]["password"] = hash_password(new_pass)

                with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=4)

                messagebox.showinfo("Success", "Password changed successfully", parent=dialog)
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {str(e)}", parent=dialog)

        ttk.Button(dialog, text="Change Password", command=save_password).pack(pady=20)

    def start_main_app(self):
        try:
            with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            teacher_name = users[self.admin_username]["name"]
            
            self.window.destroy()
            self.parent.destroy()
            from main import MainApp
            app = MainApp(self.admin_username, teacher_name)
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start main application: {str(e)}")

    def logout(self):
        self.window.destroy()
        self.parent.deiconify()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to logout?"):
            self.logout()

if __name__ == "__main__":
    login = LoginSystem()
    login.run()
