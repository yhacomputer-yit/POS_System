import tkinter as tk
from tkinter import ttk, messagebox


class StaffCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="Staff Management", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Input
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Role:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.role_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.role_entry.grid(row=1, column=1, pady=5, padx=10)
        
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
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Role"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Role", text="Role")
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=200)
        self.tree.column("Role", width=150)
        
        self.tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview).pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        tk.Button(self, text="Refresh", width=15, command=self.load).pack(pady=10)
    
    def on_select(self, event):
        if self.tree.selection():
            values = self.tree.item(self.tree.selection()[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.role_entry.delete(0, tk.END)
            self.role_entry.insert(0, values[2])
    
    def create(self):
        name = self.name_entry.get()
        role = self.role_entry.get()
        if not name or not role:
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            self.db.execute_query("INSERT INTO staff (name, role) VALUES (%s, %s)", (name, role))
            messagebox.showinfo("Success", "Created")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select staff")
            return
        staff_id = self.tree.item(self.tree.selection()[0])['values'][0]
        name = self.name_entry.get()
        role = self.role_entry.get()
        if not name or not role:
            messagebox.showwarning("Error", "Fill all fields")
            return
        try:
            self.db.execute_query("UPDATE staff SET name = %s, role = %s WHERE id = %s", (name, role, staff_id))
            messagebox.showinfo("Success", "Updated")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select staff")
            return
        staff_id = self.tree.item(self.tree.selection()[0])['values'][0]
        try:
            self.db.execute_query("DELETE FROM staff WHERE id = %s", (staff_id,))
            messagebox.showinfo("Success", "Deleted")
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear(self):
        self.name_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
    
    def load(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for row in self.db.fetch_all("SELECT id, name, role FROM staff"):
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
