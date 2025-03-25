import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController
from views.Theme import light_theme, dark_theme

class UserView:
    def __init__(self, parent, theme="light", bg_color="#ffffff"):
        self.parent = parent
        self.controller = UserController()
        self.theme = theme
        self.bg_color = bg_color
        self.light_theme = light_theme
        self.dark_theme = dark_theme

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        # Main Container (Split into Left & Right Frames)
        self.container = ttk.Frame(self.parent, padding=10, style="Custom.TFrame")
        self.container.pack(expand=True, fill=tk.BOTH)

        # Left Panel (Sidebar)
        self.sidebar = ttk.Frame(self.container, width=200, padding=10, style="Custom.TFrame")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(self.sidebar, text="User Management", font=("Arial", 16, "bold"), style="Custom.TLabel").pack(pady=20)

        # Sidebar Buttons
        self.create_nav_button("➕ Add User", self.create_user)

        # Search Entry with Clear Button
        self.search_frame = ttk.Frame(self.sidebar)
        self.search_frame.pack(pady=5, fill=tk.X)

        self.search_entry = ttk.Entry(self.search_frame, style="Custom.TEntry")
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.filter_users())

        self.clear_button = ttk.Button(self.search_frame, text="❌", command=self.clear_search)
        self.clear_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.search_entry.insert(0, "Search users...")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        # Right Panel (Main Content)
        self.main_frame = ttk.Frame(self.container, padding=20, style="Custom.TFrame")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # User Table
        columns = ("Username", "Role", "Actions")
        self.user_table = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10, style="Custom.Treeview")
        self.user_table.heading("Username", text="Username")
        self.user_table.heading("Role", text="Role")
        self.user_table.heading("Actions", text="Actions")

        self.user_table.column("Username", width=150)
        self.user_table.column("Role", width=100)
        self.user_table.column("Actions", width=300)

        self.user_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load Users
        self.load_users()

    def on_entry_click(self, event):
        if self.search_entry.get() == "Search users...":
            self.search_entry.delete(0, tk.END)

    def on_focus_out(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search users...")

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.on_focus_out()
        self.load_users()

    def apply_theme(self):
        theme = self.dark_theme if self.theme == "dark" else self.light_theme

        self.parent.configure(bg=self.bg_color)
        self.container.configure(style="Custom.TFrame")
        self.sidebar.configure(style="Custom.TFrame")
        self.main_frame.configure(style="Custom.TFrame")

        style = ttk.Style()
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color, foreground=theme.fg_color)
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Custom.Treeview", background=self.bg_color, foreground=theme.fg_color, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", background=theme.header_bg, foreground=theme.header_fg, font=("Arial", 12, "bold"))

        highlight_color = "#3da69c" if self.theme == "light" else "#444444"
        style.map("Custom.Treeview", background=[("selected", highlight_color)])

        self.search_entry.configure(style="Custom.TEntry")
        self.clear_button.configure(style=theme.button_style)

        for widget in self.sidebar.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Button):
                widget.configure(style=theme.button_style)
            elif isinstance(widget, ttk.Entry):
                widget.configure(style="Custom.TEntry")

        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style="Custom.Treeview")

    def update_theme(self, new_theme, new_bg_color):
        self.theme = new_theme
        self.bg_color = new_bg_color
        self.apply_theme()

    def create_nav_button(self, text, command):
        """Helper function to create navigation buttons in the sidebar."""
        theme = self.dark_theme if self.theme == "dark" else self.light_theme
        btn = ttk.Button(self.sidebar, text=text, command=command, style=theme.button_style)
        btn.pack(fill=tk.X, pady=5, padx=10)

    def load_users(self):
        """Load all users into the table when the window opens."""
        for row in self.user_table.get_children():
            self.user_table.delete(row)

        users = self.controller.read_users()
        for user in users:
            self.user_table.insert("", tk.END, values=(user[0], user[1], "✏️ Edit | 🔄 Reset | ❌ Delete"))

    def filter_users(self):
        """Filter users based on search input."""
        query = self.search_entry.get().strip().lower()
        for row in self.user_table.get_children():
            self.user_table.delete(row)

        users = self.controller.read_users()
        for user in users:
            if query in user[0].lower() or query in user[1].lower():
                self.user_table.insert("", tk.END, values=(user[0], user[1], "✏️ Edit | 🔄 Reset | ❌ Delete"))

    def create_popup(self, title, fields, callback, is_role_combobox=False):
        """Creates a generic popup for different actions."""
        popup = tk.Toplevel(self.parent)
        popup.title(title)
        popup.geometry("350x250")

        entries = {}
        for label in fields:
            ttk.Label(popup, text=label, style="Custom.TLabel").pack(pady=5)
            if is_role_combobox and label == "Role":
                entry = ttk.Combobox(popup, values=["admin", "user"], style="Custom.TEntry")
            else:
                entry = ttk.Entry(popup, width=30, show="*" if "Password" in label else "", style="Custom.TEntry")
            entry.pack(pady=5)
            entries[label] = entry

        theme = self.dark_theme if self.theme == "dark" else self.light_theme
        ttk.Button(popup, text="Save", command=lambda: callback(popup, entries), style=theme.button_style).pack(pady=10)
        self.apply_theme_to_popup(popup)

    def apply_theme_to_popup(self, popup):
        theme = self.light_theme if self.theme == "light" else self.dark_theme

        style = ttk.Style()
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)
        style.configure(theme.entry_style, fieldbackground=theme.entry_bg, foreground=theme.entry_fg)

        popup.configure(bg=theme.bg_color)
        for widget in popup.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Entry):
                widget.configure(style=theme.entry_style)
            elif isinstance(widget, ttk.Button):
                widget.configure(style=theme.button_style)

    def edit_role(self, username):
        """Popup window to edit the role of a user."""

        def save_role(popup, entries):
            new_role = entries["Role"].get()
            if new_role:
                self.controller.update_user_role(username, new_role)
                messagebox.showinfo("Success", "Role updated successfully!")
                popup.destroy()
                self.load_users()

        self.create_popup("Edit Role", ["Role"], save_role, is_role_combobox=True)

    def reset_password(self, username):
        """Popup window to reset the password."""
        def save_password(popup, entries):
            new_password = entries["New Password"].get()
            if new_password:
                self.controller.update_user_password(username, new_password)
                messagebox.showinfo("Success", "Password updated successfully!")
                popup.destroy()

        self.create_popup("Reset Password", ["New Password"], save_password)

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
            menu = tk.Menu(self.parent, tearoff=0)
            menu.add_command(label="✏️ Edit Role", command=lambda: self.edit_role(username))
            menu.add_command(label="🔄 Reset Password", command=lambda: self.reset_password(username))
            menu.add_command(label="❌ Delete", command=lambda: self.delete_user(username))
            menu.post(event.x_root, event.y_root)

    def create_user(self):
        """Popup to create a new user."""

        def save_user(popup, entries):
            username = entries["Username"].get()
            password = entries["Password"].get()
            role = entries["Role"].get()
            if username and password and role:
                self.controller.create_user(username, password, role)
                popup.destroy()
                self.load_users()

        self.create_popup("Create User", ["Username", "Password", "Role"], save_user, is_role_combobox=True)


# Main display function
def display(parent, theme="light", bg_color="#ffffff"):
    view = UserView(parent, theme, bg_color)
    view.user_table.bind("<ButtonRelease-1>", view.on_item_click)
    return view