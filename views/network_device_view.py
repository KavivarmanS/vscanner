import tkinter as tk
from tkinter import ttk, messagebox
from controllers.network_device_controller import NetworkDeviceController


class NetworkDeviceView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = NetworkDeviceController(self)
        self.progress_label = None

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 14, "bold"))
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(self.frame, text="Network Device Management", font=("Arial", 20, "bold")).grid(row=0, column=0,
                                                                                                 columnspan=3, pady=15)

        ttk.Label(self.frame, text="Search:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.search_entry = ttk.Entry(self.frame)
        self.search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(self.frame, text="Search", command=self.search_device).grid(row=1, column=2, padx=10, pady=5)

        ttk.Button(self.frame, text="Add Device", command=self.open_add_device_popup).grid(row=2, column=0, pady=10)
        ttk.Button(self.frame, text="Scan & Add Devices", command=self.on_scan_and_add_clicked).grid(row=2, column=2,
                                                                                                     pady=10)

        self.progress_bar = ttk.Progressbar(self.frame, mode="indeterminate", length=300)
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=5)
        self.progress_bar.grid_remove()

        self.progress_label = ttk.Label(self.frame, text="", font=("Arial", 12, "italic"), foreground="blue")
        self.progress_label.grid(row=3, column=0, columnspan=3, pady=5)

        columns = ("DeviceID", "DeviceName", "Location", "Type", "IPaddress", "Actions")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)

        headers = ["Device ID", "Device Name", "Location", "Device Type", "IP Address", "Actions"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=150)

        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.tree.bind("<Button-1>", self.on_action_click)

        self.load_data()

    def show_scan_progress(self, message):
        self.progress_label.config(text=message)
        self.parent.update_idletasks()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        devices = self.controller.get_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4], "Edit | Delete"))

    def search_device(self):
        query = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        devices = self.controller.get_devices()
        for device in devices:
            if query in device[1].lower() or query in device[2].lower() or query in device[4].lower():
                self.tree.insert("", "end",
                                 values=(device[0], device[1], device[2], device[3], device[4], "Edit | Delete"))

    def on_action_click(self, event):
        col = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        if not row_id or col != "#6":  # Ensure click is in the Actions column
            return

        item = self.tree.item(row_id, "values")
        if not item:
            return

        x, y, widget_width, widget_height = self.tree.bbox(row_id, "Actions")
        relative_x = event.x - x

        if relative_x < widget_width // 2:  # Clicked on "Edit"
            self.open_edit_device_popup(item)
        else:  # Clicked on "Delete"
            self.delete_device(item[0])

    def open_add_device_popup(self):
        popup = tk.Toplevel(self.parent)
        popup.title("Add Device")

        labels = ["Device Name", "Location", "Device Type", "IP Address"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(popup, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(popup)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def add_device():
            self.controller.add_device(entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get())
            messagebox.showinfo("Success", "Device added successfully!")
            popup.destroy()
            self.load_data()

        ttk.Button(popup, text="Save", command=add_device).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def open_edit_device_popup(self, item):
        popup = tk.Toplevel(self.parent)
        popup.title("Edit Device")

        labels = ["Device Name", "Location", "Device Type", "IP Address"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(popup, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(popup)
            entry.insert(0, item[i + 1])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def update_device():
            self.controller.modify_device(item[0], entries[0].get(), entries[1].get(), entries[2].get(),
                                          entries[3].get())
            messagebox.showinfo("Success", "Device updated successfully!")
            popup.destroy()
            self.load_data()

        ttk.Button(popup, text="Update", command=update_device).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def delete_device(self, device_id):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Device ID {device_id}?")
        if confirm:
            self.controller.remove_device(device_id)
            self.load_data()
            messagebox.showinfo("Success", "Device deleted successfully!")

    def on_scan_and_add_clicked(self):
        self.controller.scan_and_add_devices()


def display(parent):
    NetworkDeviceView(parent)
