# main_content.py
import tkinter as tk
from tkinter import messagebox

def create_main_frame(root):
    """
    Tạo frame cho vùng chính - KHÔNG pack ở đây để main.py quyết định thứ tự pack.
    """
    frame = tk.Frame(root, bg="white")
    return frame

def show_message(msg):
    messagebox.showinfo("Menu", f"Bạn chọn: {msg}")
