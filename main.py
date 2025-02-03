import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from controllers.scan_controller import ScanController  # Importing your ScanController class


def run_scan():
    profile_id = entry_profile_id.get().strip()

    if not profile_id:
        messagebox.showerror("Error", "Profile ID cannot be empty!")
        return

    try:
        controller = ScanController()
        pdf_file = "scan_results.pdf"
        controller.scan_for_cve(profile_id, pdf_file)

        messagebox.showinfo("Success", f"Scan completed! Report saved as {pdf_file}.")

        # Open the generated PDF automatically
        if os.path.exists(pdf_file):
            webbrowser.open(pdf_file)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create GUI window
root = tk.Tk()
root.title("Vulnerability Scanner")
root.geometry("300x150")

# Profile ID input field
tk.Label(root, text="Enter Profile ID:").pack(pady=5)
entry_profile_id = tk.Entry(root, width=30)
entry_profile_id.pack(pady=5)

# Scan button
btn_scan = tk.Button(root, text="Start Scan", command=run_scan)
btn_scan.pack(pady=10)

# Run GUI
root.mainloop()
