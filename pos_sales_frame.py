import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class POSSalesFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.cart = []
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="POS Sales", font=("Arial", 16, "bold")).pack(pady=10)
        
        content = tk.Frame(self)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Items
        left = tk.Frame(content)
        left.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(left, text="Barcode:").pack(anchor="w")
        barcode_frame = tk.Frame(left)
        barcode_frame.pack(fill="x", pady=5)
        self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12))
        self.barcode_entry.pack(side="left", fill="x", expand=True)
        self.barcode_entry.bind("<Return>", self.search_barcode)
        tk.Button(barcode_frame, text="Search", command=self.search_barcode).pack(side="right", padx=5)
        
        tk.Label(left, text="Items:").pack(anchor="w", pady=5)
        self.item_tree = ttk.Treeview(left, columns=("ID", "Name", "Price", "Barcode"), show="headings", height=15)
        for col in ("ID", "Name", "Price", "Barcode"):
            self.item_tree.heading(col, text=col)
            self.item_tree.column(col, width=100 if col != "Name" else 150)
        self.item_tree.pack(fill="both", expand=True)
        self.item_tree.bind("<Double-1>", self.add_to_cart)
        
        # Right side - Cart
        right = tk.Frame(content)
        right.pack(side="right", fill="both", expand=True, padx=5)
        
        tk.Label(right, text="Cart:").pack(anchor="w", pady=5)
        self.cart_tree = ttk.Treeview(right, columns=("Name", "Price", "Qty", "Total"), show="headings", height=10)
        for col in ("Name", "Price", "Qty", "Total"):
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=80 if col != "Name" else 120)
        self.cart_tree.pack(fill="both", expand=True)
        
        # Cart controls
        cart_btn = tk.Frame(right)
        cart_btn.pack(fill="x", pady=5)
        tk.Button(cart_btn, text="+", width=3, command=self.increase_qty).pack(side="left", padx=2)
        tk.Button(cart_btn, text="-", width=3, command=self.decrease_qty).pack(side="left", padx=2)
        tk.Button(cart_btn, text="Remove", command=self.remove_item).pack(side="left", padx=2)
        tk.Button(cart_btn, text="Clear", command=self.clear_cart).pack(side="right", padx=2)
        
        # Total
        total_frame = tk.Frame(right)
        total_frame.pack(fill="x", pady=10)
        tk.Label(total_frame, text="Total:", font=("Arial", 12, "bold")).pack(side="left")
        self.total_label = tk.Label(total_frame, text="0.00", font=("Arial", 12, "bold"), fg="green")
        self.total_label.pack(side="right")
        
        # Staff selection
        tk.Label(right, text="Staff:").pack(anchor="w", pady=5)
        self.staff_var = tk.StringVar()
        self.staff_menu = ttk.Combobox(right, textvariable=self.staff_var)
        self.staff_menu.pack(fill="x", pady=5)
        
        # Checkout buttons
        btn_frame = tk.Frame(right)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Checkout", bg="#4CAF50", fg="white", command=self.checkout).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(btn_frame, text="Print", bg="#2196F3", fg="white", command=self.print_receipt).pack(side="right", fill="x", expand=True, padx=5)
        
        tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame("Dashboard")).pack(pady=10)
        
        self.load_items()
        self.load_staff()
    
    def load_items(self):
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        try:
            for row in self.db.fetch_all("SELECT id, name, price, barcode FROM items"):
                self.item_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_staff(self):
        try:
            staff = self.db.fetch_all("SELECT id, name FROM staff")
            self.staff_menu["values"] = [f"{s[0]} - {s[1]}" for s in staff]
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def search_barcode(self, event=None):
        barcode = self.barcode_entry.get().strip()
        if not barcode:
            return
        for item in self.item_tree.get_children():
            if self.item_tree.item(item, "values")[3] == barcode:
                self.item_tree.selection_set(item)
                self.item_tree.focus(item)
                self.add_to_cart()
                self.barcode_entry.delete(0, tk.END)
                return
        messagebox.showwarning("Not Found", "Item not found")
    
    def add_to_cart(self, event=None):
        selected = self.item_tree.selection()
        if not selected:
            return
        item = self.item_tree.item(selected[0])
        item_id, name, price, barcode = item["values"]
        
        for cart_item in self.cart:
            if cart_item[0] == item_id:
                cart_item[3] += 1
                cart_item[4] = cart_item[2] * cart_item[3]
                self.update_cart()
                return
        
        self.cart.append([item_id, name, float(price), 1, float(price)])
        self.update_cart()
    
    def update_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for cart_item in self.cart:
            self.cart_tree.insert("", tk.END, values=(cart_item[1], f"{cart_item[2]:.2f}", cart_item[3], f"{cart_item[4]:.2f}"))
        self.total_label.config(text=f"{sum(c[4] for c in self.cart):.2f}")
    
    def increase_qty(self):
        if self.cart_tree.selection():
            idx = self.cart_tree.index(self.cart_tree.selection()[0])
            self.cart[idx][3] += 1
            self.cart[idx][4] = self.cart[idx][2] * self.cart[idx][3]
            self.update_cart()
    
    def decrease_qty(self):
        if self.cart_tree.selection():
            idx = self.cart_tree.index(self.cart_tree.selection()[0])
            if self.cart[idx][3] > 1:
                self.cart[idx][3] -= 1
                self.cart[idx][4] = self.cart[idx][2] * self.cart[idx][3]
                self.update_cart()
    
    def remove_item(self):
        if self.cart_tree.selection():
            idx = self.cart_tree.index(self.cart_tree.selection()[0])
            del self.cart[idx]
            self.update_cart()
    
    def clear_cart(self):
        self.cart = []
        self.update_cart()
    
    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Error", "Cart is empty")
            return
        staff = self.staff_var.get()
        if not staff:
            messagebox.showwarning("Error", "Select staff")
            return
        
        staff_id = int(staff.split(" - ")[0])
        total = sum(c[4] for c in self.cart)
        
        try:
            for item in self.cart:
                self.db.execute_query("INSERT INTO sales (item_id, quantity, total, date, staff_id) VALUES (%s, %s, %s, %s, %s)",
                                     (item[0], item[3], item[4], datetime.now(), staff_id))
            self.db.execute_query("INSERT INTO safe_transactions (amount, type, date, staff_id) VALUES (%s, %s, %s, %s)",
                                 (total, "Payment", datetime.now(), staff_id))
            messagebox.showinfo("Success", f"Sale complete! Total: ${total:.2f}")
            self.clear_cart()
            self.staff_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def print_receipt(self):
        if not self.cart:
            messagebox.showwarning("Error", "Cart is empty")
            return
        staff = self.staff_var.get()
        if not staff:
            messagebox.showwarning("Error", "Select staff")
            return
        
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            try:
                with open(path, "w") as f:
                    f.write("POS Receipt\n" + "=" * 30 + "\n")
                    f.write(f"Date: {datetime.now()}\nStaff: {staff}\n" + "-" * 30 + "\n")
                    for item in self.cart:
                        f.write(f"{item[1]} x{item[3]} @ ${item[2]:.2f} = ${item[4]:.2f}\n")
                    f.write("-" * 30 + f"\nTotal: ${sum(c[4] for c in self.cart):.2f}\n")
                messagebox.showinfo("Success", "Saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
