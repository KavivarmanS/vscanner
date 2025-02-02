import tkinter as tk
from tkinter import ttk, messagebox
from controllers.scan_result_controller import ScanResultController


class ScanResultView:
    def __init__(self, root):
        self.root = root
        self.root.title("Scan Results")
        self.controller = ScanResultController()


        tk.Label(root, text="Critical Vulnerabilities:").grid(row=0, column=0, padx=10, pady=5)
        self.critical_vul_entry = tk.Entry(root)
        self.critical_vul_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Total Vulnerabilities:").grid(row=1, column=0, padx=10, pady=5)
        self.total_vul_entry = tk.Entry(root)
        self.total_vul_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Add", command=self.add_scan_result).grid(row=2, column=0, pady=10)
        tk.Button(root, text="Update", command=self.update_scan_result).grid(row=2, column=1, pady=10)
        tk.Button(root, text="Delete", command=self.delete_scan_result).grid(row=2, column=2, pady=10)

        self.tree = ttk.Treeview(root, columns=("ResultID", "ScanDate", "CriticalVul", "TotalVul"), show="headings")
        self.tree.heading("ResultID", text="ID")
        self.tree.heading("ScanDate", text="Scan Date")
        self.tree.heading("CriticalVul", text="Critical Vul")
        self.tree.heading("TotalVul", text="Total Vul")
        self.tree.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        results = self.controller.get_all_scan_results()
        for result in results:
            self.tree.insert("", "end", values=(result[0], result[1], result[2], result[3]))

    def add_scan_result(self):
        critical_vul = self.critical_vul_entry.get()
        total_vul = self.total_vul_entry.get()

        if critical_vul and total_vul:
            success = self.controller.add_scan_result(critical_vul, total_vul)
            if success:
                messagebox.showinfo("Success", "Scan result added successfully.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to add scan result.")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def update_scan_result(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a scan result to update.")
            return

        result_id = self.tree.item(selected_item, "values")[0]
        scan_date = self.scan_date_entry.get()
        critical_vul = self.critical_vul_entry.get()
        total_vul = self.total_vul_entry.get()

        if scan_date and critical_vul and total_vul:
            self.controller.update_scan_result(result_id, scan_date, critical_vul, total_vul)
            messagebox.showinfo("Success", "Scan result updated successfully.")
            self.load_data()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def delete_scan_result(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a scan result to delete.")
            return

        result_id = self.tree.item(selected_item, "values")[0]
        self.controller.delete_scan_result(result_id)
        messagebox.showinfo("Success", "Scan result deleted successfully.")
        self.load_data()
