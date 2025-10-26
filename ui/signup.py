import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

ASSETS_ROOT = "../assets/"

# Setup
window = ttk.Window()
window.title("Sign up")
window.geometry("800x500")

# Background image
bg_img = Image.open(ASSETS_ROOT + 'bg/login_bg1.jpg').resize(size=(800,500))
bg_img_tk = ImageTk.PhotoImage(bg_img)
bg_label = ttk.Label(window, text="Background", image=bg_img_tk)
bg_label.place(x=0,y=0)


# Run
window.mainloop()