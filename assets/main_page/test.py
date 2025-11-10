from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.configure(bg="#f0f0f0")  # nền của widget

img = Image.open("./photos/bleu.png")  # ảnh PNG có alpha channel
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo, bg="#f0f0f0")  # màu nền trùng với widget
label.pack()
root.mainloop()
