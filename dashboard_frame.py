import tkinter as tk

# Dashboard Window
def create_dashboard_frame(parent, show_category, show_item, show_staff, show_safe_list, show_pos, show_login):
    frame = tk.Frame(parent)
    
    # Title
    tk.Label(frame, text="POS System Dashboard", font=("Arial", 20, "bold")).pack(pady=20)
    
    # POS Sales Button
    tk.Button(frame, text="POS Sales", font=("Arial", 14, "bold"),
              bg="#4CAF50", fg="white", width=20, height=2,
              command=show_pos).pack(pady=10)
    
    # Management Section
    tk.Label(frame, text="Management", font=("Arial", 14, "bold")).pack(pady=10)
    
    # CRUD Buttons
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Category", width=15, height=2, command=show_category).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Item", width=15, height=2, command=show_item).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Staff", width=15, height=2, command=show_staff).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Safe List", width=15, height=2, command=show_safe_list).grid(row=1, column=1, padx=5, pady=5)
    
    # Logout Button
    tk.Button(frame, text="Logout", bg="#f44336", fg="white", width=20, height=2,
              command=show_login).pack(pady=20)
    
    return frame
