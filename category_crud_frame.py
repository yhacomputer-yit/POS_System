import tkinter as tk
from tkinter import ttk, messagebox

class CategoryCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        title_label = tk.Label(self, text="Category Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Category Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.category_name_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.category_name_entry.grid(row=0, column=1, pady=5, padx=10)

        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Create", bg="#4CAF50", fg="white", width=10,
                 command=self.create_category).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update", bg="#2196F3", fg="white", width=10,
                 command=self.update_category).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", bg="#f44336", fg="white", width=10,
                 command=self.delete_category).grid(row=0, column=2, padx=5)

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.category_tree = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings", height=15)
        self.category_tree.heading("ID", text="ID")
        self.category_tree.heading("Name", text="Name")
        self.category_tree.column("ID", width=80)
        self.category_tree.column("Name", width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        self.category_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Refresh", width=15, command=self.load_categories).grid(row=0, column=0, padx=5)
        tk.Button(bottom_frame, text="Back to Dashboard", bg="#607d8b", fg="white", width=15,
                 command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=1, padx=5)

    def create_category(self):
        name = self.category_name_entry.get()
        if name:
            try:
                self.db.execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
                messagebox.showinfo("Success", "Category created successfully")
                self.category_name_entry.delete(0, tk.END)
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter category name")

    def update_category(self):
        selected = self.category_tree.selection()
        if selected:
            item = self.category_tree.item(selected[0])
            category_id = item['values'][0]
            name = self.category_name_entry.get()
            if name:
                try:
                    self.db.execute_query("UPDATE categories SET name = %s WHERE id = %s", (name, category_id))
                    messagebox.showinfo("Success", "Category updated successfully")
                    self.category_name_entry.delete(0, tk.END)
                    self.load_categories()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please enter category name")
        else:
            messagebox.showwarning("Selection Error", "Please select a category to update")

    def delete_category(self):
        selected = self.category_tree.selection()
        if selected:
            item = self.category_tree.item(selected[0])
            category_id = item['values'][0]
            try:
                self.db.execute_query("DELETE FROM categories WHERE id = %s", (category_id,))
                messagebox.showinfo("Success", "Category deleted successfully")
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select a category to delete")

    def load_categories(self):
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        try:
            categories = self.db.fetch_all("SELECT id, name FROM categories")
            for category in categories:
                self.category_tree.insert("", tk.END, values=category)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
