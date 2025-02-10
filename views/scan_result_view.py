import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controllers.scan_result_controller import ScanResultController


class ScanResultView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ScanResultController()

        # Profile ID Entry
        self.label = tk.Label(parent, text="Enter Profile ID:")
        self.label.pack(pady=5)

        self.profile_id_entry = tk.Entry(parent)
        self.profile_id_entry.pack(pady=5)

        # Scan Button
        self.scan_button = tk.Button(parent, text="Run Scan", command=self.run_scan)
        self.scan_button.pack(pady=5)

        # Result Display
        self.result_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=70, height=15)
        self.result_text.pack(pady=10)

    def run_scan(self):
        profile_id = self.profile_id_entry.get()
        if not profile_id:
            messagebox.showwarning("Input Error", "Please enter a Profile ID")
            return

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        result = self.controller.add_scan_result(profile_id)
        self.result_text.insert(tk.INSERT, result)

def display(parent):
    ScanResultView(parent)