import tkinter as tk

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title
        title_label = tk.Label(self, text="POS System Dashboard", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Main buttons frame
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20)

        # POS Sales button (prominent)
        pos_button = tk.Button(main_frame, text="POS Sales", font=("Arial", 14, "bold"),
                              bg="#4CAF50", fg="white", width=20, height=2,
                              command=lambda: self.controller.show_frame("POS"))
        pos_button.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Management buttons
        tk.Label(main_frame, text="Management", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(main_frame, text="Category CRUD", width=15, height=2,
                 command=lambda: self.controller.show_frame("CategoryCRUD")).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(main_frame, text="Item CRUD", width=15, height=2,
                 command=lambda: self.controller.show_frame("ItemCRUD")).grid(row=2, column=1, pady=5, padx=5)
        tk.Button(main_frame, text="Staff CRUD", width=15, height=2,
                 command=lambda: self.controller.show_frame("StaffCRUD")).grid(row=3, column=0, pady=5, padx=5)
        tk.Button(main_frame, text="Safe List", width=15, height=2,
                 command=lambda: self.controller.show_frame("SafeList")).grid(row=3, column=1, pady=5, padx=5)

        # Logout button
        tk.Button(self, text="Logout", bg="#f44336", fg="white", width=20, height=2,
                 command=lambda: self.controller.show_frame("Login")).pack(pady=20)
