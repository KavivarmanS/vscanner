import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController


class UserView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = UserController()

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 14, "bold"))

        # Main Frame
        self.frame = ttk.Frame(parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Title
        ttk.Label(self.frame, text="User Management", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=3,
                                                                                       pady=10)

        # Search Bar
        ttk.Label(self.frame, text="Search:").grid(row=1, column=0, sticky="w", padx=5)
        self.search_entry = ttk.Entry(self.frame, width=30)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.filter_users).grid(row=1, column=2, padx=5)

        # User Table
        columns = ("Username", "Role", "Actions")
        self.user_table = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)
        self.user_table.heading("Username", text="Username")
        self.user_table.heading("Role", text="Role")
        self.user_table.heading("Actions", text="Actions")

        self.user_table.column("Username", width=150)
        self.user_table.column("Role", width=100)
        self.user_table.column("Actions", width=300)

        self.user_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Add User Button
        ttk.Button(self.frame, text="Add New User", command=self.create_user).grid(row=3, column=0, pady=10)

        # Load Users
        self.load_users()

    def load_users(self):
        """Load all users into the table when the window opens."""
        for row in self.user_table.get_children():
            self.user_table.delete(row)

        users = self.controller.read_users()
        for user in users:
            self.user_table.insert("", tk.END, values=(user[0], user[1], "Edit Role | Reset Password | Delete"))

    def filter_users(self):
        """Filter users based on search input."""
        query = self.search_entry.get().strip().lower()
        for row in self.user_table.get_children():
            self.user_table.delete(row)

        users = self.controller.read_users()
        for user in users:
            if query in user[0].lower() or query in user[1].lower():
                self.user_table.insert("", tk.END, values=(user[0], user[1], "Edit Role | Reset Password | Delete"))

    def edit_role(self, username):
        """Popup window to edit the role of a user."""
        popup = tk.Toplevel(self.parent)
        popup.title("Edit Role")
        popup.geometry("300x200")

        ttk.Label(popup, text=f"Edit Role for {username}:").pack(pady=10)
        role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(popup, textvariable=role_var, values=["Admin", "User"], state="readonly")
        role_dropdown.pack(pady=10)
        role_dropdown.set("User")  # Default value

        def update_role():
            new_role = role_var.get()
            if new_role:
                self.controller.update_user_role(username, new_role)
                messagebox.showinfo("Success", "Role updated successfully!")
                popup.destroy()
                self.load_users()

        ttk.Button(popup, text="Update", command=update_role).pack(pady=10)

    def reset_password(self, username):
        """Popup window to reset the password."""
        popup = tk.Toplevel(self.parent)
        popup.title("Reset Password")
        popup.geometry("300x200")

        ttk.Label(popup, text=f"New Password for {username}:").pack(pady=10)
        new_password_entry = ttk.Entry(popup, width=30, show="*")
        new_password_entry.pack(pady=10)

        def update_password():
            new_password = new_password_entry.get()
            if new_password:
                self.controller.update_user_password(username, new_password)
                messagebox.showinfo("Success", "Password updated successfully!")
                popup.destroy()

        ttk.Button(popup, text="Update", command=update_password).pack(pady=10)

    def delete_user(self, username):
        """Delete the selected user."""
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {username}?")
        if confirm:
            self.controller.delete_user(username)
            self.load_users()
            messagebox.showinfo("Success", "User deleted successfully!")

    def on_item_click(self, event):
        """Handle user clicking on an action in the Actions column."""
        selected_item = self.user_table.selection()
        if not selected_item:
            return

        item = self.user_table.item(selected_item)
        username = item['values'][0]
        action = self.user_table.identify_column(event.x)

        if action == "#3":  # Actions column
            x, y, widget = event.x, event.y, self.user_table
            menu = tk.Menu(widget, tearoff=0)
            menu.add_command(label="Edit Role", command=lambda: self.edit_role(username))
            menu.add_command(label="Reset Password", command=lambda: self.reset_password(username))
            menu.add_command(label="Delete", command=lambda: self.delete_user(username))
            menu.post(widget.winfo_pointerx(), widget.winfo_pointery())

    def create_user(self):
        """Popup to create a new user."""
        popup = tk.Toplevel(self.parent)
        popup.title("Create User")
        popup.geometry("350x250")

        ttk.Label(popup, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(popup, width=30)
        username_entry.pack(pady=5)

        ttk.Label(popup, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(popup, width=30, show="*")
        password_entry.pack(pady=5)

        ttk.Label(popup, text="Role:").pack(pady=5)
        role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(popup, textvariable=role_var, values=["Admin", "User"], state="readonly", width=28)
        role_dropdown.pack(pady=5)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            if username and password and role:
                self.controller.create_user(username, password, role)
                popup.destroy()
                self.load_users()

        ttk.Button(popup, text="Save", command=save_user).pack(pady=10)


# Main display function
def display(parent):
    view = UserView(parent)
    view.user_table.bind("<ButtonRelease-1>", view.on_item_click)
