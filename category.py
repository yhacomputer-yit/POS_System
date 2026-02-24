import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

db = Database()

def create_category():
    name = category_name_entry.get()
    if name.strip() == "":
        messagebox.showerror("Error", "Category name required!")
        return

    db.execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
    messagebox.showinfo("Success", "Data add success")

    load_data()
    category_name_entry.delete(0, tk.END)

def load_data():
    category_tree.delete(*category_tree.get_children())
    data = db.fetch_all("SELECT * FROM categories")
    for cat in data:
        category_tree.insert("", "end", values=cat)

def update_category():
    selected = category_tree.focus()
    if selected == "":
        messagebox.showerror("Error", "Select Category")
        return

    values = category_tree.item(selected, "values")
    cat_id = values[0]

    new_name = category_name_entry.get()
    if new_name.strip() == "":
        messagebox.showerror("Error", "Category name required")
        return

    db.execute_query("UPDATE categories SET name=%s WHERE id=%s", (new_name, cat_id))
    messagebox.showinfo("Success", "Category updated!")

    load_data()

def delete_category():
    selected = category_tree.focus()
    if selected == "":
        messagebox.showerror("Error", "Select Category")
        return

    values = category_tree.item(selected, "values")
    cat_id = values[0]
    db.execute_query("DELETE FROM categories WHERE id=%s", (cat_id,))
    messagebox.showinfo("Success", "Category deleted!")
    load_data()
root = tk.Tk()
root.title("Category Management")
root.geometry("400x500")

tk.Label(root, text="Category Management", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Category Name:").pack()
category_name_entry = tk.Entry(root, width=30)
category_name_entry.pack(pady=5)

tk.Button(root, text="Create", command=create_category).pack(pady=3)
tk.Button(root, text="Update", command=update_category).pack(pady=3)
tk.Button(root, text="Delete",command=delete_category).pack(pady=3)   # delete not added yet

category_tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings", height=10)
category_tree.heading("ID", text="ID")
category_tree.heading("Name", text="Name")
category_tree.pack(pady=10)

load_data()
root.mainloop()
