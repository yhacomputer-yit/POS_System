import tkinter as tk
from tkinter import ttk, messagebox

class POSSalesFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cart = []  # (name, price, qty, total)

        # Title
        tk.Label(self, text="POS Sales (UI Only)", font=("Arial", 16, "bold")).pack(pady=10)

        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- LEFT -----------------
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(left_frame, text="Items:", font=("Arial", 12, "bold")).pack(anchor="w")

        self.item_tree = ttk.Treeview(
            left_frame,
            columns=("Name", "Price"),
            show="headings",
            height=15
        )
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.column("Name", width=150)
        self.item_tree.column("Price", width=80)
        self.item_tree.pack(fill="both", expand=True)

        self.item_tree.bind("<Double-1>", self.add_to_cart)

        # ---------------- RIGHT -----------------
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(right_frame, text="Cart:", font=("Arial", 12, "bold")).pack(anchor="w")

        self.cart_tree = ttk.Treeview(
            right_frame,
            columns=("Name", "Price", "Qty", "Total"),
            show="headings",
            height=10
        )
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Total", text="Total")
        self.cart_tree.column("Name", width=120)
        self.cart_tree.column("Price", width=70)
        self.cart_tree.column("Qty", width=40)
        self.cart_tree.column("Total", width=80)
        self.cart_tree.pack(fill="both", expand=True)

        cart_buttons = tk.Frame(right_frame)
        cart_buttons.pack(fill="x", pady=5)

        tk.Button(cart_buttons, text="+ Qty", command=self.increase_qty).pack(side="left", padx=2)
        tk.Button(cart_buttons, text="- Qty", command=self.decrease_qty).pack(side="left", padx=2)
        tk.Button(cart_buttons, text="Remove", command=self.remove_item).pack(side="left", padx=2)
        tk.Button(cart_buttons, text="Clear", command=self.clear_cart).pack(side="right", padx=2)

        total_frame = tk.Frame(right_frame)
        total_frame.pack(fill="x", pady=10)
        tk.Label(total_frame, text="Total:", font=("Arial", 12, "bold")).pack(side="left")
        self.total_label = tk.Label(total_frame, text="0.00", font=("Arial", 12, "bold"), fg="green")
        self.total_label.pack(side="right")

        tk.Button(right_frame, text="Checkout", font=("Arial", 12, "bold"),
                 command=self.checkout).pack(fill="x", pady=5)
        
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("DashboardFrame")).pack(pady=10)

        # Load Demo Items
        self.load_demo_items()

    # --------------------------- Load Demo Items ---------------------------

    def load_demo_items(self):
        demo_items = [
            ("Coca Cola", 1500),
            ("Sprite", 1500),
            ("Milk Tea", 2500),
            ("Noodles", 1200),
            ("Coffee Mix", 300),
        ]
        for name, price in demo_items:
            self.item_tree.insert("", tk.END, values=(name, price))

    # --------------------------- Cart Logic ---------------------------

    def add_to_cart(self, event=None):
        selected = self.item_tree.selection()
        if not selected:
            return
        name, price = self.item_tree.item(selected[0])['values']

        for item in self.cart:
            if item[0] == name:
                item[2] += 1
                item[3] = item[1] * item[2]
                self.update_cart()
                return

        self.cart.append([name, price, 1, price])
        self.update_cart()

    def update_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)

        for item in self.cart:
            self.cart_tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3]))

        self.update_total()

    def increase_qty(self):
        selected = self.cart_tree.selection()
        if not selected: return

        index = self.cart_tree.index(selected[0])
        self.cart[index][2] += 1
        self.cart[index][3] = self.cart[index][1] * self.cart[index][2]
        self.update_cart()

    def decrease_qty(self):
        selected = self.cart_tree.selection()
        if not selected: return

        index = self.cart_tree.index(selected[0])
        if self.cart[index][2] > 1:
            self.cart[index][2] -= 1
            self.cart[index][3] = self.cart[index][1] * self.cart[index][2]
        self.update_cart()

    def remove_item(self):
        selected = self.cart_tree.selection()
        if not selected: return

        index = self.cart_tree.index(selected[0])
        del self.cart[index]
        self.update_cart()

    def clear_cart(self):
        self.cart = []
        self.update_cart()

    def update_total(self):
        total = sum(item[3] for item in self.cart)
        self.total_label.config(text=f"{total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items first!")
            return

        total = sum(item[3] for item in self.cart)
        messagebox.showinfo("Checkout", f"UI-only checkout success!\nTotal: {total} Ks")
        self.clear_cart()
