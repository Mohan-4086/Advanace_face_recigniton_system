# window_utils.py
import tkinter as tk

def center_window(window, width, height):
    """Center a window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_popup_window(parent, title, width, height):
    """Create a properly configured popup window"""
    window = tk.Toplevel(parent)
    window.title(title)
    center_window(window, width, height)
    window.transient(parent)
    window.grab_set()
    window.focus_set()
    window.resizable(False, False)
    return window