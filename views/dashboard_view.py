import tkinter as tk
from tkinter import ttk
import subprocess
from models.session import Session
import views.vulnerability_view
import views.user_view
import views.network_device_view
import views.scan_profile_view
import views.scan_result_view


class DashBoard:
    def __init__(self, root, on_log_out):
        self.root = root
        self.root.title("Scan Profile Manager")
        self.on_log_out = on_log_out
        self.root.geometry("1300x600")
        self.root.resizable(True, True)  # Allow resizing
        self.session = Session()

        # Center the window
        self.center_window(1300, 600)

        # Styling
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)

        # Left frame for buttons
        self.left_frame = tk.Frame(root, width=200, bg="#d3d3d3")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right frame for displaying content
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Buttons
        buttons = [
            ("Logout", self.logout),
            ("Vulnerability", self.show_vulnerability_view),
            ("Device", self.show_device_view),
            ("Profile", self.show_scan_profile_view),
            ("Result", self.show_scan_result_view)
        ]

        if self.session.get_role() == "Admin":
            buttons.append(("Users", self.show_user_view))

        for text, command in buttons:
            ttk.Button(self.left_frame, text=text, command=command, style="TButton").pack(pady=10, padx=20, fill=tk.X)

    def logout(self):
        self.session.clear_session()
        self.on_log_out()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def show_vulnerability_view(self):
        self.clear_right_frame()
        views.vulnerability_view.display(self.right_frame)

    def show_device_view(self):
        self.clear_right_frame()
        views.network_device_view.display(self.right_frame)

    def show_user_view(self):
        self.clear_right_frame()
        views.user_view.display(self.right_frame)

    def show_scan_profile_view(self):
        self.clear_right_frame()
        views.scan_profile_view.display(self.right_frame)

    def show_scan_result_view(self):
        self.clear_right_frame()
        views.scan_result_view.display(self.right_frame)

    def center_window(self, width, height):
        """Centers the window on the screen dynamically."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
