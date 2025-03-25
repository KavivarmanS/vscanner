import tkinter as tk
from tkinter import ttk, messagebox, Text
from controllers.scan_result_controller import ScanResultController
from views.Theme import light_theme, dark_theme
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display(parent, theme, bg_color):
    parent.pack_propagate(False)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    view = ScanResultView(parent, theme, bg_color)
    view.frame.pack(fill=tk.BOTH, expand=True)
    return view

class ScanResultView:
    def __init__(self, parent, theme="light", bg_color="#ffffff"):
        self.parent = parent
        self.controller = ScanResultController()
        self.theme = theme
        self.bg_color = bg_color
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.create_widgets()
        self.load_data()
        self.apply_theme()

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
        self.text_area.configure(bg=theme.entry_bg, fg=theme.entry_fg, insertbackground=theme.entry_fg)

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
        selected_item = self.tree.selection()
        if selected_item:
            profile_id, scan_timestamp = self.tree.item(selected_item[0], "values")
            self.show_bar_chart(profile_id, scan_timestamp)

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.sidebar = ttk.Frame(self.frame, padding=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ttk.Label(self.sidebar, text="Scan Results", font=("Arial", 16, "bold")).pack(pady=10)

        self.search_frame = ttk.Frame(self.sidebar)
        self.search_frame.pack(pady=5, fill=tk.X)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_scan_result())

        self.clear_button = ttk.Button(self.search_frame, text="❌", command=self.clear_search)
        self.clear_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.search_entry.insert(0, "Search scan results...")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(1, weight=3)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        columns = ("ProfileID", "ScanTimestamp")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)

        headers = ["Profile ID", "Scan Timestamp"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=150)

        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.chart_frame = ttk.Frame(self.main_frame)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")
        self.chart_frame.configure(style="Custom.TFrame")

        self.text_area = Text(self.main_frame, wrap=tk.WORD, state=tk.DISABLED)
        #self.text_area.grid(row=1, column=1, sticky="nsew")
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def on_entry_click(self, event):
        if self.search_entry.get() == "Search scan results...":
            self.search_entry.delete(0, tk.END)

    def on_focus_out(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search scan results...")

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.on_focus_out()
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        scan_results = self.controller.get_scan_results_for_table()
        for result in scan_results:
            self.tree.insert("", "end", values=(result[0], result[1]))

    def search_scan_result(self):
        query = self.search_entry.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        scan_results = self.controller.get_scan_results_for_table()
        for result in scan_results:
            if any(query in str(value).lower() for value in (result[0], result[1])):
                self.tree.insert("", "end", values=(result[0], result[1]))

    def on_row_select(self, event):
        selected_item = self.tree.selection()[0]
        profile_id, scan_timestamp = self.tree.item(selected_item, "values")
        self.show_bar_chart(profile_id, scan_timestamp)
        self.show_vulnerabilities_text(profile_id, scan_timestamp)

        # Pack the text_area when a row is selected
        self.text_area.grid(row=1, column=1, sticky="nsew")
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def show_bar_chart(self, profile_id, scan_timestamp):
        data = self.controller.get_data_for_chart(profile_id, scan_timestamp)

        devices = [f"Device {item[0]}: Port {item[1]}" for item in data]
        counts = [item[2] for item in data]

        theme = self.dark_theme if self.theme == "dark" else self.light_theme

        fig, ax = plt.subplots(figsize=(5, 6))  # Reduced width by 50%
        bars = ax.bar(devices, counts, color='#349adc')
        ax.set_xlabel('Device and Port', color=theme.fg_color)
        ax.set_ylabel('Number of Vulnerabilities', color=theme.fg_color)
        ax.set_title('Vulnerabilities per Device and Port', color=theme.fg_color)
        ax.set_xticklabels(devices, rotation=45, ha='right', color=theme.fg_color)
        ax.legend(facecolor=theme.bg_color, edgecolor=theme.fg_color)
        fig.patch.set_facecolor(theme.bg_color)
        ax.set_facecolor(theme.bg_color)

        ax.spines['bottom'].set_color(theme.fg_color)
        ax.spines['left'].set_color(theme.fg_color)
        ax.tick_params(axis='x', colors=theme.fg_color)
        ax.tick_params(axis='y', colors=theme.fg_color)

        plt.tight_layout()

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_vulnerabilities_text(self, profile_id, scan_timestamp):
        vulnerabilities_text = self.controller.get_vulnerabilities_detected(profile_id, scan_timestamp)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, vulnerabilities_text)
        self.text_area.config(state=tk.DISABLED)