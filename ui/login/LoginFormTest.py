import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from logic.user.UserManager import UserManager
from ui.test.TestAfterLogin import TestAfterLogin


class LoginFormTest:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0, 0)

        self.username_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")

        self.base_dir = os.path.dirname(__file__)
        height = self.window.winfo_height()
        width = self.window.winfo_width()

        # =================Background=================
        bg = Image.open(self.base_dir + "/../..\\assets\\bg\\background1.png").resize((width, height))
        bg_photo = ImageTk.PhotoImage(bg)

        self.bg_panel = ttk.Label(self.window, image=bg_photo)
        self.bg_panel.image = bg_photo
        self.bg_panel.pack(fill="both", expand=True)

        # =================Frame login=================
        self.lgn_frame = tk.Frame(self.window, bg="#040405", width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.lgn_frame, text="BLEU XIN CHÀO",
                 font=("yu gothic ui", 25, "bold"),
                 bg="#040405", fg="white").place(x=140, y=30)

        # =================Username=================
        tk.Label(self.lgn_frame, text="Username:", bg="#040405",
                 fg="#4f4e4d", font=("yu gothic ui", 13, "bold")).place(x=550, y=300)

        self.username_entry = tk.Entry(
            self.lgn_frame,
            bg="#040405",
            fg="#6b6a69",
            relief=tk.FLAT,
            highlightthickness=0,
            font=("yu gothic ui", 13, "bold"),
            textvariable=self.username_var
        )
        self.username_entry.place(x=580, y=330, width=270)

        tk.Canvas(self.lgn_frame, width=300, height=2,
                  bg="#bdb9b1", highlightthickness=0).place(x=550, y=359)

        # =================Password=================
        tk.Label(self.lgn_frame, text="Password:", bg="#040405",
                 fg="#4f4e4d", font=("yu gothic ui", 13, "bold")).place(x=550, y=380)

        self.password_entry = tk.Entry(
            self.lgn_frame,
            bg="#040405",
            fg="#6b6a69",
            relief=tk.FLAT,
            highlightthickness=0,
            show="*",
            font=("yu gothic ui", 13, "bold"),
            textvariable=self.password_var
        )
        self.password_entry.place(x=580, y=412, width=270)

        tk.Canvas(self.lgn_frame, width=300, height=2,
                  bg="#bdb9b1", highlightthickness=0).place(x=550, y=440)

        # =================Login Button=================
        btn_img = Image.open(self.base_dir + "/../../assets/btn1.png")
        btn_photo = ImageTk.PhotoImage(btn_img)

        btn_frame = tk.Label(self.lgn_frame, image=btn_photo, bg="#040405")
        btn_frame.image = btn_photo
        btn_frame.place(x=550, y=450)

        tk.Button(
            btn_frame,
            text="Đăng nhập",
            font=("yu gothic ui", 13, "bold"),
            width=25,
            bd=0,
            bg="#3047ff",
            fg="white",
            cursor="hand2",
            activebackground="#3047ff",
            command=self.authentic
        ).place(x=20, y=10)

    # =================================================
    def authentic(self):
        username = self.username_var.get()
        pwd = self.password_var.get()

        um = UserManager()

        if not username or not pwd:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        user = um.auth(username, pwd)

        if not user:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")
            return

        print("🎉 LOGIN OK:", user)

        # >>>>>>>>>> MỞ TRANG TEST <<<<<<<<<<
        self.window.destroy()
        test = TestAfterLogin(user)
        test.mainloop()


# =================================================
def page():
    root = tk.Tk()
    LoginFormTest(root)
    root.mainloop()


if __name__ == "__main__":
    page()
