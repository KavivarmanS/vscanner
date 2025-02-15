import tkinter as tk
from tkinter import ttk, messagebox
from controllers.network_device_controller import NetworkDeviceController
import threading

class NetworkDeviceView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = NetworkDeviceController(self)

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=6)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 14, "bold"))
        style.configure("TFrame", background="#f4f4f4")

        self.create_widgets()

    def create_widgets(self):
        """Create main UI components."""
        # Main Frame
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Title
        ttk.Label(self.frame, text="Network Device Management", font=("Arial", 18, "bold")).pack(pady=10)

        # Search Field
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Search", command=self.search_device).pack(side=tk.LEFT, padx=5)

        # Buttons Frame
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10, fill=tk.X)

        ttk.Button(btn_frame, text="Add Device", command=self.open_add_device_popup).pack(side=tk.LEFT, padx=5, expand=True)
        self.scan_button = ttk.Button(btn_frame, text="Scan & Add Devices", command=self.on_scan_and_add_clicked)
        self.scan_button.pack(side=tk.LEFT, padx=5, expand=True)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", mode="indeterminate", variable=self.progress_var, length=300)
        self.progress_bar.pack(pady=5, fill=tk.X)
        self.progress_bar.pack_forget()  # Initially hidden

        # Table
        columns = ("DeviceID", "DeviceName", "Location", "Type", "IPaddress", "Actions")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.replace("DeviceID", "ID"))
            self.tree.column(col, width=150 if col != "Actions" else 200)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tree.bind("<Button-3>", self.on_item_click)

        self.load_data()

    def on_item_click(self, event):
        """Handle right-click for actions."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item, "values")
        device_id = item[0]

        action_menu = tk.Menu(self.tree, tearoff=0)
        action_menu.add_command(label="Edit", command=lambda: self.open_edit_device_popup(item))
        action_menu.add_command(label="Delete", command=lambda: self.delete_device(device_id))
        action_menu.post(event.x_root, event.y_root)

    def load_data(self):
        """Load data into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        devices = self.controller.get_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4], "Right Click for Actions"))

    def search_device(self):
        """Filter devices based on search input."""
        query = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        devices = self.controller.get_devices()
        for device in devices:
            if query in device[1].lower() or query in device[2].lower() or query in device[4].lower():
                self.tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4], "Right Click for Actions"))

    def open_add_device_popup(self):
        """Popup for manually adding a device."""
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
        """Popup for editing a device."""
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
            self.controller.modify_device(item[0], entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get())
            messagebox.showinfo("Success", "Device updated successfully!")
            popup.destroy()
            self.load_data()

        ttk.Button(popup, text="Update", command=update_device).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def delete_device(self, device_id):
        """Delete a device after confirmation."""
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Device ID {device_id}?")
        if confirm:
            self.controller.remove_device(device_id)
            self.load_data()
            messagebox.showinfo("Success", "Device deleted successfully!")

    def on_scan_and_add_clicked(self):
        """Perform network scan with a progress indicator."""
        def run_scan():
            self.scan_button.config(state=tk.DISABLED)
            self.progress_bar.pack()
            self.progress_bar.start()
            messagebox.showinfo("Scanning", "Network scan in progress. Please wait...")

            self.controller.scan_and_add_devices("Toronto")

            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.scan_button.config(state=tk.NORMAL)
            messagebox.showinfo("Success", "Scan completed and devices added.")

            self.load_data()

        threading.Thread(target=run_scan, daemon=True).start()

def display(parent):
    NetworkDeviceView(parent)
