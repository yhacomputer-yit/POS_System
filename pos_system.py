# POS System with MySQL Connection
# Features: Login, Main Dashboard, Category CRUD, Item CRUD (with barcode), Staff CRUD, Safe Page (print), Safe List (report)

import tkinter as tk
from database import Database
from login_frame import LoginFrame
from dashboard_frame import DashboardFrame
from category_crud_frame import CategoryCRUDFrame
from item_crud_frame import ItemCRUDFrame
from staff_crud_frame import StaffCRUDFrame
from pos_sales_frame import POSSalesFrame
from safe_list_frame import SafeListFrame

class POSApp:   
    def __init__(self, root):
        self.root = root
        self.root.title("POS System")
        self.root.geometry("800x600")

        self.db = Database()

        self.frames = {}
        self.create_frames()

        self.show_frame("Login")

    def create_frames(self):
        self.frames["Login"] = LoginFrame(self.root, self, self.db)
        self.frames["Dashboard"] = DashboardFrame(self.root, self)
        self.frames["CategoryCRUD"] = CategoryCRUDFrame(self.root, self, self.db)
        self.frames["ItemCRUD"] = ItemCRUDFrame(self.root, self, self.db)
        self.frames["StaffCRUD"] = StaffCRUDFrame(self.root, self, self.db)
        self.frames["POS"] = POSSalesFrame(self.root, self, self.db)
        self.frames["SafeList"] = SafeListFrame(self.root, self, self.db)

        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)
        
        if frame_name == "CategoryCRUD":
            self.frames[frame_name].load()
        elif frame_name == "ItemCRUD":
            self.frames[frame_name].load_categories()
            self.frames[frame_name].load()
        elif frame_name == "StaffCRUD":
            self.frames[frame_name].load()
        elif frame_name == "SafeList":
            self.frames[frame_name].load()
        elif frame_name == "POS":
            self.frames[frame_name].load_items()
            self.frames[frame_name].load_staff()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
