import tkinter as tk
from tkinter import messagebox
from controllers.scan_controller import ScanController  # Assuming ScanController is in a separate file


def run_scan():
    profile_id = entry_profile_id.get().strip()
    if not profile_id:
        messagebox.showerror("Error", "Profile ID cannot be empty!")
        return

    try:
        ScanController(profile_id)
        messagebox.showinfo("Success", "Scan completed! The PDF report has been generated.")
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
