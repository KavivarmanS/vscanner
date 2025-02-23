import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.scan_profile_controller import ProfileController
from controllers.network_device_controller import NetworkDeviceController
from controllers.vulnerability_controller import VulnerabilityController


class ScanProfileView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProfileController()
        self.device_controller = NetworkDeviceController(self)
        self.vulnerability_controller = VulnerabilityController(self)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.sidebar = ttk.Frame(self.frame, padding=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(self.sidebar, text="Scan Profile Management", font=("Arial", 16, "bold")).pack(pady=10)

        self.search_entry = ttk.Entry(self.sidebar)
        self.search_entry.pack(pady=5, fill=tk.X)
        ttk.Button(self.sidebar, text="Search", command=self.search_profile).pack(pady=5, fill=tk.X)

        ttk.Button(self.sidebar, text="Add Profile", command=self.open_add_profile_popup).pack(pady=5, fill=tk.X)

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
        self.detail_frame = ttk.LabelFrame(self.frame, text="Profile Details", padding=10)
        self.detail_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Devices Table
        ttk.Label(self.detail_frame, text="Devices", font=("Arial", 12, "bold")).pack()
        device_columns = ("DeviceID", "DeviceName", "Location", "Type", "IPaddress")
        self.device_tree = ttk.Treeview(self.detail_frame, columns=device_columns, show="headings", height=5)
        headers = ["Device ID", "Device Name", "Location", "Type", "IP Address"]
        for col, header in zip(device_columns, headers):
            self.device_tree.heading(col, text=header)
        self.device_tree.pack(expand=True, fill=tk.BOTH)

        ttk.Button(self.detail_frame, text="Add Device", command=self.open_add_device_popup).pack(pady=5)
        ttk.Button(self.detail_frame, text="Remove Selected Device", command=self.remove_device).pack(pady=5)

        # Vulnerabilities Table
        ttk.Label(self.detail_frame, text="Vulnerabilities", font=("Arial", 12, "bold")).pack()
        vulnerability_columns = ("VulnerabilityID", "CVE_ID", "Description", "SeverityLevel")
        self.vulnerability_tree = ttk.Treeview(self.detail_frame, columns=vulnerability_columns, show="headings",
                                               height=5)
        headers = ["Vulnerability ID", "CVE ID", "Description", "Severity Level"]
        for col, header in zip(vulnerability_columns, headers):
            self.vulnerability_tree.heading(col, text=header)
        self.vulnerability_tree.pack(expand=True, fill=tk.BOTH)

        ttk.Button(self.detail_frame, text="Add Vulnerability", command=self.open_add_vulnerability_popup).pack(pady=5)
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
            self.device_tree.insert("", "end", values=(device[0], device[1], device[2],device[3],device[4]))

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
                self.load_profile_details(profile_id)

    def remove_device(self):
        selected = self.device_tree.selection()
        if selected:
            device_id = self.device_tree.item(selected, "values")[0]
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.remove_devices(profile_id, device_id)
                self.load_profile_details(profile_id)

    def add_vulnerability(self):
        vulnerability_id = simpledialog.askstring("Add Vulnerability", "Enter Vulnerability ID:")
        if vulnerability_id:
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.add_vulnerabilities(profile_id, vulnerability_id)
                self.load_profile_details(profile_id)

    def remove_vulnerability(self):
        selected = self.vulnerability_tree.selection()
        if selected:
            vulnerability_id = self.vulnerability_tree.item(selected, "values")[0]
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.remove_vulnerabilities(profile_id, vulnerability_id)
                self.load_profile_details(profile_id)

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

    def open_add_device_popup(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Select Devices")
        popup.geometry("800x600")

        profile_id = self.tree.item(self.tree.selection(), "values")[0]

        # Style Configuration
        style = ttk.Style(popup)
        style.configure("TLabel", padding=5, font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 10, "bold"))
        style.configure("TButton", padding=8, font=("Arial", 10))
        style.configure("TEntry", padding=5)
        style.configure("TCheckbutton", padding=5)

        # Profile ID Display
        profile_frame = ttk.Frame(popup)
        profile_frame.pack(pady=10)
        ttk.Label(profile_frame, text="Profile ID:", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Label(profile_frame, text=profile_id, style="TLabel").pack(side=tk.LEFT)

        # Search Frame (Real-time search)
        search_frame = ttk.Frame(popup)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search:", style="TLabel").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, style="TEntry")
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        def search_devices(event=None):  # Added event parameter
            query = search_entry.get().strip().lower()
            load_devices(query)

        search_entry.bind("<KeyRelease>", search_devices)  # Bind to key release

        # Main Canvas with Scrollable Frame
        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Table Headers
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, pady=5)
        ttk.Label(header_frame, text="✔", width=3, anchor="center", style="Header.TLabel").grid(row=0, column=0)
        ttk.Label(header_frame, text="Device ID", width=10, anchor="center", style="Header.TLabel").grid(row=0,
                                                                                                         column=1)
        ttk.Label(header_frame, text="Device Name", width=20, anchor="center", style="Header.TLabel").grid(row=0,
                                                                                                           column=2)
        ttk.Label(header_frame, text="Location", width=15, anchor="center", style="Header.TLabel").grid(row=0, column=3)
        ttk.Label(header_frame, text="Type", width=10, anchor="center", style="Header.TLabel").grid(row=0, column=4)
        ttk.Label(header_frame, text="IP Address", width=15, anchor="center", style="Header.TLabel").grid(row=0,
                                                                                                          column=5)

        # Checkbox Dictionary
        device_checkboxes = {}

        def load_devices(search_query=""):
            for widget in scrollable_frame.winfo_children():
                if isinstance(widget, ttk.Frame) and widget is not header_frame:
                    widget.destroy()
            print("test")
            all_devices = self.device_controller.get_devices_for_profile_add(profile_id)

            if search_query:
                all_devices = [d for d in all_devices if search_query in str(d).lower()]

            for i, device in enumerate(all_devices):
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X)

                var = tk.BooleanVar()
                chk = ttk.Checkbutton(row_frame, variable=var, style="TCheckbutton")
                chk.grid(row=i, column=0, padx=5)

                ttk.Label(row_frame, text=device[0], width=10, style="TLabel").grid(row=i, column=1)
                ttk.Label(row_frame, text=device[1], width=20, style="TLabel").grid(row=i, column=2)
                ttk.Label(row_frame, text=device[2], width=15, style="TLabel").grid(row=i, column=3)
                ttk.Label(row_frame, text=device[3], width=10, style="TLabel").grid(row=i, column=4)
                ttk.Label(row_frame, text=device[4], width=15, style="TLabel").grid(row=i, column=5)

                device_checkboxes[device[0]] = var

        load_devices()

        # Add Selected Devices Button (Bottom Right)
        button_frame = ttk.Frame(popup)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        def add_selected_devices():
            selected_devices = [device_id for device_id, var in device_checkboxes.items() if var.get()]
            if selected_devices:
                try:
                    for device in selected_devices:
                        self.controller.add_devices(profile_id, device)
                    popup.destroy()
                    self.load_profile_details(profile_id)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
            else:
                messagebox.showwarning("Selection Error", "Please select at least one device.")

        ttk.Button(button_frame, text="Add Selected Devices", command=add_selected_devices, style="TButton").pack(
            side=tk.RIGHT)
    def open_add_vulnerability_popup(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Select Vulnerabilities")

        vulnerability_columns = ("VulnerabilityID", "CVE_ID")
        vulnerability_tree = ttk.Treeview(popup, columns=vulnerability_columns, show="headings", height=10)
        vulnerability_tree.heading("VulnerabilityID", text="Vulnerability ID")
        vulnerability_tree.heading("CVE_ID", text="CVE ID")

        vulnerabilities = self.vulnerability_controller.get_all_vulnerabilities()
        for vuln in vulnerabilities:
            vulnerability_tree.insert("", "end", values=vuln)

        vulnerability_tree.pack(expand=True, fill=tk.BOTH)

        def add_selected_vulnerabilities():
            selected_items = vulnerability_tree.selection()
            selected_vulns = [vulnerability_tree.item(item, "values")[0] for item in selected_items]
            profile_id = self.tree.item(self.tree.selection(), "values")[0]
            self.controller.add_vulnerabilities(profile_id, selected_vulns)
            popup.destroy()
            self.load_profile_details(profile_id)

        ttk.Button(popup, text="Add Selected Vulnerabilities", command=add_selected_vulnerabilities).pack(pady=5)


def display(parent):
    parent.pack_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    view = ScanProfileView(parent)
    view.frame.pack(fill=tk.BOTH, expand=True)
