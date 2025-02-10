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
    def __init__(self, root):
        self.root = root
        self.root.title("Scan Profile Manager")
        self.root.geometry("800x600")
        self.session = Session()


        # Left frame for buttons
        self.left_frame = tk.Frame(root, width=150, bg="lightgray")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right frame for displaying content
        self.right_frame = tk.Frame(root, width=450, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Buttons
        self.btn_logout = ttk.Button(self.left_frame, text="Logout", command=self.logout)
        self.btn_logout.pack(pady=10, padx=10, fill=tk.X)

        self.btn_vulnerability = ttk.Button(self.left_frame, text="Vulnerability", command=self.show_vulnerability_view)
        self.btn_vulnerability.pack(pady=10, padx=10, fill=tk.X)

        self.btn_device = ttk.Button(self.left_frame, text="Device", command=self.show_device_view)
        self.btn_device.pack(pady=10, padx=10, fill=tk.X)

        self.btn_device = ttk.Button(self.left_frame, text="Profile", command=self.show_scan_profile_view)
        self.btn_device.pack(pady=10, padx=10, fill=tk.X)

        self.btn_device = ttk.Button(self.left_frame, text="Result", command=self.show_scan_result_view)
        self.btn_device.pack(pady=10, padx=10, fill=tk.X)

        if self.session.get_role() == "admin":
            self.btn_device = ttk.Button(self.left_frame, text="Users", command=self.show_user_view)
            self.btn_device.pack(pady=10, padx=10, fill=tk.X)

    def logout(self):
        self.session.clear_session()
        self.root.destroy()
        import main
        main.start_login()

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