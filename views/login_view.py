import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb  # Modern theme for Tkinter
from controllers.user_controller import UserController
from models.session import Session

class LoginWindow:
    def __init__(self, root, on_login_success, on_register):
        self.root = root
        self.root.title("Login")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.on_login_success = on_login_success
        self.on_register = on_register
        self.controller = UserController()
        self.session = Session()

        if self.session.get_user()[0]:
            self.root.destroy()
            self.on_login_success()
            return

        # Center the window
        self.center_window(450, 400)

        # Styling
        self.root.configure(bg="#f8f9fa")

        # Main Frame
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = ttk.Label(main_frame, text="Welcome Back!", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Username Entry
        username_label = ttk.Label(main_frame, text="Username:", font=("Arial", 12))
        username_label.pack(anchor="w", padx=10)
        self.username_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(padx=10, pady=5)

        # Password Entry
        password_label = ttk.Label(main_frame, text="Password:", font=("Arial", 12))
        password_label.pack(anchor="w", padx=10)
        self.password_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(padx=10, pady=5)

        # Remember Me Checkbox
        self.remember_var = tk.IntVar()
        self.remember_check = ttk.Checkbutton(main_frame, text="Remember Me", variable=self.remember_var)
        self.remember_check.pack(anchor="w", padx=10, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.login_button = ttk.Button(button_frame, text="Login", style="success.TButton", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5, pady=5)

        self.register_button = ttk.Button(button_frame, text="Register", style="primary.TButton", command=self.register)
        self.register_button.grid(row=0, column=1, padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        remember_me = self.remember_var.get()

        if username and password:
            user_data = self.controller.authenticate_user(username, password)
            if user_data:
                user_id, role = user_data
                self.session.set_user(user_id, role, remember=bool(remember_me))
                self.on_login_success()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def register(self):
        self.on_register()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

