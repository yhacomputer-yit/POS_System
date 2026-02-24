import tkinter as tk
from tkinter import messagebox

# Login Window
def create_login_frame(parent, show_dashboard):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="POS System Login", font=("Arial", 20, "bold")).pack(pady=30)
    
    # Username
    tk.Label(frame, text="Username:", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
    username_entry.pack(pady=5)
    
    # Password
    tk.Label(frame, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
    password_entry.pack(pady=5)
    
    # Login Button
    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        if username == "admin" and password == "password":
            show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    tk.Button(frame, text="Login", bg="#4CAF50", fg="white", font=("Arial", 12), width=15, command=login).pack(pady=20)
    
    return frame
