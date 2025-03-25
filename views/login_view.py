# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController
from models.session import Session
from views.Theme import Theme
import platform
import subprocess

class LoginWindow:
    def __init__(self, root, on_login_success, on_register):
        self.root = root
        self.root.title("Login")
        self.root.iconbitmap(r'D:\\AIP\\New folder\\vscanner\\icon.ico')
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


        # Determine system theme
        self.theme = self.get_system_theme()
        self.light_theme = Theme(
            name="light",
            bg_color="#e0f7fa",
            fg_color="#00796b",
            entry_bg="#ffffff",
            entry_fg="black",
            btn_bg="#4db6ac",
            btn_fg="#ffffff",
            button_style="Light.TButton",
            entry_style="Light.TEntry",
            header_bg="#b2ebf2",
            header_fg="#00796b",
            gradient_start="#e0f7fa",
            gradient_end="#4dd0e1"
        )

        self.dark_theme = Theme(
            name="dark",
            bg_color="#121212",
            fg_color="#ffffff",
            entry_bg="#333333",
            entry_fg="white",
            btn_bg="#333333",
            btn_fg="white",
            button_style="Dark.TButton",
            entry_style="Dark.TEntry",
            header_bg="#333333",
            header_fg="#ffffff",
            gradient_start="#121212",
            gradient_end="#444444"
        )

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        self.main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = ttk.Label(self.main_frame, text="Welcome Back!", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Username Entry
        username_label = ttk.Label(self.main_frame, text="Username:", font=("Arial", 12))
        username_label.pack(anchor="w", padx=10)
        self.username_entry = ttk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(padx=10, pady=5)

        # Password Entry
        password_label = ttk.Label(self.main_frame, text="Password:", font=("Arial", 12))
        password_label.pack(anchor="w", padx=10)
        self.password_entry = ttk.Entry(self.main_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(padx=10, pady=5)

        # Remember Me Checkbox
        self.remember_var = tk.IntVar()
        self.remember_check = ttk.Checkbutton(self.main_frame, text="Remember Me", variable=self.remember_var)
        self.remember_check.pack(anchor="w", padx=10, pady=5)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.login_button = ttk.Button(self.button_frame, text="Login", style="success.TButton", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5, pady=5)

        self.register_button = ttk.Button(self.button_frame, text="Register", style="primary.TButton", command=self.register)
        self.register_button.grid(row=0, column=1, padx=5, pady=5)

        # Apply theme after creating widgets
        self.apply_theme()

        # Center the window
        self.center_window(450, 400)



    def apply_theme(self):
        """Applies the current theme (light or dark)."""
        if self.theme == "Light":
            theme = self.light_theme
        else:
            theme = self.dark_theme

        self.root.configure(bg=theme.bg_color)
        print(theme.bg_color)

        style = ttk.Style()
        style.configure("Card.TFrame", background=theme.bg_color)
        style.configure("Custom.TLabel", background=theme.bg_color, foreground=theme.fg_color)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Custom.TCheckbutton", background=theme.bg_color, foreground=theme.fg_color)

        if self.theme == "Dark":
            style.configure("Login.TButton", font=("Arial", 12), padding=10, background=theme.bg_color, foreground="white")
            style.configure("Register.TButton", font=("Arial", 12), padding=10, background=theme.bg_color, foreground="white")
        else:
            style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)

        # Apply solid background color to the main frame and button frame
        self.main_frame.configure(style="Card.TFrame")
        self.button_frame.configure(style="Card.TFrame")

        # Apply theme to all widgets
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Entry):
                widget.configure(style="Custom.TEntry")
            elif isinstance(widget, ttk.Button):
                if self.theme == "Dark":
                    if widget == self.login_button:
                        widget.configure(style="Login.TButton")
                    elif widget == self.register_button:
                        widget.configure(style="Register.TButton")
                else:
                    widget.configure(style=theme.button_style)
            elif isinstance(widget, ttk.Checkbutton):
                widget.configure(style="Custom.TCheckbutton")

    def get_system_theme(self):
        system = platform.system()
        if system == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "Light" if value == 1 else "Dark"
            except Exception as e:
                return f"Error: {e}"

        elif system == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True,
                    text=True
                )
                return "Dark" if result.returncode == 0 else "Light"
            except Exception as e:
                return f"Error: {e}"

        else:
            return "Unsupported OS"

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