import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# POS Sales Window
def create_pos_frame(parent, db, show_dashboard):
    frame = tk.Frame(parent)
    
    cart = []
    
    # Title
    tk.Label(frame, text="POS Sales", font=("Arial", 16, "bold")).pack(pady=10)
    
    content = tk.Frame(frame)
    content.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Left side - Items
    left = tk.Frame(content)
    left.pack(side="left", fill="both", expand=True, padx=5)
    
    tk.Label(left, text="Barcode:").pack(anchor="w")
    barcode_frame = tk.Frame(left)
    barcode_frame.pack(fill="x", pady=5)
    barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12))
    barcode_entry.pack(side="left", fill="x", expand=True)
    
    tk.Label(left, text="Items:").pack(anchor="w", pady=5)
    item_tree = ttk.Treeview(left, columns=("ID", "Name", "Price", "Barcode"), show="headings", height=15)
    for col in ("ID", "Name", "Price", "Barcode"):
        item_tree.heading(col, text=col)
        item_tree.column(col, width=100 if col != "Name" else 150)
    item_tree.pack(fill="both", expand=True)
    
    # Right side - Cart
    right = tk.Frame(content)
    right.pack(side="right", fill="both", expand=True, padx=5)
    
    tk.Label(right, text="Cart:").pack(anchor="w", pady=5)
    cart_tree = ttk.Treeview(right, columns=("Name", "Price", "Qty", "Total"), show="headings", height=10)
    for col in ("Name", "Price", "Qty", "Total"):
        cart_tree.heading(col, text=col)
        cart_tree.column(col, width=80 if col != "Name" else 120)
    cart_tree.pack(fill="both", expand=True)
    
    # Cart controls
    cart_btn = tk.Frame(right)
    cart_btn.pack(fill="x", pady=5)
    
    # Total
    total_frame = tk.Frame(right)
    total_frame.pack(fill="x", pady=10)
    tk.Label(total_frame, text="Total:", font=("Arial", 12, "bold")).pack(side="left")
    total_label = tk.Label(total_frame, text="0.00", font=("Arial", 12, "bold"), fg="green")
    total_label.pack(side="right")
    
    # Staff selection
    tk.Label(right, text="Staff:").pack(anchor="w", pady=5)
    staff_var = tk.StringVar()
    staff_menu = ttk.Combobox(right, textvariable=staff_var)
    staff_menu.pack(fill="x", pady=5)
    
    # Load items
    def load_items():
        for item in item_tree.get_children():
            item_tree.delete(item)
        try:
            for row in db.fetch_all("SELECT id, name, price, barcode FROM items"):
                item_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Load staff
    def load_staff():
        try:
            staff = db.fetch_all("SELECT id, name FROM staff")
            staff_menu["values"] = [f"{s[0]} - {s[1]}" for s in staff]
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Search barcode
    def search_barcode(event=None):
        barcode = barcode_entry.get().strip()
        if not barcode:
            return
        for item in item_tree.get_children():
            if item_tree.item(item, "values")[3] == barcode:
                item_tree.selection_set(item)
                item_tree.focus(item)
                add_to_cart()
                barcode_entry.delete(0, tk.END)
                return
        messagebox.showwarning("Not Found", "Item not found")
    
    barcode_entry.bind("<Return>", search_barcode)
    tk.Button(barcode_frame, text="Search", command=search_barcode).pack(side="right", padx=5)
    
    # Add to cart
    def add_to_cart(event=None):
        selected = item_tree.selection()
        if not selected:
            return
        item = item_tree.item(selected[0])
        item_id, name, price, barcode = item["values"]
        
        for cart_item in cart:
            if cart_item[0] == item_id:
                cart_item[3] += 1
                cart_item[4] = cart_item[2] * cart_item[3]
                update_cart()
                return
        
        cart.append([item_id, name, float(price), 1, float(price)])
        update_cart()
    
    item_tree.bind("<Double-1>", add_to_cart)
    
    # Update cart
    def update_cart():
        for item in cart_tree.get_children():
            cart_tree.delete(item)
        for cart_item in cart:
            cart_tree.insert("", tk.END, values=(cart_item[1], f"{cart_item[2]:.2f}", cart_item[3], f"{cart_item[4]:.2f}"))
        total_label.config(text=f"{sum(c[4] for c in cart):.2f}")
    
    # Cart buttons
    def increase_qty():
        if cart_tree.selection():
            idx = cart_tree.index(cart_tree.selection()[0])
            cart[idx][3] += 1
            cart[idx][4] = cart[idx][2] * cart[idx][3]
            update_cart()
    
    def decrease_qty():
        if cart_tree.selection():
            idx = cart_tree.index(cart_tree.selection()[0])
            if cart[idx][3] > 1:
                cart[idx][3] -= 1
                cart[idx][4] = cart[idx][2] * cart[idx][3]
                update_cart()
    
    def remove_item():
        if cart_tree.selection():
            idx = cart_tree.index(cart_tree.selection()[0])
            del cart[idx]
            update_cart()
    
    def clear_cart():
        cart.clear()
        update_cart()
    
    tk.Button(cart_btn, text="+", width=3, command=increase_qty).pack(side="left", padx=2)
    tk.Button(cart_btn, text="-", width=3, command=decrease_qty).pack(side="left", padx=2)
    tk.Button(cart_btn, text="Remove", command=remove_item).pack(side="left", padx=2)
    tk.Button(cart_btn, text="Clear", command=clear_cart).pack(side="right", padx=2)
    
    # Checkout
    def checkout():
        if not cart:
            messagebox.showwarning("Error", "Cart is empty")
            return
        staff = staff_var.get()
        if not staff:
            messagebox.showwarning("Error", "Select staff")
            return
        
        staff_id = int(staff.split(" - ")[0])
        total = sum(c[4] for c in cart)
        
        try:
            for item in cart:
                db.execute_query("INSERT INTO sales (item_id, quantity, total, date, staff_id) VALUES (%s, %s, %s, %s, %s)",
                             (item[0], item[3], item[4], datetime.now(), staff_id))
            db.execute_query("INSERT INTO safe_transactions (amount, type, date, staff_id) VALUES (%s, %s, %s, %s)",
                         (total, "Payment", datetime.now(), staff_id))
            messagebox.showinfo("Success", f"Sale complete! Total: ${total:.2f}")
            clear_cart()
            staff_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Print receipt
    def print_receipt():
        if not cart:
            messagebox.showwarning("Error", "Cart is empty")
            return
        staff = staff_var.get()
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
                    for item in cart:
                        f.write(f"{item[1]} x{item[3]} @ ${item[2]:.2f} = ${item[4]:.2f}\n")
                    f.write("-" * 30 + f"\nTotal: ${sum(c[4] for c in cart):.2f}\n")
                messagebox.showinfo("Success", "Saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    # Buttons
    btn_frame = tk.Frame(right)
    btn_frame.pack(fill="x", pady=10)
    tk.Button(btn_frame, text="Checkout", bg="#4CAF50", fg="white", command=checkout).pack(side="left", fill="x", expand=True, padx=5)
    tk.Button(btn_frame, text="Print", bg="#2196F3", fg="white", command=print_receipt).pack(side="right", fill="x", expand=True, padx=5)
    
    tk.Button(frame, text="Back to Dashboard", command=show_dashboard).pack(pady=10)
    
    # Expose
    frame.load_items = load_items
    frame.load_staff = load_staff
    return frame
