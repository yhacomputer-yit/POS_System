import tkinter as tk
from tkinter import ttk, messagebox

class StaffCRUDFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        title_label = tk.Label(self, text="Staff Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Staff Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.staff_name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.staff_name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(input_frame, text="Role:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.staff_role_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.staff_role_entry.grid(row=1, column=1, pady=5, padx=10)

        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Create", bg="#4CAF50", fg="white", width=10,
                 command=self.create_staff).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update", bg="#2196F3", fg="white", width=10,
                 command=self.update_staff).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", bg="#f44336", fg="white", width=10,
                 command=self.delete_staff).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Back to Dashboard", bg="#607d8b", fg="white", width=15,
                 command=lambda: self.controller.show_frame("Dashboard")).grid(row=0, column=3, padx=5)

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.staff_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Role"), show="headings", height=15)
        self.staff_tree.heading("ID", text="ID")
        self.staff_tree.heading("Name", text="Name")
        self.staff_tree.heading("Role", text="Role")
        self.staff_tree.column("ID", width=80)
        self.staff_tree.column("Name", width=200)
        self.staff_tree.column("Role", width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.staff_tree.yview)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)

        self.staff_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Refresh", width=15, command=self.load_staff).grid(row=0, column=0, padx=5)



    def create_staff(self):
        name = self.staff_name_entry.get()
        role = self.staff_role_entry.get()
        if name and role:
            try:
                self.db.execute_query("INSERT INTO staff (name, role) VALUES (%s, %s)", (name, role))
                messagebox.showinfo("Success", "Staff created successfully")
                self.staff_name_entry.delete(0, tk.END)
                self.staff_role_entry.delete(0, tk.END)
                self.load_staff()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter name and role")

    def update_staff(self):
        selected = self.staff_tree.selection()
        if selected:
            item = self.staff_tree.item(selected[0])
            staff_id = item['values'][0]
            name = self.staff_name_entry.get()
            role = self.staff_role_entry.get()
            if name and role:
                try:
                    self.db.execute_query("UPDATE staff SET name = %s, role = %s WHERE id = %s", (name, role, staff_id))
                    messagebox.showinfo("Success", "Staff updated successfully")
                    self.staff_name_entry.delete(0, tk.END)
                    self.staff_role_entry.delete(0, tk.END)
                    self.load_staff()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please enter name and role")
        else:
            messagebox.showwarning("Selection Error", "Please select staff to update")

    def delete_staff(self):
        selected = self.staff_tree.selection()
        if selected:
            item = self.staff_tree.item(selected[0])
            staff_id = item['values'][0]
            try:
                self.db.execute_query("DELETE FROM staff WHERE id = %s", (staff_id,))
                messagebox.showinfo("Success", "Staff deleted successfully")
                self.load_staff()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select staff to delete")

    def load_staff(self):
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
        try:
            staff = self.db.fetch_all("SELECT id, name, role FROM staff")
            for s in staff:
                self.staff_tree.insert("", tk.END, values=s)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
