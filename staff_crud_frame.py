import tkinter as tk
from tkinter import ttk, messagebox

# Staff CRUD Window
def create_staff_frame(parent, db, show_dashboard):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="Staff Management", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Input
    input_frame = tk.Frame(frame)
    input_frame.pack(pady=10)
    
    tk.Label(input_frame, text="Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    name_entry.grid(row=0, column=1, pady=5, padx=10)
    
    tk.Label(input_frame, text="Role:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
    role_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    role_entry.grid(row=1, column=1, pady=5, padx=10)
    
    # Treeview
    tree_frame = tk.Frame(frame)
    tree_frame.pack(pady=10, fill="both", expand=True)
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Role"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Role", text="Role")
    tree.column("ID", width=80)
    tree.column("Name", width=200)
    tree.column("Role", width=150)
    
    tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview).pack(side="right", fill="y")
    
    # On select
    def on_select(event):
        if tree.selection():
            values = tree.item(tree.selection()[0])['values']
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            role_entry.delete(0, tk.END)
            role_entry.insert(0, values[2])
    
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Clear
    def clear():
        name_entry.delete(0, tk.END)
        role_entry.delete(0, tk.END)
    
    # Create
    def create():
        name = name_entry.get()
        role = role_entry.get()
        if not name or not role:
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            db.execute_query("INSERT INTO staff (name, role) VALUES (%s, %s)", (name, role))
            messagebox.showinfo("Success", "Created")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Update
    def update():
        if not tree.selection():
            messagebox.showwarning("Error", "Select staff")
            return
        staff_id = tree.item(tree.selection()[0])['values'][0]
        name = name_entry.get()
        role = role_entry.get()
        if not name or not role:
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            db.execute_query("UPDATE staff SET name = %s, role = %s WHERE id = %s", (name, role, staff_id))
            messagebox.showinfo("Success", "Updated")
            clear()
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Delete
    def delete():
        if not tree.selection():
            messagebox.showwarning("Error", "Select staff")
            return
        staff_id = tree.item(tree.selection()[0])['values'][0]
        try:
            db.execute_query("DELETE FROM staff WHERE id = %s", (staff_id,))
            messagebox.showinfo("Success", "Deleted")
            load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Load
    def load():
        for item in tree.get_children():
            tree.delete(item)
        try:
            for row in db.fetch_all("SELECT id, name, role FROM staff"):
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
    
    # Expose
    frame.load = load
    return frame
