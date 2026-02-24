import tkinter as tk
from tkinter import ttk, messagebox

# Category CRUD Window
def create_category_frame(parent, db, show_dashboard):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="Category Management", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Input
    tk.Label(frame, text="Category Name:").pack()
    name_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    name_entry.pack(pady=5)
    
    # Buttons
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    
    # Treeview
    tree_frame = tk.Frame(frame)
    tree_frame.pack(pady=10, fill="both", expand=True)
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.column("ID", width=80)
    tree.column("Name", width=200)
    tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview).pack(side="right", fill="y")
    
    # Load categories
    def load():
        for item in tree.get_children():
            tree.delete(item)
        try:
            for row in db.fetch_all("SELECT id, name FROM categories"):
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # On select
    def on_select(event):
        if tree.selection():
            values = tree.item(tree.selection()[0])['values']
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
    
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Create
    def create():
        name = name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Enter category name")
            return
        try:
            db.execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
            messagebox.showinfo("Success", "Created")
            name_entry.delete(0, tk.END)
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Update
    def update():
        if not tree.selection():
            messagebox.showwarning("Error", "Select category")
            return
        cat_id = tree.item(tree.selection()[0])['values'][0]
        name = name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Enter category name")
            return
        try:
            db.execute_query("UPDATE categories SET name = %s WHERE id = %s", (name, cat_id))
            messagebox.showinfo("Success", "Updated")
            name_entry.delete(0, tk.END)
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Delete
    def delete():
        if not tree.selection():
            messagebox.showwarning("Error", "Select category")
            return
        cat_id = tree.item(tree.selection()[0])['values'][0]
        try:
            db.execute_query("DELETE FROM categories WHERE id = %s", (cat_id,))
            messagebox.showinfo("Success", "Deleted")
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Button commands
    tk.Button(btn_frame, text="Create", bg="#4CAF50", fg="white", width=10, command=create).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Update", bg="#2196F3", fg="white", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", width=10, command=delete).grid(row=0, column=2, padx=5)
    
    # Bottom buttons
    bottom = tk.Frame(frame)
    bottom.pack(pady=10)
    tk.Button(bottom, text="Refresh", width=15, command=load).grid(row=0, column=0, padx=5)
    tk.Button(bottom, text="Back to Dashboard", bg="#607d8b", fg="white", width=15, command=show_dashboard).grid(row=0, column=1, padx=5)
    
    # Load on show
    frame.load = load
    return frame
