import tkinter as tk
from tkinter import ttk, messagebox
from controllers.network_device_controller import NetworkDeviceController


class NetworkDeviceView:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Device Manager")
        self.root.geometry("600x400")
        self.controller = NetworkDeviceController()

        # Labels & Entries
        tk.Label(root, text="Device ID").grid(row=0, column=0, padx=10, pady=5)
        self.device_id_entry = tk.Entry(root)
        self.device_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Device Name").grid(row=1, column=0, padx=10, pady=5)
        self.device_name_entry = tk.Entry(root)
        self.device_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Location").grid(row=2, column=0, padx=10, pady=5)
        self.location_entry = tk.Entry(root)
        self.location_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Device Type").grid(row=3, column=0, padx=10, pady=5)
        self.device_type_entry = tk.Entry(root)
        self.device_type_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="IP Address").grid(row=4, column=0, padx=10, pady=5)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.grid(row=4, column=1, padx=10, pady=5)



        # Buttons
        tk.Button(root, text="Add Device", command=self.add_device).grid(row=5, column=0, padx=10, pady=5)
        tk.Button(root, text="Update Device", command=self.update_device).grid(row=5, column=1, padx=10, pady=5)
        tk.Button(root, text="Delete Device", command=self.delete_device).grid(row=6, column=0, padx=10, pady=5)
        tk.Button(root, text="Refresh", command=self.load_data).grid(row=6, column=1, padx=10, pady=5)

        # Table
        self.tree = ttk.Treeview(root, columns=("ID", "Location", "Device Type", "IP Address"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Device Type", text="Device Type")
        self.tree.heading("IP Address", text="IP Address")
        self.tree.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        devices = self.controller.get_devices()
        for device in devices:
            self.tree.insert("", "end", values=device)

    def add_device(self):
        device_name = self.device_name_entry.get()
        location = self.location_entry.get()
        device_type = self.device_type_entry.get()
        ip_address = self.ip_entry.get()

        if location and device_type and ip_address:
            self.controller.add_device(device_name, location, device_type, ip_address)
            self.load_data()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def update_device(self):
        device_name = self.device_name_entry.get()
        device_id = self.device_id_entry.get()
        location = self.location_entry.get()
        device_type = self.device_type_entry.get()
        ip_address = self.ip_entry.get()

        if device_id and location and device_type and ip_address:
            self.controller.modify_device(device_name, device_id, location, device_type, ip_address)
            self.load_data()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def delete_device(self):
        device_id = self.device_id_entry.get()
        if device_id:
            self.controller.remove_device(device_id)
            self.load_data()
        else:
            messagebox.showwarning("Warning", "Please enter a Device ID to delete.")
