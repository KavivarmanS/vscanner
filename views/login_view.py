import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController
from models.session import Session


class LoginWindow:
    def __init__(self, root, on_login_success, on_register):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)  # Allow resizing
        self.on_login_success = on_login_success
        self.on_register = on_register
        self.controller = UserController()
        self.session = Session()

        if self.session.get_user()[0]:
            self.root.destroy()
            self.on_login_success()
            return

        # Center the window
        self.center_window(400, 300)

        # Styling
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TEntry", font=("Arial", 12))

        # UI Elements
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        for i in range(4):
            frame.grid_rowconfigure(i, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.remember_var = tk.IntVar()
        self.remember_check = ttk.Checkbutton(frame, text="Remember Me", variable=self.remember_var)
        self.remember_check.grid(row=2, column=1, pady=5, sticky="w")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=1, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.login_button = ttk.Button(button_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.register_button = ttk.Button(button_frame, text="Register", command=self.register)
        self.register_button.grid(row=0, column=1, padx=5, sticky="ew")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        remember_me = self.remember_var.get()

        if username and password:
            user_data = self.controller.authenticate_user(username, password)
            if user_data:
                user_id, role = user_data
                self.session.set_user(user_id, role, remember=bool(remember_me))
                self.on_login_success()  # SWITCH VIEW (don't destroy root)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def register(self):
        self.on_register()

    def center_window(self, width, height):
        """Centers the window on the screen dynamically."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


# Example usage:
# root = tk.Tk()
# app = LoginWindow(root, lambda: print("Logged In!"), lambda: print("Go to Register Page"))
# root.mainloop()
