import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from main_content import initialize_main_content
from sidebar_left import create_sidebar_left

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

main_frame, show_lesson_list, show_in_main = initialize_main_content(root)

create_sidebar_left(root, show_in_main)

main_frame.pack(side="left", fill="both", expand=True)
show_lesson_list()

root.mainloop()
