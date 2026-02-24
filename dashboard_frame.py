import tkinter as tk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self, text="POS System Dashboard", font=("Arial", 20, "bold")).pack(pady=20)
        
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20)
        
        # POS Sales button (prominent)
        tk.Button(main_frame, text="POS Sales", font=("Arial", 14, "bold"),
                  bg="#4CAF50", fg="white", width=20, height=2,
                  command=lambda: self.controller.show_frame("POS")).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        
        # Management section
        tk.Label(main_frame, text="Management", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=10)
        
        buttons = [
            ("Category", "CategoryCRUD"),
            ("Item", "ItemCRUD"),
            ("Staff", "StaffCRUD"),
            ("Safe List", "SafeList")
        ]
        
        for i, (text, frame) in enumerate(buttons):
            row = 2 + (i // 2)
            col = i % 2
            tk.Button(main_frame, text=f"{text} CRUD" if text != "Safe List" else text, width=15, height=2,
                     command=lambda f=frame: self.controller.show_frame(f)).grid(row=row, column=col, pady=5, padx=5)
        
        # Logout button
        tk.Button(self, text="Logout", bg="#f44336", fg="white", width=20, height=2,
                 command=lambda: self.controller.show_frame("Login")).pack(pady=20)
