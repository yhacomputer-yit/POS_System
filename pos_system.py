import tkinter as tk
from database import Database
from login_frame import create_login_frame
from dashboard_frame import create_dashboard_frame
from category_crud_frame import create_category_frame
from item_crud_frame import create_item_frame
from staff_crud_frame import create_staff_frame
from pos_sales_frame import create_pos_frame
from safe_list_frame import create_safe_list_frame

# Main App
def main():
    db = Database()
    
    root = tk.Tk()
    root.title("POS System")
    root.geometry("800x600")
    
    # Container for all frames
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)
    
    # Store frames
    frames = {}
    
    # Show frame function (defined early)
    def show_frame(frame_name):
        # Hide all frames first
        for f in frames.values():
            f.pack_forget()
        # Show the requested frame
        frames[frame_name].pack(fill="both", expand=True)
        
        # Load data when showing certain frames
        if frame_name == "category":
            frames["category"].load()
        elif frame_name == "item":
            frames["item"].load_categories()
            frames["item"].load()
        elif frame_name == "staff":
            frames["staff"].load()
        elif frame_name == "safe_list":
            frames["safe_list"].load()
        elif frame_name == "pos":
            frames["pos"].load_items()
            frames["pos"].load_staff()
    
    # Create show_frame lambdas
    show_category = lambda: show_frame("category")
    show_item = lambda: show_frame("item")
    show_staff = lambda: show_frame("staff")
    show_safe_list = lambda: show_frame("safe_list")
    show_pos = lambda: show_frame("pos")
    show_login = lambda: show_frame("login")
    show_dashboard = lambda: show_frame("dashboard")
    
    # Create all frames
    frames["login"] = create_login_frame(container, show_dashboard)
    frames["dashboard"] = create_dashboard_frame(container, show_category, show_item, show_staff, show_safe_list, show_pos, show_login)
    frames["category"] = create_category_frame(container, db, show_dashboard)
    frames["item"] = create_item_frame(container, db, show_dashboard)
    frames["staff"] = create_staff_frame(container, db, show_dashboard)
    frames["pos"] = create_pos_frame(container, db, show_dashboard)
    frames["safe_list"] = create_safe_list_frame(container, db, show_dashboard)
    
    # Show login first
    show_frame("login")
    
    root.mainloop()

if __name__ == "__main__":
    main()
