import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import Database


class SafeListFrame(tk.Frame):
    def __init__(self, parent, controller=None, db=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        tk.Label(self, text="Safe Transactions Report", font=("Arial", 16, "bold")).pack(pady=20)

        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Date:", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, sticky="w", pady=5, padx=10)
        
        # DateEntry widget for date dropdown
        self.date_entry = DateEntry(search_frame, font=("Arial", 12), width=12, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Button(search_frame, text="Search", bg="#FF9800", fg="white", width=10,
                  command=self.search_transactions).grid(row=0, column=4, padx=10)
        tk.Button(search_frame, text="Clear", bg="#9E9E9E", fg="white", width=10,
                  command=self.clear_search).grid(row=0, column=5, padx=10)

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.safe_tree = ttk.Treeview(tree_frame, columns=("ID", "Amount", "Type", "Date", "Staff"),
                                      show="headings", height=15)
        for col in ("ID", "Amount", "Type", "Date", "Staff"):
            self.safe_tree.heading(col, text=col)
            self.safe_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.safe_tree.yview)
        self.safe_tree.configure(yscrollcommand=scrollbar.set)

        self.safe_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Refresh", width=15, command=self.load_safe_transactions)\
            .grid(row=0, column=0, padx=5)
        tk.Button(bottom_frame, text="Print Receipt", bg="#2196F3", fg="white", width=15)\
            .grid(row=0, column=1, padx=5)
        tk.Button(bottom_frame, text="Back to Dashboard", bg="#607d8b", fg="white", width=15,
                  command=lambda: messagebox.showinfo("Navigation", "Back to Dashboard clicked"))\
            .grid(row=0, column=2, padx=5)

        # Load initial data
        self.load_safe_transactions()

    def load_safe_transactions(self):
        # Clear current items
        for item in self.safe_tree.get_children():
            self.safe_tree.delete(item)

        if not self.db:
            return  # skip if no database provided

        try:
            transactions = self.db.fetch_all(
                "SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id;"
            )
            for trans in transactions:
                self.safe_tree.insert("", tk.END, values=trans)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_transactions(self):
        if not self.db:
            return
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
        
        # Clear treeview first
        for item in self.safe_tree.get_children():
            self.safe_tree.delete(item)

        try:
            transactions = self.db.fetch_all(
                "SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id WHERE DATE(st.date) = %s", (selected_date,)
            )
            for trans in transactions:
                self.safe_tree.insert("", tk.END, values=trans)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear_search(self):
        self.date_entry.set_date('')
        self.load_safe_transactions()


# For testing the UI independently
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Safe Transactions")
    root.geometry("700x500")

    db = Database()  # create your database object here
    frame = SafeListFrame(root, controller=None, db=db)
    frame.pack(fill="both", expand=True)

    root.mainloop()
