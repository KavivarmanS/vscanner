import tkinter as tk
from tkinter import ttk, messagebox
from controllers.scan_profile_controller import ProfileController
from models.session import Session


class ScanProfileWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Scan Profile Manager")
        self.root.geometry("600x400")
        self.controller = ProfileController()
        self.session = Session()
        self.user_id, self.role = self.session.get_user()

        # Labels & Entries
        tk.Label(root, text="User ID").grid(row=0, column=0, padx=10, pady=5)
        self.user_id_entry = tk.Entry(root)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.user_id_entry.insert(0, self.user_id)
        self.user_id_entry.config(state="readonly")

        tk.Label(root, text="Scan Frequency").grid(row=1, column=0, padx=10, pady=5)
        self.scan_frequency_entry = tk.Entry(root)
        self.scan_frequency_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Profile ID").grid(row=2, column=0, padx=10, pady=5)
        self.profile_id_entry = tk.Entry(root)
        self.profile_id_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add Profile", command=self.add_profile).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(root, text="Update Profile", command=self.update_profile).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(root, text="Delete Profile", command=self.delete_profile).grid(row=3, column=2, padx=10, pady=5)
        tk.Button(root, text="Refresh", command=self.load_data).grid(row=4, column=1, padx=10, pady=5)

        # Table
        self.tree = ttk.Treeview(root, columns=("ProfileID", "UserID", "ScanFrequency"), show="headings")
        self.tree.heading("ProfileID", text="Profile ID")
        self.tree.heading("UserID", text="User ID")
        self.tree.heading("ScanFrequency", text="Scan Frequency")
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        profiles = self.controller.get_profiles()
        for profile in profiles:
            self.tree.insert("", "end", values=profile)

    def add_profile(self):
        user_id = self.user_id_entry.get()
        scan_frequency = self.scan_frequency_entry.get()

        if user_id and scan_frequency:
            try:
                self.controller.add_profile(int(user_id), int(scan_frequency))
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add profile: {e}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def update_profile(self):
        profile_id = self.profile_id_entry.get()
        user_id = self.user_id_entry.get()
        scan_frequency = self.scan_frequency_entry.get()

        if profile_id and user_id and scan_frequency:
            try:
                self.controller.modify_profile(int(profile_id), int(user_id), int(scan_frequency))
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {e}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def delete_profile(self):
        profile_id = self.profile_id_entry.get()
        if profile_id:
            try:
                self.controller.remove_profile(int(profile_id))
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete profile: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a Profile ID to delete.")
