import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class SafePageFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        # Title
        title_label = tk.Label(self, text="Safe Transaction", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Amount:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.safe_amount_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.safe_amount_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(input_frame, text="Type:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        type_frame = tk.Frame(input_frame)
        type_frame.grid(row=1, column=1, sticky="w", pady=5)
        self.safe_type_var = tk.StringVar(value="Deposit")
        tk.Radiobutton(type_frame, text="Deposit", variable=self.safe_type_var, value="Deposit", font=("Arial", 10)).pack(side="left", padx=10)
        tk.Radiobutton(type_frame, text="Withdrawal", variable=self.safe_type_var, value="Withdrawal", font=("Arial", 10)).pack(side="left", padx=10)

        tk.Label(input_frame, text="Staff:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.staff_var = tk.StringVar()
        self.staff_menu = ttk.Combobox(input_frame, textvariable=self.staff_var, font=("Arial", 12), width=18)
        self.staff_menu.grid(row=2, column=1, pady=5, padx=10)

        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Submit Transaction", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 width=20, command=self.submit_safe_transaction).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Print Receipt", bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                 width=20, command=self.print_receipt).grid(row=0, column=1, padx=10)

        # Back button
        tk.Button(self, text="Back to Dashboard", bg="#607d8b", fg="white", font=("Arial", 10, "bold"),
                 width=25, command=lambda: self.controller.show_frame("Dashboard")).pack(pady=20)

        # Load staff
        self.load_staff()

    def submit_safe_transaction(self):
        amount = self.safe_amount_entry.get()
        trans_type = self.safe_type_var.get()
        staff_selection = self.staff_var.get()
        if amount and staff_selection:
            staff_id = int(staff_selection.split(' - ')[0])
            try:
                self.db.execute_query("INSERT INTO safe_transactions (amount, type, date, staff_id) VALUES (%s, %s, %s, %s)", (float(amount), trans_type, datetime.now(), staff_id))
                messagebox.showinfo("Success", "Transaction submitted successfully")
                self.safe_amount_entry.delete(0, tk.END)
                self.staff_var.set("")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter amount and select staff")

    def load_staff(self):
        try:
            staff = self.db.fetch_all("SELECT id, name FROM staff")
            self.staff_menu['values'] = [f"{s[0]} - {s[1]}" for s in staff]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def print_receipt(self):
        # Simple print to file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write("POS Safe Receipt\n")
                f.write(f"Amount: {self.safe_amount_entry.get()}\n")
                f.write(f"Type: {self.safe_type_var.get()}\n")
                f.write(f"Date: {datetime.now()}\n")
            messagebox.showinfo("Success", "Receipt printed to file")
