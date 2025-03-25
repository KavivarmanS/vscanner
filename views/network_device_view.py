import tkinter as tk
from tkinter import ttk, messagebox
from controllers.network_device_controller import NetworkDeviceController
from views.Theme import light_theme, dark_theme
import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from controllers.device_scan_controller import DeviceScanController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.scan_profile_controller import ProfileController
from controllers.network_device_controller import NetworkDeviceController


def display(parent, theme, bg_color):
    parent.pack_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    view = NetworkDeviceView(parent, theme, bg_color)
    view.frame.pack(fill=tk.BOTH, expand=True)
    return view

class NetworkDeviceView:
    def __init__(self, parent, theme="light", bg_color="#ffffff"):
        self.parent = parent
        self.controller = NetworkDeviceController(self)
        self.device_scan_controller = DeviceScanController(self)
        self.theme = theme
        self.bg_color = bg_color
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.create_widgets()
        self.load_data()
        self.apply_theme()
        self.scan_thread = None
        self.scanning = False
        self.scan_popup = None

    def apply_theme(self):
        theme = self.dark_theme if self.theme == "dark" else self.light_theme

        self.parent.configure(bg=self.bg_color)
        self.frame.configure(style="Custom.TFrame")
        self.sidebar.configure(style="Custom.TFrame")
        self.main_frame.configure(style="Custom.TFrame")

        style = ttk.Style()
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color, foreground=theme.fg_color)
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)
        style.configure("Custom.TEntry", fieldbackground=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Custom.Treeview", background=self.bg_color, foreground=theme.fg_color, fieldbackground=self.bg_color)
        style.configure("Custom.TText", background=theme.entry_bg, foreground=theme.entry_fg)
        style.configure("Treeview.Heading", background=theme.header_bg, foreground=theme.header_fg, font=("Arial", 12, "bold"))

        highlight_color = "#3da69c" if self.theme == "light" else "#444444"
        style.map("Custom.Treeview", background=[("selected", highlight_color)])

        scrollbar_bg = theme.entry_bg
        scrollbar_troughcolor = theme.bg_color
        style.configure("Custom.Vertical.TScrollbar", background=scrollbar_bg, troughcolor=scrollbar_troughcolor)

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

        # Regenerate the chart to apply the new theme
        selected_item = self.tree.selection()
        if selected_item:
            device_id = self.tree.item(selected_item, "values")[0]
            self.generate_chart(device_id)
            self.display_scan_details(device_id)

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self.frame, padding=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ttk.Label(self.sidebar, text="Network Devices", font=("Arial", 16, "bold")).pack(pady=10)

        self.search_frame = ttk.Frame(self.sidebar)
        self.search_frame.pack(pady=5, fill=tk.X)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_device())

        self.clear_button = ttk.Button(self.search_frame, text="❌", command=self.clear_search)
        self.clear_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.search_entry.insert(0, "Search devices...")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        ttk.Button(self.sidebar, text="➕ Add Device", command=self.open_add_device_popup).pack(pady=5, fill=tk.X)
        ttk.Button(self.sidebar, text="📡 Scan & Add Devices", command=self.on_scan_and_add_clicked).pack(pady=5, fill=tk.X)

        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(1, weight=3)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        columns = ("DeviceID", "DeviceName", "Location", "Type", "IPaddress", "Actions")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)

        headers = ["Device ID", "Device Name", "Location", "Device Type", "IP Address", "Actions"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=150)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<ButtonRelease-1>", self.on_action_click)

        # Add chart frame
        self.chart_frame = ttk.Frame(self.main_frame)
        self.chart_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

    def on_entry_click(self, event):
        if self.search_entry.get() == "Search devices...":
            self.search_entry.delete(0, tk.END)

    def on_focus_out(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search devices...")

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.on_focus_out()
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        devices = self.controller.get_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4], "✏️ | 🗑️"))

    def search_device(self):
        query = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        devices = self.controller.get_devices()
        for device in devices:
            if any(query in str(value).lower() for value in device):
                self.tree.insert("", "end", values=(device[0], device[1], device[2], device[3], device[4], "✏️ | 🗑️"))

    def on_action_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, "values")
        if not item_values:
            return

        col_id = self.tree.identify_column(event.x)
        if col_id == "#6":
            x, y, width, height = self.tree.bbox(selected_item, "Actions")
            relative_x = event.x - x
            if relative_x < width // 2:
                self.open_edit_device_popup(item_values)
            else:
                self.delete_device(item_values[0])
        else:
            device_id = item_values[0]
            self.display_scan_details(device_id)

    def display_scan_details(self, device_id):
        # Clear previous content
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Generate and display the chart
        self.generate_chart(device_id)

        # Create a text area for scan details
        scan_details_text = self.device_scan_controller.get_scan_details_text(device_id)
        text_area = tk.Text(self.chart_frame, wrap=tk.WORD, height=10, width=50)
        text_area.insert(tk.END, scan_details_text)
        text_area.config(state=tk.DISABLED)

        # Apply theme to the text area
        theme = self.dark_theme if self.theme == "dark" else self.light_theme
        text_area.configure(bg=theme.entry_bg, fg=theme.entry_fg, font=("Arial", 12))

        text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        self.apply_theme_to_popup(popup)
        self.center_popup(popup)

    def delete_device(self, device_id):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Device ID {device_id}?")
        if confirm:
            self.controller.remove_device(device_id)
            self.load_data()
            messagebox.showinfo("Success", "Device deleted successfully!")

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
            self.controller.modify_device(item[0], entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get())
            messagebox.showinfo("Success", "Device updated successfully!")
            popup.destroy()
            self.load_data()

        ttk.Button(popup, text="Update", command=update_device).grid(row=len(labels), column=0, columnspan=2, pady=10)
        self.apply_theme_to_popup(popup)
        self.center_popup(popup)

    def apply_theme_to_popup(self, popup):
        theme = self.light_theme if self.theme == "light" else self.dark_theme

        style = ttk.Style()
        style.configure(theme.button_style, font=("Arial", 12), padding=10, background=theme.btn_bg, foreground=theme.btn_fg)
        style.configure(theme.entry_style, fieldbackground=theme.entry_bg, foreground=theme.entry_fg)

        popup.configure(bg=theme.bg_color)
        for widget in popup.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(background=theme.bg_color, foreground=theme.fg_color)
            elif isinstance(widget, ttk.Entry):
                widget.configure(style=theme.entry_style)
            elif isinstance(widget, ttk.Button):
                widget.configure(style=theme.button_style)

    def center_popup(self, popup):
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def on_scan_and_add_clicked(self):
        if self.scan_thread is None or not self.scan_thread.is_alive():
            self.scan_thread = threading.Thread(target=self.run_scan_and_add_devices)
            self.scan_thread.start()

    def run_scan_and_add_devices(self):
        self.controller.scan_and_add_devices()
        self.load_data()


    def cancel_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread = None
            self.scan_popup.destroy()
            messagebox.showinfo("Cancelled", "Scanning process has been cancelled.")



    def generate_chart(self, device_id):
        severity_counts = self.controller.get_scan_result_by_device_id(device_id)
        if severity_counts is None or any(count is None for count in severity_counts.values()):
            # Clear previous chart if exists
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            # Display scanning in progress message
            theme = self.dark_theme if self.theme == "dark" else self.light_theme
            self.chart_frame.configure(style="Custom.TFrame")
            label = ttk.Label(self.chart_frame, text="Scanning in progress...", font=("Arial", 14), background=theme.bg_color, foreground=theme.fg_color)
            label.pack(pady=20)
            return

        labels = []
        sizes = []
        for key, count in severity_counts.items():
            if count > 0:
                labels.append(f"{key} ({count})")
                sizes.append(int(count))

        if not sizes:
            labels = ['Safe']
            sizes = [100]
            colors = ['#66ff66']
            explode = (0,)  # no explode
        else:
            colors = ['#66b3ff', '#ffcc99', '#ff9999', '#ff6666']
            explode = [0.1] + [0] * (len(sizes) - 1)  # dynamically set explode length

        # Get theme background color and label color
        theme = self.dark_theme if self.theme == "dark" else self.light_theme
        bg_color = theme.bg_color
        label_color = theme.fg_color

        fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size
        fig.patch.set_facecolor(bg_color)  # Set figure background color
        ax.set_facecolor(bg_color)  # Set axes background color

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85, explode=explode)
        centre_circle = plt.Circle((0, 0), 0.70, fc=bg_color)  # Set center circle color to match theme
        fig.gca().add_artist(centre_circle)

        # Set label colors
        for text in texts + autotexts:
            text.set_color(label_color)

        # Clear previous chart if exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Close the figure to free up memory
        plt.close(fig)