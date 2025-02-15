import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController


class RegisterWindow:
    def __init__(self, root, on_register_success, on_cancel):
        self.root = root
        self.root.title("Register")
        self.root.geometry("400x350")
        self.root.resizable(True, True)  # Allow resizing
        self.on_register_success = on_register_success
        self.on_cancel = on_cancel
        self.controller = UserController()

        # Center the window
        self.center_window(400, 350)

        # Styling
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))

        # UI Elements
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.confirm_password_entry = ttk.Entry(frame, width=25, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Role:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.role_combobox = ttk.Combobox(frame, values=["User", "Admin"], state="readonly", width=22)
        self.role_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.role_combobox.current(0)  # Default selection

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=1, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.register_button = ttk.Button(button_frame, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=0, column=1, padx=5, sticky="ew")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_combobox.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")
            return

        success = self.controller.create_user(username, password, role)
        if success:
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
            self.on_register_success()
        else:
            messagebox.showerror("Error", "Registration failed. User may already exist.")

    def cancel(self):
        self.on_cancel()

    def center_window(self, width, height):
        """Centers the window on the screen dynamically."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


# Example usage:
# root = tk.Tk()
# app = RegisterWindow(root, lambda: print("Registered!"), lambda: print("Cancel Registration"))
# root.mainloop()
