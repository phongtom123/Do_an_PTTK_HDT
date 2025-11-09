import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from logic.auth import SigninManager
import os, messagebox, re

class SignupForm:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed") # Dam bao windoww phong ta ra
        self.window.resizable(0,0) # Tat resize
        self.window.update()

        self.username_var = tk.StringVar(value="123")
        self.password_var = tk.StringVar(value="123")
        self.email_var = tk.StringVar(value="123")
        self.re_enter_pwd_var = tk.StringVar(value="123")
        height = self.window.winfo_height()
        width = self.window.winfo_width()

        # =================Start background image=============
        self.bg_frame = Image.open(os.path.dirname(__file__) + "/../assets/bg/background1.png").resize((width, height))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = ttk.Label(self.window, image=photo)
        self.bg_panel.image = photo #?
        self.bg_panel.pack(fill="both", expand=True)
        # =================End background image===============

        # =================Start login frame==================
        self.lgn_frame = tk.Frame(self.window, bg="#040405", width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.txt = 'BLER XIN CHÀO!'
        self.heading = tk.Label(
            self.lgn_frame,
            text=self.txt,
            font=("yu gothic ui", 25, "bold"),
            bg="#040405",
            fg="white")
        self.heading.place(x=140, y=30, anchor= 'nw')
        # =================End login frame====================

        # =================Start left side image==============
        self.side_image = Image.open(os.path.dirname(__file__) + "/../assets/vector.png")
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image = tk.Label(self.lgn_frame, image=photo, bg= "#040405")
        self.side_image.image = photo  # ?
        self.side_image.place(x=5, y=100)
        # =================End left side image================

        # =================Start sign in,label======================
        self.sign_in_label = tk.Label(
            self.lgn_frame,
            text="Đăng ký nha",
            bg="#040405",
            fg="white",
            font=("yu gothic ui", 17, "bold")
        )
        self.sign_in_label.place(x=640, y=90)
        # =================End sign in image,label======================

        # =================Start email===============================
        self.email_label = tk.Label(
            self.lgn_frame,
                text="Email:",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.email_label.place(x=550, y=130)

        self.email_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT, # Tạo viền 3 chiều ( ảo giác sâu)
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 13, "bold"),
            textvariable= self.email_var
        )
        self.email_entry.place(x=580, y=160, width=270)

        self.email_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.email_line.place(x=550, y=190)
        # =================End email===================================

        # ==================Start email icon=============
        self.email_icon = Image.open(os.path.dirname(__file__) + "/../assets/icons/email_icon.png")
        photo = ImageTk.PhotoImage(self.email_icon)
        self.email_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.email_icon.image = photo  # ?
        self.email_icon.place(x=550, y=160)
        # ==================End email icon===============

        # =================Start username===============================
        self.username_label = tk.Label(
            self.lgn_frame,
            text="Tên đăng nhập:",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.username_label.place(x=550, y=210)

        self.username_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT, # Tạo viền 3 chiều ( ảo giác sâu)
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 13, "bold"),
            textvariable= self.username_var
        )
        self.username_entry.place(x=580, y=240, width=270)

        self.username_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.username_line.place(x=550, y=270)
        # ==================End username====================

        # ==================Start username icon=============
        self.username_icon = Image.open(os.path.dirname(__file__) + "/../assets/icons/username_icon.png")
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.username_icon.image = photo  # ?
        self.username_icon.place(x=550, y=240)
        # ==================End username icon===============

        # =================Start password===============================
        self.password_label = tk.Label(
            self.lgn_frame,
            text="Mật khẩu:",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.password_label.place(x=550, y=285)

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
        self.password_entry.place(x=580, y=315, width=270)

        self.password_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.password_line.place(x=550, y=340)
        # ==================End password====================

        # ==================Start password icon=============
        self.password_icon = Image.open(os.path.dirname(__file__) + "/../assets/icons/password_icon.png")
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.password_icon.image = photo  # ?
        self.password_icon.place(x=550, y=310)
        # ==================End password icon===============

        # ==================Start re-enter pwd==============
        self.re_enter_password_label = tk.Label(
            self.lgn_frame,
            text="Nhập lại mật khẩu :",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.re_enter_password_label.place(x=550, y=370)

        self.re_enter_password_entry = tk.Entry(
            self.lgn_frame,
            highlightthickness=0,
            relief=tk.FLAT, # Tạo viền 3 chiều ( ảo giác sâu)
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 13, "bold"),
            show="*",
            textvariable= self.re_enter_pwd_var
        )
        self.re_enter_password_entry.place(x=580, y=405, width=400)

        self.re_enter_password_line = tk.Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.re_enter_password_line.place(x=550, y=430)
        # ==================End re-enter pwd===============

        # ==================Start re_enter_pwd icon=============
        self.re_enter_pwd_icon = Image.open(os.path.dirname(__file__) + "/../assets/icons/re_enter_pwd_icon.png")
        photo = ImageTk.PhotoImage(self.re_enter_pwd_icon)
        self.re_enter_pwd_icon = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.re_enter_pwd_icon.image = photo  # ?
        self.re_enter_pwd_icon.place(x=550, y=400)
        # ==================End re_enter_pwd icon===============

        # ==================Start signup button==============
        self.sgnup_button = tk.Button(self.lgn_frame)
        self.sgnup_button_label = Image.open(os.path.dirname(__file__) + "/../assets/btn1.png") # Dùng image để tạo nút tròn ảo
        photo = ImageTk.PhotoImage(self.sgnup_button_label)
        self.sgnup_button_label = tk.Label(self.lgn_frame, image=photo, bg="#040405")
        self.sgnup_button_label.image = photo  # ?
        self.sgnup_button_label.place(x=550, y=450)

        self.signup = tk.Button(
            self.sgnup_button_label,
            text="Đăng ký",
            font=("yu gothic ui", 13, "bold"),
            width=25,
            bd=0,
            bg="#3047ff",
            cursor="hand2", # Tạo cursor cái tay
            activebackground="#3047ff", # Tạo hoạt ảnh khi ấn
            fg="white",
            command = self.signup
        )
        self.signup.place(x=20, y=10)
    # ======================End Signup button===================

    # ======================Start forgot password==============
        self.forgot_button = tk.Button(
            self.lgn_frame,
            text="Forgot Password ?",
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

        self.sign_up_label = Image.open(os.path.dirname(__file__) + "/../assets/register.png")
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


        # ================Show/hide password============
        self.show_image = Image.open(os.path.dirname(__file__) + "/../assets/icons/show.png")
        photo = ImageTk.PhotoImage(self.show_image)
        self.show_button = tk.Label(
            self.lgn_frame,
            image=photo,
            bg="#040405",
            activebackground="#040405",
            cursor="hand2",
            bd=0
        )
        self.show_button_image = photo
        self.show_button.place(x=860, y=420)

    
    def get_infor(self):
        '''Lấy 4 giá trị từ form, trả về 1 tuple'''
        email = self.email_var.get()
        username = self.username_var.get()
        pwd = self.password_var.get()
        re_enter_pwd = self.re_enter_pwd_var.get()
        return (email, username, pwd, re_enter_pwd)

    def signup(self):
        '''Cập nhật thông tin vào database'''
        email, username, pwd, re_enter_pwd = self.get_infor()
        
        # setup
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        # TH khoảng bị bỏ trống
        if '' in (email, username, pwd, re_enter_pwd):
            messagebox.showinfo("Hỏng", "Vui lòng điền đầy đủ thông tin để tạo tài khoản.")
        # TH không đúng định dạng chuỗi
        elif re.match(email_pattern, email) == False:
            messagebox.showinfo("Hỏng", "Vui lòng điền đầy đủ thông tin để tạo tài khoản.")
        # TH pwd khác re_enter_pwd
        elif pwd != re_enter_pwd:
            messagebox.showinfo("Hỏng", "Mật khẩu nhập lại không trùng khớp.")
            self.re_enter_pwd_var.set('')
        # TH phải query
        else:
            sgnup_mnr = SigninManager()
            is_existed = sgnup_mnr.check_if_exists(
                email= email,
                username= username,
                pwd= pwd
            )

            if is_existed == 1:
                messagebox.showinfo("Hỏng", "Email đã tồn tại.")
            elif is_existed == 2:
                messagebox.showinfo("Hỏng", "Tên đăng nhập đã tồn tại, vui lòng trọn tên đăng nhập khác.")
            else:
                is_success = sgnup_mnr.add_user(
                    username= username,
                    pwd= pwd,
                    email= email
                )
                if is_success:
                    messagebox.showinfo("Chào mừng", "Bạn đã tạo tài khoản thành công, vui lòng đăng nhập.")
                else:
                    messagebox.showinfo("Hỏng", "Chương trình đang có quá nhiều người dùng, vui lòng thử lại sau.")

def page():
    window = tk.Tk()
    SignupForm(window)
    window.mainloop()

if __name__ == "__main__":
    page()