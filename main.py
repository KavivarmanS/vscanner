import tkinter as tk
from views.login_view import LoginWindow
from views.dashboard_view import DashBoard
from models.session import Session

def start_main_app():
    root = tk.Tk()
    app = DashBoard(root)
    root.mainloop()

def start_login():
    login_root = tk.Tk()
    LoginWindow(login_root, start_main_app)
    login_root.mainloop()

if __name__ == "__main__":
    session = Session()
    if session.get_user()[0]:
        start_main_app()
    else:
        start_login()
