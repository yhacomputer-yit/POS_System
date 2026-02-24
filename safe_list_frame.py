import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class SafeListFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="Safe Transactions Report", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Date:").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.date_entry = tk.Entry(search_frame, font=("Arial", 12), width=12)
        self.date_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Button(search_frame, text="Search", bg="#FF9800", fg="white", width=10, command=self.search).grid(row=0, column=2, padx=10)
        tk.Button(search_frame, text="Clear", bg="#9E9E9E", fg="white", width=10, command=self.load).grid(row=0, column=3, padx=10)
        
        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)
        
        cols = ("ID", "Amount", "Type", "Date", "Staff")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "ID" else 60)
        
        self.tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview).pack(side="right", fill="y")
        
        # Bottom buttons
        bottom = tk.Frame(self)
        bottom.pack(pady=10)
        tk.Button(bottom, text="Refresh", width=15, command=self.load).grid(row=0, column=0, padx=5)
        tk.Button(bottom, text="Print", bg="#2196F3", fg="white", width=15, command=self.print_receipt).grid(row=0, column=1, padx=5)
        tk.Button(bottom, text="Back", bg="#607d8b", fg="white", width=15, command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=2, padx=5)
    
    def load(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = self.db.fetch_all("SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id")
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def search(self):
        date = self.date_entry.get().strip()
        if not date:
            self.load()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = self.db.fetch_all("SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id WHERE DATE(st.date) = %s", (date,))
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def print_receipt(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select a transaction")
            return
        
        values = self.tree.item(self.tree.selection()[0])["values"]
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            try:
                with open(path, "w") as f:
                    f.write("Safe Transaction Receipt\n" + "=" * 30 + "\n")
                    f.write(f"ID: {values[0]}\nDate: {values[3]}\nStaff: {values[4]}\nType: {values[2]}\nAmount: ${values[1]:.2f}\n")
                messagebox.showinfo("Success", "Saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
