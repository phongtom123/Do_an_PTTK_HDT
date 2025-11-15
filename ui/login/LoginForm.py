import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from logic.user.UserManager import UserManager


class LoginForm:
    def __init__(self, window):
        # Setup window
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0,0)
        self.window.update()

        self.username_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")

        self.base_dir = os.path.dirname(__file__)
        height = self.window.winfo_height()
        width = self.window.winfo_width()

        # ================= Background =================
        self.bg_frame = Image.open(self.base_dir + "/../..\\assets\\bg\\background1.png").resize((width, height))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = ttk.Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill="both", expand=True)

        # ================= Frame Đăng nhập =================
        self.lgn_frame = tk.Frame(self.window, bg="#040405", width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.lgn_frame,
            text="BLEU XIN CHÀO",
            font=("yu gothic ui", 25, "bold"),
            bg="#040405",
            fg="white"
        ).place(x=140, y=30)

        # ================= Hình bên trái =================
        left_img = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/vector.png"))
        tk.Label(self.lgn_frame, image=left_img, bg="#040405").place(x=5, y=100)
        self.lgn_frame.left_img = left_img  # tránh bị garbage collect

        # ================= Avatar đăng nhập =================
        avatar_img = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/login_avatar.png"))
        tk.Label(self.lgn_frame, image=avatar_img, bg="#040405").place(x=620, y=130)
        self.lgn_frame.avatar_img = avatar_img

        tk.Label(
            self.lgn_frame,
            text="Đăng nhập",
            bg="#040405",
            fg="white",
            font=("yu gothic ui", 17, "bold")
        ).place(x=637, y=240)

        # ================= Username =================
        tk.Label(self.lgn_frame, text="Username :", bg="#040405",
                 fg="#4f4e4d", font=("yu gothic ui", 13, "bold")).place(x=550, y=300)

        self.username_entry = tk.Entry(
            self.lgn_frame, bg="#040405", fg="#6b6a69",
            highlightthickness=0, relief=tk.FLAT,
            font=("yu gothic ui", 13, "bold"),
            textvariable=self.username_var
        )
        self.username_entry.place(x=580, y=330, width=270)

        tk.Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1",
                  highlightthickness=0).place(x=550, y=359)

        user_icon = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/icons/username_icon.png"))
        tk.Label(self.lgn_frame, image=user_icon, bg="#040405").place(x=550, y=332)
        self.lgn_frame.user_icon = user_icon

        # ================= Password =================
        tk.Label(self.lgn_frame, text="Password :", bg="#040405",
                 fg="#4f4e4d", font=("yu gothic ui", 13, "bold")).place(x=550, y=380)

        self.password_entry = tk.Entry(
            self.lgn_frame, bg="#040405", fg="#6b6a69",
            highlightthickness=0, relief=tk.FLAT,
            font=("yu gothic ui", 13, "bold"),
            show="*",
            textvariable=self.password_var
        )
        self.password_entry.place(x=580, y=412, width=270)

        tk.Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1",
                  highlightthickness=0).place(x=550, y=440)

        pass_icon = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/icons/password_icon.png"))
        tk.Label(self.lgn_frame, image=pass_icon, bg="#040405").place(x=550, y=410)
        self.lgn_frame.pass_icon = pass_icon

        # ================= Login Button =================
        btn_img = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/btn1.png"))
        btn_frame = tk.Label(self.lgn_frame, image=btn_img, bg="#040405")
        btn_frame.image = btn_img
        btn_frame.place(x=550, y=450)

        tk.Button(
            btn_frame, text="Đăng nhập", width=25,
            font=("yu gothic ui", 13, "bold"),
            bd=0, bg="#3047ff", fg="white",
            cursor="hand2", activebackground="#3047ff",
            command=self.authentic
        ).place(x=20, y=10)

        # ================= Quên mật khẩu =================
        tk.Button(
            self.lgn_frame, text="Quên mật khẩu?",
            font=("yu gothic ui", 13, "bold underline"),
            fg="white", bg="#040405", bd=0,
            cursor="hand2"
        ).place(x=575, y=510)

        # ================= Đăng ký =================
        tk.Label(
            self.lgn_frame,
            text="Let learn English!",
            font=("yu gothic ui", 11, "italic"),
            background="#040405",
            fg="white",
        ).place(x=550, y=553)

        reg_img = ImageTk.PhotoImage(Image.open(self.base_dir + "/../../assets/register.png"))
        lbl_reg = tk.Label(self.lgn_frame, image=reg_img, bg="#040405", cursor="hand2")
        lbl_reg.image = reg_img
        lbl_reg.place(x=670, y=550, width=111, height=35)
        lbl_reg.bind('<Button-1>', self.go_to_signup)

        # ================= Show Password =================
        self.show_image = ImageTk.PhotoImage(file=self.base_dir + '/../../assets/icons/show.png')
        self.hide_image = ImageTk.PhotoImage(file=self.base_dir + '/../../assets/icons/show.png')

        self.show_button = tk.Button(self.lgn_frame, image=self.show_image,
                                     command=self.show, relief=tk.FLAT,
                                     borderwidth=0, cursor="hand2")
        self.show_button.place(x=860, y=420)


    # =====================================================
    # SHOW / HIDE PASSWORD
    # =====================================================
    def show(self):
        self.password_entry.config(show='')
        btn = tk.Button(self.lgn_frame, image=self.hide_image,
                        command=self.hide, relief=tk.FLAT, borderwidth=0,
                        cursor="hand2")
        btn.place(x=860, y=420)

    def hide(self):
        self.password_entry.config(show='*')
        btn = tk.Button(self.lgn_frame, image=self.show_image,
                        command=self.show, relief=tk.FLAT, borderwidth=0,
                        cursor="hand2")
        btn.place(x=860, y=420)


    # =====================================================
    # LOGIN LOGIC — HOÀN CHỈNH
    # =====================================================
    def authentic(self):
        username = self.username_var.get()
        pwd = self.password_var.get()

        user_mgr = UserManager()

        if username == "" or pwd == "":
            messagebox.showinfo("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        user = user_mgr.auth(username, pwd)

        if user is False:
            messagebox.showinfo("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
            return

        print("🎉 Đăng nhập thành công:", user)

        # → Qua trang HomePage + truyền user
        self.window.destroy()
        from ui.home_page.HomePage import HomePage
        home = HomePage(user)
        home.mainloop()


    # =====================================================
    def go_to_signup(self, event=None):
        self.window.destroy()
        from ui.signup.SignupForm import SignupForm
        root = tk.Tk()
        SignupForm(root)
        root.mainloop()


def page():
    window = tk.Tk()
    LoginForm(window)
    window.mainloop()


if __name__ == "__main__":
    page()
