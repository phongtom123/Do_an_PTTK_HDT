import tkinter as tk

root = tk.Tk()
root.title("Image Button Demo")

# Load ảnh (hỗ trợ PNG, GIF bằng PhotoImage)
img = tk.PhotoImage(file="./photos/avataaars.png")  # đổi thành đường dẫn file ảnh của bạn

def on_click():
    print("Ảnh được click!")

btn_img = tk.Button(root, image=img, command=on_click, bd=0, cursor="hand2")
btn_img.pack(pady=20)

root.mainloop()
