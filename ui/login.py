import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk


ASSETS_ROOT = "../assets/"
BG = "#99CDFC"
# BG = "white"
# Setups
window = ttk.Window()
window.title("Login")
window.geometry("800x500")
window.resizable(False, False)

# Grid setup
window.rowconfigure(0, weight=1, uniform='a')
window.columnconfigure(0, weight=2, uniform='a')
window.columnconfigure(1, weight=1, uniform='a')
# Style setup
s = ttk.Style()
s.configure('TFrame', background=BG)


# Background Image
bg_img = Image.open(ASSETS_ROOT + 'bg/login_bg1.jpg').resize(size=(800,500))
bg_img_tk = ImageTk.PhotoImage(bg_img)
bg_label = ttk.Label(window, text="Background", image=bg_img_tk)
bg_label.place(x=0,y=0)

# Widgets
## left frame
left_frame = ttk.Frame(window)
left_frame.grid(row=0, column=0, sticky="")


## content frame
content_frame = ttk.Frame(window)
content_frame.place(relx=0.35, rely=0.5, anchor="center")

# Logo
logo_img = Image.open(ASSETS_ROOT + "/logo_blue.png").resize(size=(300,200))
logo_img_tk = ImageTk.PhotoImage(logo_img)
logo = ttk.Label(content_frame, text="main logo", image=logo_img_tk, background=BG)
logo.pack(side="top")

# Info frame
info_frame = ttk.Frame(content_frame)
info_frame.pack(side="top", expand=True)

## Username/pwd frame
### Username
username_pwd_frame = ttk.Frame(info_frame)
username_label = ttk.Label(username_pwd_frame, text="Tên đăng nhập:", background=BG)
username_entry = ttk.Entry(username_pwd_frame, bootstyle="primary")
username_entry.focus() # Tự động để pt vào khi login
username_pwd_frame.grid(row=1, column=0, sticky="wens", pady=10)
username_label.grid(row=0, column=0, sticky="we")
username_entry.grid(row=0, column=1, sticky="ew")

### Password
pwd_label = ttk.Label(username_pwd_frame, text="Mật khẩu:", background=BG)
pwd_entry = ttk.Entry(username_pwd_frame, bootstyle="primary")
pwd_label.grid(row=1, column=0, sticky="we")
pwd_entry.grid(row=1, column=1, sticky="we")

# Button frame
button_frame = ttk.Frame(info_frame)
login_btn = ttk.Button(button_frame, text="Đăng nhập", bootstyle="info")
sign_up = ttk.Button(button_frame, text="Đăng ký", bootstyle="success")
button_frame.grid(row=3, column=0, sticky="wens")
login_btn.pack(side="left", expand=True, fill="x", padx=(0,5))
sign_up.pack(side="left", expand=True, fill="x")

# Ads
ads1_img = Image.open(ASSETS_ROOT + "/ads/ads1.jpg").resize(size=(266,500))
ads1_img_tk = ImageTk.PhotoImage(ads1_img)
ads = ttk.Label(window, text="ads1", image= ads1_img_tk)
ads.grid(row=0, column=1, rowspan=4)

# Runs
window.mainloop()