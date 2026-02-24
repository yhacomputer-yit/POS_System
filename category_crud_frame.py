import tkinter as tk
from tkinter import ttk, messagebox


class CategoryCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="Category Management", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Input
        tk.Label(self, text="Category Name:").pack()
        self.name_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Create", bg="#4CAF50", fg="white", width=10, command=self.create).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", bg="#2196F3", fg="white", width=10, command=self.update).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", width=10, command=self.delete).grid(row=0, column=2, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=200)
        
        self.tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview).pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Bottom buttons
        bottom = tk.Frame(self)
        bottom.pack(pady=10)
        tk.Button(bottom, text="Refresh", width=15, command=self.load).grid(row=0, column=0, padx=5)
        tk.Button(bottom, text="Back to Dashboard", bg="#607d8b", fg="white", width=15, command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=1, padx=5)
    
    def on_select(self, event):
        if self.tree.selection():
            values = self.tree.item(self.tree.selection()[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
    
    def create(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Enter category name")
            return
        try:
            self.db.execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
            messagebox.showinfo("Success", "Created")
            self.name_entry.delete(0, tk.END)
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select category")
            return
        cat_id = self.tree.item(self.tree.selection()[0])['values'][0]
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Enter category name")
            return
        try:
            self.db.execute_query("UPDATE categories SET name = %s WHERE id = %s", (name, cat_id))
            messagebox.showinfo("Success", "Updated")
            self.name_entry.delete(0, tk.END)
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete(self):
        if not self.tree.selection():
            messagebox.showwarning("Error", "Select category")
            return
        cat_id = self.tree.item(self.tree.selection()[0])['values'][0]
        try:
            self.db.execute_query("DELETE FROM categories WHERE id = %s", (cat_id,))
            messagebox.showinfo("Success", "Deleted")
            self.load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for row in self.db.fetch_all("SELECT id, name FROM categories"):
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
