import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.scan_profile_controller import ProfileController


class ScanProfileView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProfileController()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.sidebar = ttk.Frame(self.frame, padding=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(self.sidebar, text="Scan Profile Management", font=("Arial", 16, "bold")).pack(pady=10)

        self.search_entry = ttk.Entry(self.sidebar)
        self.search_entry.pack(pady=5, fill=tk.X)
        ttk.Button(self.sidebar, text="Search", command=self.search_profile).pack(pady=5, fill=tk.X)

        ttk.Button(self.sidebar, text="Add Profile", command=self.open_add_profile_popup).pack(pady=5, fill=tk.X)
        self.refresh_button = ttk.Button(self.sidebar, text="Refresh", command=self.load_data)
        self.refresh_button.pack(pady=5, fill=tk.X)

        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        columns = ("ProfileID", "UserID", "ScanFrequency", "Actions")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)

        headers = ["Profile ID", "User ID", "Scan Frequency", "Actions"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        # Devices and Vulnerabilities Section
        self.detail_frame = ttk.Frame(self.frame)
        self.detail_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Devices Table
        ttk.Label(self.detail_frame, text="Devices", font=("Arial", 12, "bold")).pack()
        device_columns = ("DeviceID",)
        self.device_tree = ttk.Treeview(self.detail_frame, columns=device_columns, show="headings", height=5)
        self.device_tree.heading("DeviceID", text="Device ID")
        self.device_tree.pack(expand=True, fill=tk.BOTH)

        ttk.Button(self.detail_frame, text="Add Device", command=self.add_device).pack(pady=5)
        ttk.Button(self.detail_frame, text="Remove Selected Device", command=self.remove_device).pack(pady=5)

        # Vulnerabilities Table
        ttk.Label(self.detail_frame, text="Vulnerabilities", font=("Arial", 12, "bold")).pack()
        vulnerability_columns = ("VulnerabilityID",)
        self.vulnerability_tree = ttk.Treeview(self.detail_frame, columns=vulnerability_columns, show="headings",
                                               height=5)
        self.vulnerability_tree.heading("VulnerabilityID", text="Vulnerability ID")
        self.vulnerability_tree.pack(expand=True, fill=tk.BOTH)

        ttk.Button(self.detail_frame, text="Add Vulnerability", command=self.add_vulnerability).pack(pady=5)
        ttk.Button(self.detail_frame, text="Remove Selected Vulnerability", command=self.remove_vulnerability).pack(
            pady=5)

    def search_profile(self):
        query = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        profiles = self.controller.get_profiles()
        for profile in profiles:
            if query in str(profile[0]) or query in str(profile[1]):
                self.tree.insert("", "end", values=(profile[0], profile[1], profile[2], "Manage | Edit | Delete"))

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        profiles = self.controller.get_profiles()
        for profile in profiles:
            self.tree.insert("", "end", values=(profile[0], profile[1], profile[2], "Manage | Edit | Delete"))

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, "values")
        if item_values:
            self.load_profile_details(item_values[0])

    def load_profile_details(self, profile_id):
        # Load Devices
        for row in self.device_tree.get_children():
            self.device_tree.delete(row)
        devices = self.controller.get_devices_by_profile(profile_id)
        for device in devices:
            self.device_tree.insert("", "end", values=(device,))

        # Load Vulnerabilities
        for row in self.vulnerability_tree.get_children():
            self.vulnerability_tree.delete(row)
        vulnerabilities = self.controller.get_vulnerabilities_by_profile(profile_id)
        for vulnerability in vulnerabilities:
            self.vulnerability_tree.insert("", "end", values=(vulnerability,))

    def add_device(self):
        device_id = simpledialog.askstring("Add Device", "Enter Device ID:")
        if device_id:
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.add_devices(profile_id, device_id)
                self.device_tree.insert("", "end", values=(device_id,))

    def remove_device(self):
        selected = self.device_tree.selection()
        if selected:
            device_id = self.device_tree.item(selected, "values")[0]
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.remove_devices(profile_id, device_id)
                self.device_tree.delete(selected)

    def add_vulnerability(self):
        vulnerability_id = simpledialog.askstring("Add Vulnerability", "Enter Vulnerability ID:")
        if vulnerability_id:
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.add_vulnerabilities(profile_id, vulnerability_id)
                self.vulnerability_tree.insert("", "end", values=(vulnerability_id,))

    def remove_vulnerability(self):
        selected = self.vulnerability_tree.selection()
        if selected:
            vulnerability_id = self.vulnerability_tree.item(selected, "values")[0]
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.remove_vulnerabilities(profile_id, vulnerability_id)
                self.vulnerability_tree.delete(selected)

    def open_add_profile_popup(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Add Profile")

        labels = ["User ID", "Scan Frequency"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(popup, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(popup)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def add_profile():
            self.controller.add_profile(entries[0].get(), entries[1].get())
            messagebox.showinfo("Success", "Profile added successfully!")
            popup.destroy()
            self.load_data()

        ttk.Button(popup, text="Save", command=add_profile).grid(row=len(labels), column=0, columnspan=2, pady=10)


def display(parent):
    parent.pack_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    view = ScanProfileView(parent)
    view.frame.pack(fill=tk.BOTH, expand=True)
