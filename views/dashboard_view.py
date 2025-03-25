# views/dashboard_view.py
import tkinter as tk
from tkinter import ttk
from models.session import Session
from views.Theme import Theme
import views.vulnerability_view
import views.user_view
import views.network_device_view
import views.scan_profile_view
import views.scan_result_view
import views.scan_profile_view
import views.scan_result_view
import platform
import subprocess
from views.Theme import light_theme, dark_theme


class DashBoard:
    def __init__(self, root, on_log_out):
        self.root = root
        self.root.title("VScanner")
        self.root.iconbitmap(r'D:\\AIP\\New folder\\vscanner\\icon.ico')
        self.on_log_out = on_log_out
        self.theme = self.get_system_theme()
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.root.geometry("1500x600")
        self.root.resizable(True, True)  # Allow resizing
        self.session = Session()
        self.vulnerability_view = None
        self.device_view = None
        self.user_view = None
        self.scan_profile_view = None
        self.scan_result_view = None

        # Set the window to full screen with title bar
        self.fullscreen = True
        self.root.state("zoomed")

        # Center the window
        self.center_window(1500, 600)

        # Bind F11 to toggle full screen
        self.root.bind("<F11>", self.toggle_fullscreen)

        # Styling
        self.theme = self.get_system_theme()
        if self.theme == "Dark":
            self.light_mode = False
        else:
            self.light_mode = True  # Initial mode is light

        # Left frame for buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Dashboard title
        title_label = tk.Label(
            self.left_frame, text="📊 Dashboard", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50"
        )
        title_label.pack(pady=20)

        # Buttons
        self.create_nav_button("🔓 Vulnerability", self.show_vulnerability_view)
        self.create_nav_button("💻 Device", self.show_device_view)
        self.create_nav_button("📂 Profile", self.show_scan_profile_view)
        self.create_nav_button("📊 Result", self.show_scan_result_view)


        if self.session.get_role() == "Admin" or self.session.get_role() == "admin":
            self.create_nav_button("👥 Users", self.show_user_view)

        # Theme toggle button
        self.theme_toggle_var = tk.BooleanVar(value=False)  # False for light, True for dark
        self.theme_toggle_button = ttk.Button(
            self.left_frame,
            text="🌙",  # Initial text
            command=self.toggle_theme,
        )
        self.theme_toggle_button.pack(pady=20, padx=20, side=tk.BOTTOM, fill=tk.X)

        # Logout button at bottom
        logout_btn = ttk.Button(
            self.left_frame, text="🚪 Logout", command=self.logout
        )
        logout_btn.pack(pady=20, padx=20, side=tk.BOTTOM, fill=tk.X)

        # Right frame for displaying content
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.apply_theme()  # Apply initial theme AFTER all widgets are created.

        # self.show_vulnerability_view()

    def toggle_fullscreen(self, event=None):
        """Toggles full screen mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.root.state("zoomed")
        else:
            self.root.state("normal")

    def apply_theme(self):
        """Applies the current theme (light or dark)."""
        if self.light_mode:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()

    def apply_light_theme(self):
        """Applies the light theme using the Theme class."""
        theme = self.light_theme

        self.root.configure(bg=theme.bg_color)
        self.left_frame.configure(bg=theme.bg_color)

        title_label = self.left_frame.winfo_children()[0]
        title_label.config(fg=theme.fg_color, bg=theme.bg_color, font=("Arial", 16, "bold"))

        # Define modern button style
        style = ttk.Style()
        style.configure(
            theme.button_style,
            font=("Arial", 12, "bold"),
            padding=12,
            relief="flat",
            background=theme.btn_bg,
            foreground=theme.btn_fg,
            borderwidth=0,
            bordercolor="",
            focusthickness=3,
            focustype="underline",
        )
        style.map(theme.button_style,
                  background=[("active", "#26a69a"), ("pressed", "#00796b")],
                  relief=[("pressed", "flat")])

        for widget in self.left_frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget != self.theme_toggle_button:
                widget.configure(style=theme.button_style)

        # Set a different solid background color for the right frame
        self.right_frame.configure(bg="#e8f9ff")

        self.theme_toggle_button.config(text="🌙", style=theme.button_style)
        self.theme = "light"

    def apply_dark_theme(self):
        """Applies the dark theme using the Theme class."""
        theme = self.dark_theme
        self.root.configure(bg=theme.bg_color)
        self.left_frame.configure(bg=theme.bg_color)

        title_label = self.left_frame.winfo_children()[0]
        title_label.config(fg=theme.fg_color, bg=theme.bg_color, font=("Arial", 16, "bold"))

        # Define modern button style for dark theme
        style = ttk.Style()
        style.configure(
            theme.button_style,
            font=("Arial", 12, "bold"),
            padding=12,
            relief="flat",
            background=theme.btn_bg,
            foreground=theme.btn_fg,
            borderwidth=0,
            bordercolor="",
            focusthickness=3,
            focustype="underline",
        )
        style.map(theme.button_style,
                  background=[("active", "#444444"), ("pressed", "#555555")],
                  relief=[("pressed", "flat")])

        for widget in self.left_frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget != self.theme_toggle_button:
                widget.configure(style=theme.button_style)

        # Set a different solid background color for the right frame
        self.right_frame.configure(bg="#222222")

        self.theme_toggle_button.config(text="☀️", style=theme.button_style)
        self.theme = "dark"

    def toggle_theme(self):
        """Toggles between light and dark mode and updates all views."""
        self.light_mode = not self.light_mode
        self.apply_theme()

        # Notify the currently active view about the theme change
        if self.vulnerability_view is not None:
            self.vulnerability_view.update_theme(self.theme, self.right_frame.cget("bg"))
        if self.device_view is not None:
            self.device_view.update_theme(self.theme, self.right_frame.cget("bg"))
        if self.user_view is not None:
            self.user_view.update_theme(self.theme, self.right_frame.cget("bg"))
        if self.scan_profile_view is not None:
            self.scan_profile_view.update_theme(self.theme, self.right_frame.cget("bg"))
        if self.scan_result_view is not None:
            self.scan_result_view.update_theme(self.theme, self.right_frame.cget("bg"))

    def create_nav_button(self, text, command):
        """Helper function to create navigation buttons."""
        btn = ttk.Button(self.left_frame, text=text, command=command)
        btn.pack(pady=10, padx=20, fill=tk.X)

    def logout(self):
        self.root.state("normal")
        self.session.clear_session()
        self.on_log_out()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def show_vulnerability_view(self):
        self.clear_right_frame()
        self.vulnerability_view = views.vulnerability_view.display(self.right_frame, self.theme, self.right_frame.cget("bg"))
        self.device_view = None
        self.user_view = None
        self.scan_profile_view = None
        self.scan_result_view = None

    def show_device_view(self):
        self.clear_right_frame()
        self.device_view = views.network_device_view.display(self.right_frame, self.theme, self.right_frame.cget("bg"))
        self.vulnerability_view = None
        self.user_view = None
        self.scan_profile_view = None
        self.scan_result_view = None

    def show_user_view(self):
        self.clear_right_frame()
        self.user_view = views.user_view.display(self.right_frame, self.theme, self.right_frame.cget("bg"))
        self.vulnerability_view = None
        self.device_view = None
        self.scan_profile_view = None
        self.scan_result_view = None

    def show_scan_profile_view(self):
        self.clear_right_frame()
        self.scan_profile_view = views.scan_profile_view.display(self.right_frame, self.theme, self.right_frame.cget("bg"))
        self.vulnerability_view = None
        self.device_view = None
        self.user_view = None
        self.scan_result_view = None

    def show_scan_result_view(self):
        self.clear_right_frame()
        self.scan_result_view = views.scan_result_view.display(self.right_frame, self.theme, self.right_frame.cget("bg"))
        self.vulnerability_view = None
        self.device_view = None
        self.user_view = None
        self.scan_profile_view = None

    def center_window(self, width, height):
        """Centers the window on the screen dynamically."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


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


