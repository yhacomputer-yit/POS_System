import tkinter as tk
from tkinter import ttk, messagebox

class ItemCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        title_label = tk.Label(self, text="Item Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Row 1: Name and Price
        tk.Label(input_frame, text="Item Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.item_name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.item_name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(input_frame, text="Price:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", pady=5)
        self.item_price_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.item_price_entry.grid(row=0, column=3, pady=5, padx=10)

        # Row 2: Barcode and Category
        tk.Label(input_frame, text="Barcode:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.item_barcode_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.item_barcode_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(input_frame, text="Category:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", pady=5)
        self.item_category_var = tk.StringVar()
        self.item_category_menu = ttk.Combobox(input_frame, textvariable=self.item_category_var, font=("Arial", 12), width=15)
        self.item_category_menu.grid(row=1, column=3, pady=5, padx=10)

        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(button_frame, text="Create", bg="#4CAF50", fg="white", width=10,
                 command=self.create_item).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update", bg="#2196F3", fg="white", width=10,
                 command=self.update_item).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", bg="#f44336", fg="white", width=10,
                 command=self.delete_item).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Back to Dashboard", bg="#607d8b", fg="white", width=15,
                 command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=3, padx=5)

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.item_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Barcode", "Category"), show="headings", height=15)
        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.heading("Barcode", text="Barcode")
        self.item_tree.heading("Category", text="Category")
        self.item_tree.column("ID", width=60)
        self.item_tree.column("Name", width=150)
        self.item_tree.column("Price", width=80)
        self.item_tree.column("Barcode", width=120)
        self.item_tree.column("Category", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)

        self.item_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Refresh", width=15, command=self.load_items).grid(row=0, column=0, padx=5)



    def load_categories_for_item(self):
        try:
            categories = self.db.fetch_all("SELECT id, name FROM categories")
            self.item_category_menu['values'] = [f"{cat[0]} - {cat[1]}" for cat in categories]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def create_item(self):
        name = self.item_name_entry.get()
        price = self.item_price_entry.get()
        barcode = self.item_barcode_entry.get()
        category = self.item_category_var.get().split(' - ')[0] if self.item_category_var.get() else None
        if name and price and barcode and category:
            try:
                self.db.execute_query("INSERT INTO items (name, price, barcode, category_id) VALUES (%s, %s, %s, %s)", (name, float(price), barcode, int(category)))
                messagebox.showinfo("Success", "Item created successfully")
                self.item_name_entry.delete(0, tk.END)
                self.item_price_entry.delete(0, tk.END)
                self.item_barcode_entry.delete(0, tk.END)
                self.item_category_var.set("")
                self.load_items()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter all fields")

    def update_item(self):
        selected = self.item_tree.selection()
        if selected:
            item = self.item_tree.item(selected[0])
            item_id = item['values'][0]
            name = self.item_name_entry.get()
            price = self.item_price_entry.get()
            barcode = self.item_barcode_entry.get()
            category = self.item_category_var.get().split(' - ')[0] if self.item_category_var.get() else None
            if name and price and barcode and category:
                try:
                    self.db.execute_query("UPDATE items SET name = %s, price = %s, barcode = %s, category_id = %s WHERE id = %s", (name, float(price), barcode, int(category), item_id))
                    messagebox.showinfo("Success", "Item updated successfully")
                    self.item_name_entry.delete(0, tk.END)
                    self.item_price_entry.delete(0, tk.END)
                    self.item_barcode_entry.delete(0, tk.END)
                    self.item_category_var.set("")
                    self.load_items()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please enter all fields")
        else:
            messagebox.showwarning("Selection Error", "Please select an item to update")

    def delete_item(self):
        selected = self.item_tree.selection()
        if selected:
            item = self.item_tree.item(selected[0])
            item_id = item['values'][0]
            try:
                self.db.execute_query("DELETE FROM items WHERE id = %s", (item_id,))
                messagebox.showinfo("Success", "Item deleted successfully")
                self.load_items()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select an item to delete")

    def load_items(self):
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        try:
            items = self.db.fetch_all("SELECT i.id, i.name, i.price, i.barcode, c.name FROM items i JOIN categories c ON i.category_id = c.id")
            for item in items:
                self.item_tree.insert("", tk.END, values=item)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
