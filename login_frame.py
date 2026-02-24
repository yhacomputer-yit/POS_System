import tkinter as tk
from tkinter import messagebox


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="POS System Login", font=("Arial", 20, "bold")).pack(pady=30)
        
        input_frame = tk.Frame(self)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.username_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(input_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Button(self, text="Login", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15, command=self.login).pack(pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "password":
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
