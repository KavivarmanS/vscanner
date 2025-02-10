import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController

class UserView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = UserController()

        # Username Label and Entry
        tk.Label(parent, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(parent)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password Label and Entry
        tk.Label(parent, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(parent, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password Label and Entry
        tk.Label(parent, text="Role:").grid(row=2, column=0, padx=10, pady=5)
        self.role_entry = tk.Entry(parent, show="*")
        self.role_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(parent, text="Create User", command=self.create_user).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(parent, text="Show Users", command=self.show_users).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(parent, text="Update Password", command=self.update_user).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(parent, text="Delete User", command=self.delete_user).grid(row=6, column=0, columnspan=2, pady=5)

        # User List Display
        self.user_listbox = tk.Listbox(parent, width=40)
        self.user_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        if username and password and role:
            success = self.controller.create_user(username, password, role)
            if success:
                messagebox.showinfo("Success", "User created successfully!")
            else:
                messagebox.showerror("Error", "Failed to create user. Username may already exist.")
        else:
            messagebox.showwarning("Warning", "Username and password cannot be empty.")

    def show_users(self):
        self.user_listbox.delete(0, tk.END)
        users = self.controller.read_users()
        for user in users:
            self.user_listbox.insert(tk.END, user[0])

    def update_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        new_password = self.password_entry.get()
        role = self.role_entry.get()
        if selected_user and new_password:
            self.controller.update_user(selected_user, new_password, role)
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showwarning("Warning", "Select a user and enter a new password.")

    def delete_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if selected_user:
            self.controller.delete_user(selected_user)
            self.show_users()
            messagebox.showinfo("Success", "User deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Select a user to delete.")

def display(parent):
    UserView(parent)