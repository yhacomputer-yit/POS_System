import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class POSSalesFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.cart = []  # List of (item_id, name, price, quantity, total)

        # Title
        tk.Label(self, text="POS Sales", font=("Arial", 16, "bold")).pack(pady=10)

        # Main content frame
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left side - Item selection
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Barcode search
        tk.Label(left_frame, text="Barcode Search:", font=("Arial", 10, "bold")).pack(anchor="w")
        barcode_frame = tk.Frame(left_frame)
        barcode_frame.pack(fill="x", pady=5)
        self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12))
        self.barcode_entry.pack(side="left", fill="x", expand=True)
        self.barcode_entry.bind("<Return>", self.search_by_barcode)
        tk.Button(barcode_frame, text="Search", command=self.search_by_barcode).pack(side="right", padx=5)

        # Item list
        tk.Label(left_frame, text="Items:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.item_tree = ttk.Treeview(left_frame, columns=("ID", "Name", "Price", "Barcode"), show="headings", height=15)
        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.heading("Barcode", text="Barcode")
        self.item_tree.column("ID", width=50)
        self.item_tree.column("Name", width=150)
        self.item_tree.column("Price", width=80)
        self.item_tree.column("Barcode", width=100)
        self.item_tree.pack(fill="both", expand=True)
        self.item_tree.bind("<Double-1>", self.add_to_cart)

        # Right side - Cart and checkout
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Cart
        tk.Label(right_frame, text="Cart:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cart_tree = ttk.Treeview(right_frame, columns=("Name", "Price", "Qty", "Total"), show="headings", height=10)
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Total", text="Total")
        self.cart_tree.column("Name", width=120)
        self.cart_tree.column("Price", width=80)
        self.cart_tree.column("Qty", width=50)
        self.cart_tree.column("Total", width=80)
        self.cart_tree.pack(fill="both", expand=True)

        # Cart controls
        cart_controls = tk.Frame(right_frame)
        cart_controls.pack(fill="x", pady=5)
        tk.Button(cart_controls, text="+ Qty", command=self.increase_qty).pack(side="left", padx=2)
        tk.Button(cart_controls, text="- Qty", command=self.decrease_qty).pack(side="left", padx=2)
        tk.Button(cart_controls, text="Remove", command=self.remove_from_cart).pack(side="left", padx=2)
        tk.Button(cart_controls, text="Clear Cart", command=self.clear_cart).pack(side="right", padx=2)

        # Total
        total_frame = tk.Frame(right_frame)
        total_frame.pack(fill="x", pady=10)
        tk.Label(total_frame, text="Total:", font=("Arial", 12, "bold")).pack(side="left")
        self.total_label = tk.Label(total_frame, text="0.00", font=("Arial", 12, "bold"), fg="green")
        self.total_label.pack(side="right")

        # Staff selection
        tk.Label(right_frame, text="Staff:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.staff_var = tk.StringVar()
        self.staff_menu = ttk.Combobox(right_frame, textvariable=self.staff_var)
        self.staff_menu.pack(fill="x", pady=5)

        # Checkout and Print
        button_frame = tk.Frame(right_frame)
        button_frame.pack(fill="x", pady=10)
        tk.Button(button_frame, text="Checkout", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 command=self.checkout).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(button_frame, text="Print Receipt", bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                 command=self.print_receipt).pack(side="right", fill="x", expand=True, padx=5)

        # Back button
        tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame("Dashboard")).pack(pady=10)

        # Load data
        self.load_items()
        self.load_staff()

    def load_items(self):
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        try:
            items = self.db.fetch_all("SELECT id, name, price, barcode FROM items")
            for item in items:
                self.item_tree.insert("", tk.END, values=item)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_staff(self):
        try:
            staff = self.db.fetch_all("SELECT id, name FROM staff")
            self.staff_menu['values'] = [f"{s[0]} - {s[1]}" for s in staff]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_by_barcode(self, event=None):
        barcode = self.barcode_entry.get().strip()
        if barcode:
            for item in self.item_tree.get_children():
                item_values = self.item_tree.item(item, 'values')
                if item_values[3] == barcode:  # Barcode is column 3
                    self.item_tree.selection_set(item)
                    self.item_tree.focus(item)
                    self.item_tree.see(item)
                    self.add_to_cart()
                    self.barcode_entry.delete(0, tk.END)
                    return
            messagebox.showwarning("Not Found", "Item with this barcode not found")
        else:
            messagebox.showwarning("Input Error", "Please enter a barcode")

    def add_to_cart(self, event=None):
        selected = self.item_tree.selection()
        if selected:
            item = self.item_tree.item(selected[0])
            item_id, name, price, barcode = item['values']

            # Check if item already in cart
            for cart_item in self.cart:
                if cart_item[0] == item_id:
                    cart_item[3] += 1  # Increase quantity
                    cart_item[4] = cart_item[2] * cart_item[3]  # Update total
                    self.update_cart_display()
                    self.update_total()
                    return

            # Add new item to cart
            self.cart.append([item_id, name, float(price), 1, float(price)])
            self.update_cart_display()
            self.update_total()

    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for cart_item in self.cart:
            self.cart_tree.insert("", tk.END, values=(cart_item[1], f"{cart_item[2]:.2f}", cart_item[3], f"{cart_item[4]:.2f}"))

    def increase_qty(self):
        selected = self.cart_tree.selection()
        if selected:
            index = self.cart_tree.index(selected[0])
            self.cart[index][3] += 1
            self.cart[index][4] = self.cart[index][2] * self.cart[index][3]
            self.update_cart_display()
            self.update_total()

    def decrease_qty(self):
        selected = self.cart_tree.selection()
        if selected:
            index = self.cart_tree.index(selected[0])
            if self.cart[index][3] > 1:
                self.cart[index][3] -= 1
                self.cart[index][4] = self.cart[index][2] * self.cart[index][3]
                self.update_cart_display()
                self.update_total()

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if selected:
            index = self.cart_tree.index(selected[0])
            del self.cart[index]
            self.update_cart_display()
            self.update_total()

    def clear_cart(self):
        self.cart = []
        self.update_cart_display()
        self.update_total()

    def update_total(self):
        total = sum(item[4] for item in self.cart)
        self.total_label.config(text=f"{total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart before checkout")
            return

        staff_selection = self.staff_var.get()
        if not staff_selection:
            messagebox.showwarning("Staff Required", "Please select a staff member")
            return

        staff_id = int(staff_selection.split(' - ')[0])

        try:
            total_amount = sum(item[4] for item in self.cart)
            for cart_item in self.cart:
                item_id, name, price, qty, total = cart_item
                self.db.execute_query(
                    "INSERT INTO sales (item_id, quantity, total, date, staff_id) VALUES (%s, %s, %s, %s, %s)",
                    (item_id, qty, total, datetime.now(), staff_id)
                )

            # Record in safe_transactions as payment
            self.db.execute_query(
                "INSERT INTO safe_transactions (amount, type, date, staff_id) VALUES (%s, %s, %s, %s)",
                (total_amount, "Payment", datetime.now(), staff_id)
            )

            messagebox.showinfo("Success", f"Sale completed! Total: ${total_amount:.2f}")
            self.clear_cart()
            self.staff_var.set("")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def print_receipt(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart before printing receipt")
            return

        staff_selection = self.staff_var.get()
        if not staff_selection:
            messagebox.showwarning("Staff Required", "Please select a staff member")
            return

        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write("POS Receipt\n")
                    f.write("=" * 30 + "\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Staff: {staff_selection}\n")
                    f.write("-" * 30 + "\n")
                    for cart_item in self.cart:
                        name, price, qty, total = cart_item[1], cart_item[2], cart_item[3], cart_item[4]
                        f.write(f"{name} x{qty} @ ${price:.2f} = ${total:.2f}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Total: ${sum(item[4] for item in self.cart):.2f}\n")
                messagebox.showinfo("Success", "Receipt printed to file")
            except Exception as e:
                messagebox.showerror("Error", str(e))
