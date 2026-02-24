import tkinter as tk

def show_main():
    main_window.deiconify()   # Show main window
    first_window.withdraw()   # Hide first window

def show_first():
    first_window.deiconify()  # Show first window
    main_window.withdraw()    # Hide main window

# Main Window
main_window = tk.Tk()
main_window.title("Main Window")
main_window.geometry("300x200")

btn_to_first = tk.Button(main_window, text="Go to First.py", command=show_first)
btn_to_first.pack(pady=50)

# First Window
first_window = tk.Toplevel(main_window)
first_window.title("First Window")
first_window.geometry("300x200")
first_window.withdraw()  # Hide initially

tk.Label(first_window, text="This is First.py").pack(pady=20)
btn_back = tk.Button(first_window, text="Back to Main", command=show_main)
btn_back.pack(pady=20)

main_window.mainloop()
