import tkinter as tk
from views.login_view import LoginWindow
from views.dashboard_view import DashBoard
from views.register_view import RegisterWindow
from models.session import Session
import ttkbootstrap as tb


class MainApp:
    def __init__(self, root):
        self.root = root
        self.session = Session()
        self.style = tb.Style()
        self.show_initial_screen()

    def show_initial_screen(self):
        """Decides whether to show Login or Dashboard based on session."""
        if self.session.get_user()[0]:  # If a user is already logged in
            self.show_dashboard()
        else:
            self.show_login()

    def show_login(self):
        """Switch to login without destroying root."""
        if not self.root.winfo_exists():  # Check if root exists before clearing
            return
        self.clear_window()
        LoginWindow(self.root, self.show_dashboard, self.show_register)

    def show_register(self):
        """Destroys current frame and shows registration screen."""
        self.clear_window()
        RegisterWindow(self.root, self.show_login, self.show_login)

    def show_dashboard(self):
        """Switch to the dashboard without destroying root."""
        self.clear_window()  # Clear old widgets, but don't destroy root
        DashBoard(self.root, self.show_login)

    def clear_window(self):
        if not self.root.winfo_exists():  # Prevents errors if root is destroyed
            return
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    app = MainApp(root)
    root.mainloop()
