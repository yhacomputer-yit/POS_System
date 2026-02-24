import tkinter as tk
from tkinter import ttk, messagebox


class ItemCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="Item Management", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Input fields
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        
        fields = [
            ("Item Name:", "name"),
            ("Price:", "price"),
            ("Barcode:", "barcode"),
            ("Category:", "category")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(input_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
            if key == "category":
                self.category_var = tk.StringVar()
                entry = ttk.Combobox(input_frame, textvariable=self.category_var, font=("Arial", 12), width=22)
            else:
                entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[key] = entry
        
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Create", bg="#4CAF50", fg="white", width=10, command=self.create).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", bg="#2196F3", fg="white", width=10, command=self.update).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", width=10, command=self.delete).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Back", bg="#607d8b", fg="white", width=10, command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=3, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)
        
        cols = ("ID", "Name", "Price", "Barcode", "Category")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "ID" else 60)
        
        self.tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview).pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        tk.Button(self, text="Refresh", width=15, command=self.load).pack(pady=10)
    
    def load_categories(self):
        try:
            cats = self.db.fetch_all("SELECT id, name FROM categories")
            self.entries["category"]["values"] = [f"{c[0]} - {c[1]}" for c in cats]
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def on_select(self, event):
        if self.tree.selection():
            values = self.tree.item(self.tree.selection()[0])['values']
            self.entries["name"].delete(0, tk.END)
            self.entries["name"].insert(0, values[1])
            self.entries["price"].delete(0, tk.END)
            self.entries["price"].insert(0, values[2])
            self.entries["barcode"].delete(0, tk.END)
            self.entries["barcode"].insert(0, values[3])
            self.category_var.set(values[4])
    
    def get_values(self):
        name = self.entries["name"].get()
        price = self.entries["price"].get()
        barcode = self.entries["barcode"].get()
        cat = self.category_var.get().split(" - ")[0] if self.category_var.get() else None
        return name, price, barcode, cat
    
    def create(self):
        name, price, barcode, cat = self.get_values()
        if not all([name, price, barcode, cat]):
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            self.db.execute_query("INSERT INTO items (name, price, barcode, category_id) VALUES (%s, %s, %s, %s)", (name, float(price), barcode, int(cat)))
            messagebox.showinfo("Success", "Created")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select item")
            return
        item_id = self.tree.item(self.tree.selection()[0])['values'][0]
        name, price, barcode, cat = self.get_values()
        if not all([name, price, barcode, cat]):
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            self.db.execute_query("UPDATE items SET name = %s, price = %s, barcode = %s, category_id = %s WHERE id = %s", (name, float(price), barcode, int(cat), item_id))
            messagebox.showinfo("Success", "Updated")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select item")
            return
        item_id = self.tree.item(self.tree.selection()[0])['values'][0]
        try:
            self.db.execute_query("DELETE FROM items WHERE id = %s", (item_id,))
            messagebox.showinfo("Success", "Deleted")
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear(self):
        self.entries["name"].delete(0, tk.END)
        self.entries["price"].delete(0, tk.END)
        self.entries["barcode"].delete(0, tk.END)
        self.category_var.set("")
    
    def load(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = self.db.fetch_all("SELECT i.id, i.name, i.price, i.barcode, c.name FROM items i JOIN categories c ON i.category_id = c.id")
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
