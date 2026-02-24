import tkinter as tk
from tkinter import ttk, messagebox

# Item CRUD Window
def create_item_frame(parent, db, show_dashboard):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="Item Management", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Input fields
    input_frame = tk.Frame(frame)
    input_frame.pack(pady=10)
    
    # Name
    tk.Label(input_frame, text="Item Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    name_entry.grid(row=0, column=1, pady=5, padx=10)
    
    # Price
    tk.Label(input_frame, text="Price:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
    price_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    price_entry.grid(row=1, column=1, pady=5, padx=10)
    
    # Barcode
    tk.Label(input_frame, text="Barcode:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
    barcode_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    barcode_entry.grid(row=2, column=1, pady=5, padx=10)
    
    # Category
    tk.Label(input_frame, text="Category:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
    category_var = tk.StringVar()
    category_combo = ttk.Combobox(input_frame, textvariable=category_var, font=("Arial", 12), width=22)
    category_combo.grid(row=3, column=1, pady=5, padx=10)
    
    # Treeview
    tree_frame = tk.Frame(frame)
    tree_frame.pack(pady=10, fill="both", expand=True)
    
    cols = ("ID", "Name", "Price", "Barcode", "Category")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col != "ID" else 60)
    
    tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview).pack(side="right", fill="y")
    
    # Load categories
    def load_categories():
        try:
            cats = db.fetch_all("SELECT id, name FROM categories")
            category_combo["values"] = [f"{c[0]} - {c[1]}" for c in cats]
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # On select
    def on_select(event):
        if tree.selection():
            values = tree.item(tree.selection()[0])['values']
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            price_entry.delete(0, tk.END)
            price_entry.insert(0, values[2])
            barcode_entry.delete(0, tk.END)
            barcode_entry.insert(0, values[3])
            category_var.set(values[4])
    
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Get values
    def get_values():
        name = name_entry.get()
        price = price_entry.get()
        barcode = barcode_entry.get()
        cat = category_var.get().split(" - ")[0] if category_var.get() else None
        return name, price, barcode, cat
    
    # Clear
    def clear():
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        barcode_entry.delete(0, tk.END)
        category_var.set("")
    
    # Create
    def create():
        name, price, barcode, cat = get_values()
        if not all([name, price, barcode, cat]):
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            db.execute_query("INSERT INTO items (name, price, barcode, category_id) VALUES (%s, %s, %s, %s)", (name, float(price), barcode, int(cat)))
            messagebox.showinfo("Success", "Created")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Update
    def update():
        if not tree.selection():
            messagebox.showwarning("Error", "Select item")
            return
        item_id = tree.item(tree.selection()[0])['values'][0]
        name, price, barcode, cat = get_values()
        if not all([name, price, barcode, cat]):
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            db.execute_query("UPDATE items SET name = %s, price = %s, barcode = %s, category_id = %s WHERE id = %s", (name, float(price), barcode, int(cat), item_id))
            messagebox.showinfo("Success", "Updated")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Delete
    def delete():
        if not tree.selection():
            messagebox.showwarning("Error", "Select item")
            return
        item_id = tree.item(tree.selection()[0])['values'][0]
        try:
            db.execute_query("DELETE FROM items WHERE id = %s", (item_id,))
            messagebox.showinfo("Success", "Deleted")
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Load items
    def load():
        for item in tree.get_children():
            tree.delete(item)
        try:
            rows = db.fetch_all("SELECT i.id, i.name, i.price, i.barcode, c.name FROM items i JOIN categories c ON i.category_id = c.id")
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Buttons
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Create", bg="#4CAF50", fg="white", width=10, command=create).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Update", bg="#2196F3", fg="white", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", width=10, command=delete).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Back", bg="#607d8b", fg="white", width=10, command=show_dashboard).grid(row=0, column=3, padx=5)
    
    tk.Button(frame, text="Refresh", width=15, command=load).pack(pady=10)
    
    # Expose functions
    frame.load = load
    frame.load_categories = load_categories
    return frame
