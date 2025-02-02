import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
from models.session import Session

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login")
        self.on_login_success = on_login_success
        self.controller = UserController()
        self.session = Session()

        if self.session.get_user()[0]:
            self.root.destroy()
            self.on_login_success()
            return

        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.remember_var = tk.IntVar()
        tk.Checkbutton(root, text="Remember Me", variable=self.remember_var).grid(row=2, column=1)

        tk.Button(root, text="Login", command=self.login).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        remember_me = self.remember_var.get()

        if username and password:
            user_data = self.controller.authenticate_user(username, password)
            if user_data:
                user_id, role = user_data
                self.session.set_user(user_id, role, remember=bool(remember_me))
                self.root.destroy()
                self.on_login_success()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
