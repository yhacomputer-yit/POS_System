import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class SafeListFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        title_label = tk.Label(self, text="Safe Transactions Report", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Date:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.date_entry = DateEntry(search_frame, font=("Arial", 12), width=12, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Button(search_frame, text="Search", bg="#FF9800", fg="white", width=10, command=self.search_transactions).grid(row=0, column=4, padx=10)
        tk.Button(search_frame, text="Clear", bg="#9E9E9E", fg="white", width=10, command=self.clear_search).grid(row=0, column=5, padx=10)

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.safe_tree = ttk.Treeview(tree_frame, columns=("ID", "Amount", "Type", "Date", "Staff"), show="headings", height=15)
        self.safe_tree.heading("ID", text="ID")
        self.safe_tree.heading("Amount", text="Amount")
        self.safe_tree.heading("Type", text="Type")
        self.safe_tree.heading("Date", text="Date")
        self.safe_tree.heading("Staff", text="Staff")
        self.safe_tree.column("ID", width=60)
        self.safe_tree.column("Amount", width=100)
        self.safe_tree.column("Type", width=80)
        self.safe_tree.column("Date", width=120)
        self.safe_tree.column("Staff", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.safe_tree.yview)
        self.safe_tree.configure(yscrollcommand=scrollbar.set)

        self.safe_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Refresh", width=15, command=self.load_safe_transactions).grid(row=0, column=0, padx=5)
        tk.Button(bottom_frame, text="Print Receipt", bg="#2196F3", fg="white", width=15,
                 command=self.print_receipt).grid(row=0, column=1, padx=5)
        tk.Button(bottom_frame, text="Back to Dashboard", bg="#607d8b", fg="white", width=15,
                 command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=2, padx=5)

    def load_safe_transactions(self):
        for item in self.safe_tree.get_children():
            self.safe_tree.delete(item)
        try:
            transactions = self.db.fetch_all("SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id")
            for trans in transactions:
                self.safe_tree.insert("", tk.END, values=trans)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_transactions(self):
        date_filter = self.date_entry.get_date().strftime('%Y-%m-%d') if self.date_entry.get() else ""

        query = "SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id WHERE DATE(st.date) = %s"
        params = []

        if date_filter:
            query += " WHERE DATE(st.date) = %s"
            params.append(date_filter)

        for item in self.safe_tree.get_children():
            self.safe_tree.delete(item)
        try:
            transactions = self.db.fetch_all(query, params)
            for trans in transactions:
                self.safe_tree.insert("", tk.END, values=trans)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear_search(self):
        self.date_entry.set_date(datetime.now())
        self.load_safe_transactions()



    def print_receipt(self):
        selected = self.safe_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a transaction to print receipt")
            return

        trans = self.safe_tree.item(selected[0])['values']
        trans_id, amount, trans_type, date, staff = trans

        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write("Safe Transaction Receipt\n")
                    f.write("=" * 30 + "\n")
                    f.write(f"Transaction ID: {trans_id}\n")
                    f.write(f"Date: {date}\n")
                    f.write(f"Staff: {staff}\n")
                    f.write(f"Type: {trans_type}\n")
                    f.write(f"Amount: ${amount:.2f}\n")
                messagebox.showinfo("Success", "Receipt printed to file")
            except Exception as e:
                messagebox.showerror("Error", str(e))


