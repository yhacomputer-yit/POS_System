# first.py
import tkinter as tk
from main import start_main  # Import function from main.py

def start_first():
    root = tk.Tk()
    root.title("First Window")
    root.geometry("300x200")
    
    tk.Label(root, text="This is First.py").pack(pady=20)
    
    btn_back = tk.Button(root, text="Back to Main", command=lambda: redirect_to_main(root))
    btn_back.pack(pady=20)
    
    root.mainloop()

def redirect_to_main(current_window):
    current_window.destroy()  # Close first.py window
    start_main()              # Open main.py GUI
