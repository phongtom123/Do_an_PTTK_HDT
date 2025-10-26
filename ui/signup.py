import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk


ASSETS_ROOT = "../assets/"
BG = "#99CDFC"

# Setup
window = ttk.Window()
window.title("Sign up")
window.geometry("800x500")
window.resizable(False, False)

# Style setup
s = ttk.Style()
s.configure('TFrame', background=BG)

# Background image
bg_img = Image.open(ASSETS_ROOT + 'bg/login_bg1.jpg').resize(size=(800,500))
bg_img_tk = ImageTk.PhotoImage(bg_img)
bg_label = ttk.Label(window, text="Background", image=bg_img_tk)
bg_label.place(x=0,y=0)

# Logo
logo_img = Image.open(ASSETS_ROOT + "/logo_blue.png").resize(size=(300,200))
logo_img_tk = ImageTk.PhotoImage(logo_img)
logo = ttk.Label(window, text="main logo", image=logo_img_tk, background=BG)


# Widgets
widget_frame =  ttk.Frame(window)

email = ttk.Label(widget_frame,
                  text="Email: ",
                  background=BG,
                  font=('Segoe UI',9,"bold"))
email_entry = ttk.Entry(widget_frame)

username = ttk.Label(widget_frame,
                     text="Tên đăng nhập: ",
                     background=BG,
                     font=('Segoe UI',9,"bold"))
username_entry = ttk.Entry(widget_frame)

pwd = ttk.Label(widget_frame,
                text="Mật khẩu: ",
                background=BG,
                font=('Segoe UI',9,"bold"))
pwd_entry = ttk.Entry(widget_frame)

# Dùng để báo khi gmail đã có rồi
email_check_label = ttk.Label(widget_frame,
                              text="Email đã tồn tại",
                              background=BG,
                              bootstyle="danger",
                              font=('Segoe UI',12,"bold"))

back_btn = ttk.Button(widget_frame, text="Quay lại", bootstyle="secondary")
signup_btn = ttk.Button(widget_frame, text="Đăng ký", bootstyle="info")

# Layouts

logo.pack(side="top", padx=(10,0))
widget_frame.pack(side="top")
## Grid setup
widget_frame.rowconfigure((0,1,2,3,4), weight=1, uniform='a')
widget_frame.columnconfigure((0,1), weight=1, uniform='a')

email.grid(row=0, column=0)
email_entry.grid(row=0, column=1)

username.grid(row=1, column=0)
username_entry.grid(row=1, column=1)

pwd.grid(row=2, column=0)
pwd_entry.grid(row=2, column=1)

email_check_label.grid(row=3, column=0, columnspan=2, sticky="e")

back_btn.grid(row=4, column=0)
signup_btn.grid(row=4, column=1)

# Run
window.mainloop()