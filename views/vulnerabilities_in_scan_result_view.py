import tkinter as tk
from tkinter import messagebox
from controllers.vulnerabilities_in_scan_result_controller import VulnerabilitiesInScanResultController

class VulnerabilitiesView:
    def __init__(self, root):
        self.root = root
        self.controller = VulnerabilitiesInScanResultController()
        self.root.title("Manage Vulnerabilities in Scan Results")

        # Labels & Entry Fields
        tk.Label(root, text="Result ID:").grid(row=0, column=0, padx=10, pady=5)
        self.result_id_entry = tk.Entry(root)
        self.result_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Vulnerability ID:").grid(row=1, column=0, padx=10, pady=5)
        self.vulnerability_id_entry = tk.Entry(root)
        self.vulnerability_id_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add", command=self.add_vulnerability).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Delete", command=self.delete_vulnerability).grid(row=3, column=0, columnspan=2, pady=10)

        # Data Display
        self.result_list = tk.Listbox(root, width=50)
        self.result_list.grid(row=4, column=0, columnspan=2, pady=10)
        self.load_data()

    def add_vulnerability(self):
        result_id = self.result_id_entry.get()
        vulnerability_id = self.vulnerability_id_entry.get()

        if result_id and vulnerability_id:
            success = self.controller.add_vulnerability(result_id, vulnerability_id)
            if success:
                messagebox.showinfo("Success", "Vulnerability added successfully.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to add vulnerability.")
        else:
            messagebox.showwarning("Input Error", "Please enter both Result ID and Vulnerability ID.")

    def delete_vulnerability(self):
        selected = self.result_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a vulnerability to delete.")
            return

        selected_data = self.result_list.get(selected[0]).split(" | ")
        result_id, vulnerability_id = selected_data[0], selected_data[1]

        success = self.controller.delete_vulnerability(result_id, vulnerability_id)
        if success:
            messagebox.showinfo("Success", "Vulnerability deleted successfully.")
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to delete vulnerability.")

    def load_data(self):
        self.result_list.delete(0, tk.END)
        vulnerabilities = self.controller.get_all_vulnerabilities()
        for v in vulnerabilities:
            self.result_list.insert(tk.END, f"{v[0]} | {v[1]}")

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = VulnerabilitiesView(root)
    root.mainloop()
