import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Safe List Window
def create_safe_list_frame(parent, db, show_dashboard):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="Safe Transactions Report", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Search frame
    search_frame = tk.Frame(frame)
    search_frame.pack(pady=10)
    
    tk.Label(search_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", pady=5, padx=10)
    date_entry = tk.Entry(search_frame, font=("Arial", 12), width=12)
    date_entry.grid(row=0, column=1, pady=5, padx=10)
    
    # Treeview
    tree_frame = tk.Frame(frame)
    tree_frame.pack(pady=10, fill="both", expand=True)
    
    cols = ("ID", "Amount", "Type", "Date", "Staff")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "ID" else 60)
    
    tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview).pack(side="right", fill="y")
    
    # Load
    def load():
        for item in tree.get_children():
            tree.delete(item)
        try:
            rows = db.fetch_all("SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id")
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Search
    def search():
        date = date_entry.get().strip()
        if not date:
            load()
            return
        
        for item in tree.get_children():
            tree.delete(item)
        try:
            rows = db.fetch_all("SELECT st.id, st.amount, st.type, st.date, COALESCE(s.name, 'Unknown') FROM safe_transactions st LEFT JOIN staff s ON st.staff_id = s.id WHERE DATE(st.date) = %s", (date,))
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Print receipt
    def print_receipt():
        if not tree.selection():
            messagebox.showwarning("Error", "Select a transaction")
            return
        
        values = tree.item(tree.selection()[0])["values"]
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            try:
                with open(path, "w") as f:
                    f.write("Safe Transaction Receipt\n" + "=" * 30 + "\n")
                    f.write(f"ID: {values[0]}\nDate: {values[3]}\nStaff: {values[4]}\nType: {values[2]}\nAmount: ${values[1]:.2f}\n")
                messagebox.showinfo("Success", "Saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    # Buttons (after functions are defined)
    tk.Button(search_frame, text="Search", bg="#FF9800", fg="white", width=10, command=search).grid(row=0, column=2, padx=10)
    tk.Button(search_frame, text="Clear", bg="#9E9E9E", fg="white", width=10, command=load).grid(row=0, column=3, padx=10)
    
    # Bottom buttons
    bottom = tk.Frame(frame)
    bottom.pack(pady=10)
    tk.Button(bottom, text="Refresh", width=15, command=load).grid(row=0, column=0, padx=5)
    tk.Button(bottom, text="Print", bg="#2196F3", fg="white", width=15, command=print_receipt).grid(row=0, column=1, padx=5)
    tk.Button(bottom, text="Back", bg="#607d8b", fg="white", width=15, command=show_dashboard).grid(row=0, column=2, padx=5)
    
    # Expose
    frame.load = load
    return frame
