import tkinter as tk
import threading
from tkinter import ttk, messagebox, simpledialog
from controllers.scan_profile_controller import ProfileController
from controllers.network_device_controller import NetworkDeviceController
from controllers.vulnerability_controller import VulnerabilityController
from controllers.scan_profile_vulnerabilities_controller import ScanProfileVulnerabilitiesController
from controllers.scan_controller import ScanController
from models.session import Session
from views.Theme import light_theme, dark_theme


def display(parent, theme, bg_color):
    parent.pack_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    view = ScanProfileView(parent, theme, bg_color)
    view.frame.pack(fill=tk.BOTH, expand=True)
    return view

class ScanProfileView:
    def __init__(self, parent, theme="light", bg_color="#ffffff"):
        self.parent = parent
        self.controller = ProfileController()
        self.device_controller = NetworkDeviceController(self)
        self.vulnerability_controller = VulnerabilityController(self)
        self.vulnerability_profile_controller = ScanProfileVulnerabilitiesController()
        self.scan_controller = ScanController()
        self.bg_color = bg_color
        self.theme = theme
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.widths = [3, 10, 20, 15, 10, 15]
        self.create_widgets()
        self.load_data()
        self.apply_theme()


        self.tree.bind("<Button-3>", self.show_context_menu)


    def show_context_menu(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            menu = tk.Menu(self.tree, tearoff=0)
            menu.add_command(label="🔍Trigger Scan", command=self.trigger_scan)
            menu.post(event.x_root, event.y_root)

    def trigger_scan(self):
        selected_item = self.tree.selection()
        if selected_item:
            profile_id = self.tree.item(selected_item, "values")[0]
            self.show_progress_bar(profile_id)

    def show_progress_bar(self, profile_id):
        self.progress_popup = tk.Toplevel(self.parent)
        self.progress_popup.title("Scanning Profile")
        self.progress_popup.geometry("400x200")

        ttk.Label(self.progress_popup, text="Scanning profile...").pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_popup, orient="horizontal", mode="determinate")
        self.progress_bar.pack(pady=10, fill=tk.X)

        self.cancel_button = ttk.Button(self.progress_popup, text="Cancel", command=self.cancel_scan)
        self.cancel_button.pack(pady=10)

        self.progress_popup.protocol("WM_DELETE_WINDOW", self.cancel_scan)
        self.apply_theme_to_popup(self.progress_popup)
        self.center_popup(self.progress_popup)

        # Start the scan in a separate thread
        self.scan_thread = threading.Thread(target=self.run_scan, args=(profile_id,), daemon=True)
        self.scan_thread.start()
        self.update_progress_bar()

    def apply_theme_to_popup(self, popup):
        theme = self.dark_theme if self.theme == "dark" else self.light_theme

        style = ttk.Style()
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)

        popup.configure(bg=theme.bg_color)
        for widget in popup.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(background=theme.bg_color, foreground=theme.fg_color)
            elif isinstance(widget, ttk.Entry):
                widget.configure(style="Custom.TEntry")
            elif isinstance(widget, ttk.Button):
                widget.configure(style=theme.button_style)

    def cancel_scan(self):
        if hasattr(self, 'scan_thread') and self.scan_thread.is_alive():
            messagebox.showinfo("Cancelled", "Scan operation cancelled.")
        self.progress_popup.destroy()
        self.progress_bar.stop()

    def run_scan(self, profile_id):
        result = self.scan_controller.scan_profile(profile_id)
        messagebox.showinfo("Scan Result", result)

    def apply_theme(self):
        theme = self.dark_theme if self.theme == "dark" else self.light_theme
        self.configure_styles(theme)
        self.apply_styles(theme)

    def update_progress_bar(self):
        if self.scan_thread.is_alive():
            self.progress_bar.step(1)
            self.progress_popup.after(100, self.update_progress_bar)
        else:
            self.progress_bar.stop()
            self.progress_popup.destroy()

    def configure_styles(self, theme):
        style = ttk.Style()
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color, foreground=theme.fg_color)
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg,
                        foreground=theme.btn_fg)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Custom.Treeview", background=self.bg_color, foreground=theme.fg_color,
                        fieldbackground=self.bg_color)
        style.configure("Custom.TText", background=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Treeview.Heading", background=theme.header_bg, foreground=theme.header_fg,
                        font=("Arial", 12, "bold"))

    def apply_styles(self, theme):
        self.frame.configure(style="Custom.TFrame")
        self.sidebar.configure(style="Custom.TFrame")
        self.main_frame.configure(style="Custom.TFrame")
        self.detail_frame.configure(style="Custom.TFrame")
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

        for widget in self.detail_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style="Custom.Treeview")
            elif isinstance(widget, ttk.Button):
                widget.configure(style=theme.button_style)

    def update_theme(self, new_theme, new_bg_color):
        self.theme = new_theme
        self.bg_color = new_bg_color
        self.apply_theme()

        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style="Custom.TFrame")
            elif isinstance(widget, ttk.Label):
                widget.configure(style="Custom.TLabel")
            elif isinstance(widget, ttk.Button):
                widget.configure(
                    style=self.light_theme.button_style if self.theme == "light" else self.dark_theme.button_style)
            elif isinstance(widget, ttk.Entry):
                widget.configure(style="Custom.TEntry")
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style="Custom.Treeview")

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.create_sidebar()
        self.create_main_frame()
        self.create_detail_frame()

    def create_sidebar(self):
        self.sidebar = ttk.Frame(self.frame, padding=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(self.sidebar, text="Scan Profile Management", font=("Arial", 16, "bold")).pack(pady=10)

        self.search_frame = ttk.Frame(self.sidebar)
        self.search_frame.pack(pady=5, fill=tk.X)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_profile())

        self.clear_button = ttk.Button(self.search_frame, text="❌", command=self.clear_search)
        self.clear_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.search_entry.insert(0, "Search profiles...")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        ttk.Button(self.sidebar, text="➕ Create new profile", command=self.create_profile).pack(pady=5, fill=tk.X)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.on_focus_out()
        self.load_data()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        columns = ("ProfileID", "UserID", "Actions")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)

        headers = ["Profile ID", "User ID", "Actions"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)
        self.tree.bind("<<TreeviewSelect>>", self.enable_buttons)

    def create_detail_frame(self):
        self.detail_frame = ttk.Frame(self.frame, padding=10, style="Custom.TFrame")
        self.detail_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.create_device_section()
        self.create_vulnerability_section()

    def create_device_section(self):
        ttk.Label(self.detail_frame, text="Devices", font=("Arial", 12, "bold")).pack()
        device_columns = ("DeviceID", "DeviceName", "Location", "Type", "IPaddress")
        self.device_tree = ttk.Treeview(self.detail_frame, columns=device_columns, show="headings", height=5)
        device_headers = ["Device ID", "Device Name", "Location", "Type", "IP Address"]
        for col, header in zip(device_columns, device_headers):
            self.device_tree.heading(col, text=header)
            self.device_tree.column(col, anchor="center", width=150)
        self.device_tree.pack(expand=True, fill=tk.BOTH)

        self.add_device_button = ttk.Button(self.detail_frame, text="➕ Add Device", command=self.open_add_device_popup,
                                            state=tk.DISABLED)
        self.add_device_button.pack(pady=5)

        # Bind right-click event
        self.device_tree.bind("<Button-3>", self.show_device_context_menu)

    def show_device_context_menu(self, event):
        selected_item = self.device_tree.identify_row(event.y)
        if selected_item:
            self.device_tree.selection_set(selected_item)
            menu = tk.Menu(self.device_tree, tearoff=0)
            menu.add_command(label="🗑️Remove", command=self.remove_device)
            menu.post(event.x_root, event.y_root)

    def create_vulnerability_section(self):
        ttk.Label(self.detail_frame, text="Vulnerabilities", font=("Arial", 12, "bold")).pack()
        vulnerability_columns = ("VulnerabilityID", "CVE_ID", "Description", "SeverityLevel")
        self.vulnerability_tree = ttk.Treeview(self.detail_frame, columns=vulnerability_columns, show="headings",
                                               height=5)
        vulnerability_headers = ["Vulnerability ID", "CVE ID", "Description", "Severity Level"]
        for col, header in zip(vulnerability_columns, vulnerability_headers):
            self.vulnerability_tree.heading(col, text=header)
            self.vulnerability_tree.column(col, anchor="center", width=150)
        self.vulnerability_tree.pack(expand=True, fill=tk.BOTH)

        self.add_vulnerability_button = ttk.Button(self.detail_frame, text="➕ Add Vulnerability",
                                                   command=self.open_add_vulnerability_popup, state=tk.DISABLED)
        self.add_vulnerability_button.pack(pady=5)

        # Bind right-click event
        self.vulnerability_tree.bind("<Button-3>", self.show_vulnerability_context_menu)

    def show_vulnerability_context_menu(self, event):
        selected_item = self.vulnerability_tree.identify_row(event.y)
        if selected_item:
            self.vulnerability_tree.selection_set(selected_item)
            menu = tk.Menu(self.vulnerability_tree, tearoff=0)
            menu.add_command(label="🗑️Remove", command=self.remove_vulnerability)
            menu.post(event.x_root, event.y_root)

    def enable_buttons(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.add_device_button.config(state=tk.NORMAL)
            self.add_vulnerability_button.config(state=tk.NORMAL)
        else:
            self.add_device_button.config(state=tk.DISABLED)
            self.add_vulnerability_button.config(state=tk.DISABLED)

    def on_entry_click(self, event):
        if self.search_entry.get() == "Search profiles...":
            self.search_entry.delete(0, tk.END)

    def on_focus_out(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search profiles...")

    def create_profile(self):
        session = Session()
        user_id = session.get_user()[0]
        self.controller.add_profile(user_id)
        messagebox.showinfo("Success", "Profile created successfully!")
        self.load_data()

    def search_profile(self):
        query = self.search_entry.get().strip().lower()
        self.clear_tree(self.tree)

        profiles = self.controller.get_profiles()
        for profile in profiles:
            if query in str(profile[0]) or query in str(profile[1]):
                self.tree.insert("", "end", values=(profile[0], profile[1], "🗑️"))

    def load_data(self):
        self.clear_tree(self.tree)

        profiles = self.controller.get_profiles()
        for profile in profiles:
            self.tree.insert("", "end", values=(profile[0], profile[1], "🗑️"))

    def clear_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if column == "#3":  # Check if the clicked column is the "Actions" column
            profile_id = self.tree.item(item, "values")[0]
            self.delete_profile(profile_id)
            self.load_data()

        item_values = self.tree.item(selected_item, "values")
        if item_values:
            self.load_profile_details(item_values[0])

    def delete_profile(self, profile_id):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Profile ID {profile_id}?")
        if confirm:
            self.controller.remove_profile(profile_id)
            self.load_data()
            messagebox.showinfo("Success", "Profile deleted successfully!")

    def load_profile_details(self, profile_id):
        self.clear_tree(self.device_tree)
        devices = self.controller.get_devices_by_profile(profile_id)
        for device in devices:
            self.device_tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4]))

        self.clear_tree(self.vulnerability_tree)
        vulnerabilities = self.controller.get_vulnerabilities_by_profile(profile_id)
        for vulnerability in vulnerabilities:
            self.vulnerability_tree.insert("", "end", values=(vulnerability[0],vulnerability[1],vulnerability[2],vulnerability[3]))

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



    def remove_vulnerability(self):
        selected = self.vulnerability_tree.selection()
        if selected:
            vulnerability_id = self.vulnerability_tree.item(selected, "values")[0]
            selected_item = self.tree.selection()
            if selected_item:
                profile_id = self.tree.item(selected_item, "values")[0]
                self.controller.remove_vulnerabilities(profile_id, vulnerability_id)
                self.load_profile_details(profile_id)

    def open_add_device_popup(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a profile first.")
            return

        profile_id = self.tree.item(selected_item, "values")[0]
        popup = tk.Toplevel(self.parent)
        popup.title("Select Devices")
        popup.geometry("800x600")

        self.create_popup_widgets(popup, profile_id)
        self.configure_popup_styles(popup)
        self.center_popup(popup)

    def configure_popup_styles(self, popup):
        theme = self.dark_theme if self.theme == "dark" else self.light_theme

        style = ttk.Style(popup)
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color, foreground=theme.fg_color)
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg,
                        foreground=theme.btn_fg)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Custom.Treeview", background=self.bg_color, foreground=theme.fg_color,
                        fieldbackground=self.bg_color)
        style.configure("Custom.TText", background=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Treeview.Heading", background=theme.header_bg, foreground=theme.header_fg,
                        font=("Arial", 12, "bold"))

        popup.configure(bg=self.bg_color)
        self.apply_styles_recursively(popup, theme)

    def apply_styles_recursively(self, widget, theme):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(style="Custom.TLabel")
            elif isinstance(child, ttk.Entry):
                child.configure(style="Custom.TEntry")
            elif isinstance(child, ttk.Button):
                child.configure(style=theme.button_style)
            elif isinstance(child, ttk.Frame):
                child.configure(style="Custom.TFrame")
            elif isinstance(child, ttk.Treeview):
                child.configure(style="Custom.Treeview")
            elif isinstance(child, tk.Text):
                child.configure(bg=theme.entry_bg, fg=theme.entry_fg)
            elif isinstance(child, ttk.Checkbutton):
                child.configure(style="Custom.TCheckbutton")
            elif isinstance(child, tk.Canvas):
                child.configure(bg=self.bg_color)
            self.apply_styles_recursively(child, theme)

    def create_popup_widgets(self, popup, profile_id):
        profile_frame = ttk.Frame(popup)
        profile_frame.pack(pady=10)
        ttk.Label(profile_frame, text="Profile ID:", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Label(profile_frame, text=profile_id, style="TLabel").pack(side=tk.LEFT)

        search_frame = ttk.Frame(popup)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search:", style="TLabel").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, style="TEntry")
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        search_entry.bind("<KeyRelease>", lambda event: self.search_devices(event, search_entry, profile_id))

        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)  # Define scrollable_frame as an instance attribute

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.header_frame = ttk.Frame(self.scrollable_frame)
        self.header_frame.pack(fill=tk.X, pady=5)
        headers = ["✔", "ID", "Name", "Location", "Type", "IP Address"]
        widths = [3, 5, 6, 15, 30, 15]
        for i, (header, width) in enumerate(zip(headers, widths)):
            ttk.Label(self.header_frame, text=header, width=width, anchor="center", style="Header.TLabel").grid(row=0,
                                                                                                                column=i)

        self.device_checkboxes = {}
        self.load_devices(self.scrollable_frame, profile_id)

        button_frame = ttk.Frame(popup)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        ttk.Button(button_frame, text="Add Selected Devices",
                   command=lambda: self.add_selected_devices(popup, profile_id)).pack(pady=5)


    def search_devices(self, event, search_entry, profile_id):
        query = search_entry.get().strip().lower()
        self.load_devices(self.scrollable_frame, profile_id, query)

    def load_devices(self, scrollable_frame, profile_id, search_query=""):
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget is not self.header_frame:
                widget.destroy()

        all_devices = self.device_controller.get_devices_for_profile_add(profile_id)

        if search_query:
            all_devices = [d for d in all_devices if search_query in str(d).lower()]
        widths = [3, 5, 6, 15, 30, 15]
        for i, device in enumerate(all_devices):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X)

            var = tk.BooleanVar()
            chk = ttk.Checkbutton(row_frame, variable=var, style="TCheckbutton")
            chk.grid(row=i, column=0, padx=5)

            for j, value in enumerate(device):
                ttk.Label(row_frame, text=value, width=widths[j+1], style="TLabel").grid(row=i, column=j+1)

            self.device_checkboxes[device[0]] = var

    def add_selected_devices(self, popup, profile_id):
        selected_devices = [device_id for device_id, var in self.device_checkboxes.items() if var.get()]
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

    def open_add_vulnerability_popup(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a profile first.")
            return

        profile_id = self.tree.item(selected_item, "values")[0]
        popup = tk.Toplevel(self.parent)
        popup.title("Select Vulnerabilities")
        popup.geometry("800x600")


        self.create_vulnerability_popup_widgets(popup, profile_id)
        self.configure_popup_styles(popup)
        self.center_popup(popup)

    def add_selected_vulnerabilities(self, popup, vulnerability_tree):
        selected_items = vulnerability_tree.selection()
        selected_vulns = [vulnerability_tree.item(item, "values")[0] for item in selected_items]
        profile_id = self.tree.item(self.tree.selection(), "values")[0]
        self.controller.add_vulnerabilities(profile_id, selected_vulns)
        popup.destroy()
        self.load_profile_details(profile_id)

    def center_popup(self, popup):
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")


    def create_vulnerability_popup_widgets(self, popup, profile_id):
        search_frame = ttk.Frame(popup)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search:", style="TLabel").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, style="TEntry")
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        search_entry.bind("<KeyRelease>", lambda event: self.search_vulnerabilities(event, search_entry, profile_id))

        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)  # Define scrollable_frame as an instance attribute

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.vulnerability_header_frame = ttk.Frame(self.scrollable_frame)
        self.vulnerability_header_frame.pack(fill=tk.X, pady=5)
        headers = ["✔", "Vulnerability ID", "CVE ID", "Severity", "Description"]
        widths = widths = [3, 10, 18, 8, 50]
        for i, (header, width) in enumerate(zip(headers, widths)):
            ttk.Label(self.vulnerability_header_frame, text=header, width=width, anchor="center", style="Header.TLabel").grid(row=0, column=i)

        self.vulnerability_checkboxes = {}
        self.load_vulnerabilities(self.scrollable_frame, profile_id)

        button_frame = ttk.Frame(popup)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        ttk.Button(button_frame, text="Add Selected Vulnerabilities",
                   command=lambda: self.add_selected_vulnerabilities(popup, profile_id)).pack(pady=5)

    def search_vulnerabilities(self, event, search_entry, profile_id):
        query = search_entry.get().strip().lower()
        self.load_vulnerabilities(self.scrollable_frame, profile_id, query)

    def load_vulnerabilities(self, scrollable_frame, profile_id, search_query=""):
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget is not self.vulnerability_header_frame:
                widget.destroy()

        all_vulnerabilities = self.vulnerability_controller.get_all_vulnerabilities_for_profile_add()

        if search_query:
            all_vulnerabilities = self.vulnerability_controller.search_vulnerabilities_for_profile_add(search_query)
        widths = [3, 10, 18, 8, 60]
        for i, vulnerability in enumerate(all_vulnerabilities):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X)

            var = tk.BooleanVar()
            chk = ttk.Checkbutton(row_frame, variable=var, style="TCheckbutton")
            chk.grid(row=i, column=0, padx=5)

            for j, value in enumerate(vulnerability):
                ttk.Label(row_frame, text=value, width=widths[j+1], style="TLabel").grid(row=i, column=j+1)

            self.vulnerability_checkboxes[vulnerability[0]] = var

    def add_selected_vulnerabilities(self, popup, profile_id):
        selected_vulnerabilities = [vulnerability_id for vulnerability_id, var in self.vulnerability_checkboxes.items() if var.get()]
        if selected_vulnerabilities:
            try:
                for vulnerability in selected_vulnerabilities:
                    self.vulnerability_profile_controller.add_scan_profile_vulnerability(profile_id, vulnerability)
                popup.destroy()
                self.load_profile_details(profile_id)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Selection Error", "Please select at least one vulnerability.")