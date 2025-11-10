import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from logic.auth import LoginManager
import os

class LoginForm:
    def __init__(self, window):
        # Setup
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed") # Dam bao windoww phong ta ra
        self.window.resizable(0,0) # Tat resize
        self.window.update()

        self.username_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")
        self.base_dir = os.path.dirname(__file__)

        height = self.window.winfo_height()
        width = self.window.winfo_width()

        # =================Start background image=============
        self.bg_frame = Image.open(self.base_dir + "/..\\assets\\bg\\background1.png").resize((width, height))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = ttk.Label(self.window, image=photo)
        self.bg_panel.image = photo #?
        self.bg_panel.pack(fill="both", expand=True)
        # =================End background image===============

        # =================Start login frame==================
        self.lgn_frame = tk.Frame(self.window, bg="#040405", width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.txt = 'BLER XIN CHÀO'
        self.heading = tk.Label(
            self.lgn_frame,
            text=self.txt,
            font=("yu gothic ui", 25, "bold"),
            bg="#040405",
            fg="white")
        self.heading.place(x=140, y=30, anchor= 'nw')
        # =================End login frame====================

        # =================Start left side image==============
        self.side_image = Image.open(self.base_dir + "/../assets/vector.png")
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image = tk.Label(self.lgn_frame, image=photo, bg= "#040405")
        self.side_image.image = photo  # ?
        self.side_image.place(x=5, y=100)
        # =================End left side image================

        # =================Start sign in image,label======================
        self.sign_in_image = Image.open(self.base_dir + "/../assets/login_avatar.png")
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.sign_in_image.image = photo  # ?
        self.sign_in_image.place(x=620, y=130)

        self.sign_in_label = tk.Label(
            self.lgn_frame,
            text="Đăng nhập",
            bg="#040405",
            fg="white",
            font=("yu gothic ui", 17, "bold")
        )
        self.sign_in_label.place(x=637, y=240)
        # =================End sign in image,label======================

        # =================Start username===============================
        self.username_label = tk.Label(
            self.lgn_frame,
            text="Username :",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.username_label.place(x=550, y=300)

        self.username_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT, # Tạo viền 3 chiều ( ảo giác sâu)
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 13, "bold"),
            textvariable= self.username_var
        )
        self.username_entry.place(x=580, y=330, width=270)

        self.username_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.username_line.place(x=550, y=359)
        # ==================End username====================

        # ==================Start username icon=============
        self.username_icon = Image.open(self.base_dir + "/../assets/icons/username_icon.png")
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.username_icon.image = photo  # ?
        self.username_icon.place(x=550, y=332)
        # ==================End username icon===============

        # =================Start password===============================
        self.password_label = tk.Label(
            self.lgn_frame,
            text="Password :",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.password_label.place(x=550, y=380)

        self.password_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT, # Tạo viền 3 chiều ( ảo giác sâu)
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 13, "bold"),
            show="*",
            textvariable= self.password_var
        )
        self.password_entry.place(x=580, y=412, width=270)

        self.password_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.password_line.place(x=550, y=440)
        # ==================End password====================

        # ==================Start password icon=============
        self.password_icon = Image.open(self.base_dir + "/../assets/icons/password_icon.png")
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.password_icon.image = photo  # ?
        self.password_icon.place(x=550, y=410)
        # ==================End password icon===============

        # ==================Start login button==============
        self.lgn_button = tk.Button(self.lgn_frame)
        self.lgn_button_label = Image.open(self.base_dir + "/../assets/btn1.png") # Dùng image để tạo nút tròn ảo
        photo = ImageTk.PhotoImage(self.lgn_button_label)
        self.lgn_button_label = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.lgn_button_label.image = photo  # ?
        self.lgn_button_label.place(x=550, y=450)

        self.login = tk.Button(
            self.lgn_button_label,
            text="Đăng nhập",
            font=("yu gothic ui", 13, "bold"),
            width=25,
            bd=0,
            bg="#3047ff",
            cursor="hand2", # Tạo cursor cái tay
            activebackground="#3047ff", # Tạo hoạt ảnh khi ấn
            fg="white",
            command=self.authentic
        )
        self.login.place(x=20, y=10)
    # ======================End login button===================

    # ======================Start forgot password==============
        self.forgot_button = tk.Button(
            self.lgn_frame,
            text="Quên mật khẩu?",
            font=("yu gothic ui", 13, "bold underline"),
            fg = "white",
            width=25,
            bd=0,
            bg = "#040405",
            activebackground= "#040405",
            cursor="hand2"
        )
        self.forgot_button.place(x=575, y=510)
    # ======================End forgot password================


    # ======================Start sign up============================
        self.sign_label = tk.Label(
            self.lgn_frame,
            text="Let learn English!",
            font=("yu gothic ui", 11, "italic"),
            background="#040405",
            fg="white",
        )
        self.sign_label.place(x=550, y=553)

        self.sign_up_label = Image.open(self.base_dir + "/../assets/register.png")
        photo = ImageTk.PhotoImage(self.sign_up_label)
        self.sign_up_label = tk.Label(
            self.lgn_frame,
            image=photo,
            bg="#040405",
            activebackground="#040405",
            cursor="hand2",
            bd=0
        )

        self.sign_up_label.image = photo  # ?
        self.sign_up_label.place(x=670, y=550, width=111, height=35)
        # event
        self.sign_up_label.bind('<Button-1>', self.go_to_signup)

        # ================Show/hide password============
        self.show_image = ImageTk.PhotoImage \
            (file=self.base_dir + '/../assets/icons/show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file=self.base_dir + '/../assets/icons/show.png')

        self.show_button = tk.Button(self.lgn_frame, image=self.show_image, command=self.show, relief=tk.FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = tk.Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=tk.FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = tk.Button(self.lgn_frame, image=self.show_image, command=self.show, relief=tk.FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')


        
    def authentic(self):
            username = self.username_var.get()
            pwd = self.password_var.get()
            print(f"Username: {username}")
            print(f"Password: {pwd}")
            login_mnr = LoginManager()
            if login_mnr.auth(username= username, password= pwd):
                print("Đăng nhập thành công")
            else:
                print("Đăng nhập không thành công.")
            
    def go_to_signup(self, event=None):
        '''Hàm redirect qua form Signup'''
        self.window.destroy()
        from ui.SignupForm import SignupForm
        new_window = tk.Tk()
        SignupForm(new_window)
        new_window.mainloop()

def page():
    window = tk.Tk()
    LoginForm(window)
    window.mainloop()

if __name__ == "__main__":
    page()