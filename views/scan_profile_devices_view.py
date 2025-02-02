import tkinter as tk
from tkinter import ttk, messagebox
from controllers.scan_profile_devices_controller import ScanProfileDeviceController


class ScanProfileDeviceView:
    def __init__(self, root):
        self.root = root
        self.root.title("Scan Profile Devices")
        self.controller = ScanProfileDeviceController()

        tk.Label(root, text="Profile ID:").grid(row=0, column=0, padx=10, pady=5)
        self.profile_id_entry = tk.Entry(root)
        self.profile_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Device ID:").grid(row=1, column=0, padx=10, pady=5)
        self.device_id_entry = tk.Entry(root)
        self.device_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Add", command=self.add_scan_profile_device).grid(row=2, column=0, pady=10)
        tk.Button(root, text="Delete", command=self.delete_scan_profile_device).grid(row=2, column=1, pady=10)

        self.tree = ttk.Treeview(root, columns=("ProfileID", "DeviceID"), show="headings")
        self.tree.heading("ProfileID", text="Profile ID")
        self.tree.heading("DeviceID", text="Device ID")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        devices = self.controller.get_all_scan_profile_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device[0], device[1]))

    def add_scan_profile_device(self):
        profile_id = self.profile_id_entry.get()
        device_id = self.device_id_entry.get()

        if profile_id and device_id:
            success = self.controller.add_scan_profile_device(profile_id, device_id)
            if success:
                messagebox.showinfo("Success", "Device added to scan profile successfully.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to add device.")
        else:
            messagebox.showwarning("Input Error", "Please enter both Profile ID and Device ID.")

    def delete_scan_profile_device(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a device to delete.")
            return

        profile_id, device_id = self.tree.item(selected_item, "values")
        self.controller.delete_scan_profile_device(profile_id, device_id)
        messagebox.showinfo("Success", "Device removed from scan profile successfully.")
        self.load_data()
