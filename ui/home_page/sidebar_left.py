# ui/home_page/sidebar_left.py

import tkinter as tk
from PIL import Image, ImageTk
import os, sys

# Thêm đường dẫn cha để import controller & utils
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from logic.unit_controller import get_all_units
from utils.make_button import make_button

current_path = os.path.dirname(__file__)

class SidebarLeft(tk.Frame):
    """Sidebar bên trái của giao diện chính"""
    def __init__(self, root, show_in_main):
        super().__init__(
            root, 
            bg="#FFFFFF", 
            width=200, 
            highlightbackground="#e0e0e0", 
            highlightthickness=1)
        self.root = root
        self.show_in_main = show_in_main

        # Trạng thái
        self._collapsed = False
        self._courses_open = False
        self._practice_open = False
        self._account_open = False

        # Container chính
        self.container = tk.Frame(root, bg="#FFFFFF")
        self.container.pack(side="left", fill="y")

        self.sidebar_frame = self
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Toggle frame
        self.toggle_frame = tk.Frame(self.container, bg="#FFFFFF", width=15)
        self.toggle_frame.pack(side="left", fill="y")

        self.toggle_icon = tk.Label(
            self.toggle_frame, 
            text="<", 
            font=("Arial", 12, "bold"), 
            bg="#FFFFFF", 
            cursor="hand2"
        )
        self.toggle_icon.pack(padx=5, pady=10)
        self.toggle_icon.bind("<Button-1>", self._toggle_sidebar)

        # Tải icon
        self.icons = {}
        self._load_icons()

        # Tạo giao diện
        self._create_logo()
        self._create_sections()

    
    def _load_icons(self) -> dict:
        '''Load 1 loạt icon. Trả về 1 dict chứa tên và đối tượng ImageTk'''
        def load(name, path, size):
            try:
                img = Image.open(path).resize(size)
                self.icons[name] = ImageTk.PhotoImage(img)
            except Exception:
                self.icons[name] = None
        load("logo",  current_path + "/../../assets/logo_blue.png", (150, 160))
        load("learn", current_path + "/../../assets/main_page/Home.png", (35, 35))
        load("game", current_path + "/../../assets/main_page/game_icon.png", (25,30))
        load("practice", current_path + "/../../assets/main_page/Practice.png", (35, 35))
        load("profile", current_path + "/../../assets/main_page/avataaars.png", (35, 35))
        load("more", current_path + "/../../assets/main_page/More.png", (35, 35))
        load("ranking", current_path + "/../../assets/main_page/ranking.png", (35, 35))
        load("vocab", current_path + "/../../assets/main_page/vocab.png", (25, 25))
        load("logout", current_path + "/../../assets/main_page/logout.png", (25, 25))
        load("profile1", current_path + "/../../assets/main_page/profile.png", (25, 25))
        load("book", current_path + "/../../assets/main_page/book.png", (25, 25))
        load("earphone", current_path + "/../../assets/main_page/earphone.png", (20, 20))

    
    def _create_logo(self):
        '''Tạo logo trong sidebar'''
        logo_frame = tk.Frame(self.sidebar_frame, bg="#FFFFFF", height=120)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        def go_home():
            self.show_in_main("__BACK__", [])

        try:
            btn_logo = tk.Button(
                logo_frame, image=self.icons["logo"], bg="#FFFFFF", bd=0,
                activebackground="#FFFFFF", command=go_home
            )
            btn_logo.pack(pady=20)
        except Exception:
            tk.Button(
                logo_frame, text="My Logo", font=("Arial", 16, "bold"),
                fg="black", bg="#FFFFFF", bd=0, activebackground="#FFFFFF",
                command=go_home
            ).pack(pady=20)

    # -------------------------------------------------------
    # SECTIONS
    # -------------------------------------------------------
    def _create_sections(self):
        # Mục Học
        self.btn_courses = make_button(self.sidebar_frame, "Học", self.icons["learn"])
        self.btn_courses.pack(fill="x", pady=5)
        
        # # ==== start game ====
        # self.btn_game = make_button(self.sidebar_frame, "Chơi trò chơi", self.icons["game"])
        # self.btn_game.pack(fill="y", pady=5)

        self.btn_vocab = make_button(
            self.sidebar_frame, "Từ vựng", self.icons["vocab"],
            cmd=lambda: self.show_in_main("Từ vựng", ["Từ mới hôm nay", "Ôn tập tuần"]),
            padx=40
        )
        self.courses_sub = [self.btn_vocab]
        self.btn_courses.config(command=self._toggle_courses)

        # Mục Luyện tập
        self.btn_practice = make_button(self.sidebar_frame, "Luyện tập", self.icons["practice"])
        self.btn_practice.pack(fill="x", pady=5)

        self.btn_reading = make_button(
            self.sidebar_frame, "Reading", self.icons["book"],
            cmd=lambda: self.show_in_main("Reading", get_all_units()), padx=40
        )
        self.btn_listening = make_button(
            self.sidebar_frame, "Listening", self.icons["earphone"],
            cmd=lambda: self.show_in_main("Listening", get_all_units()), padx=40
        )
        self.practice_sub = [self.btn_reading, self.btn_listening]
        self.btn_practice.config(command=self._toggle_practice)

        # Mục khác
        self.btn_rank = make_button(
            self.sidebar_frame, "Xếp hạng", self.icons["ranking"],
            lambda: self.show_in_main("Xếp hạng", ["Top 1: Nam", "Top 2: Linh"])
        )
        self.btn_rank.pack(fill="x", pady=5)

        self.btn_more = make_button(
            self.sidebar_frame, "Xem thêm", self.icons["more"],
            lambda: self.show_in_main("Xem thêm", ["Profile", "Security"])
        )
        self.btn_more.pack(fill="x", pady=5)

        # Account
        self.btn_account = make_button(self.sidebar_frame, "Tài khoản", self.icons["profile"])
        self.btn_account.pack(fill="x", pady=5)

        self.btn_profile = make_button(
            self.sidebar_frame, "Hồ sơ", self.icons["profile1"],
            cmd=lambda: self.show_in_main("Hồ sơ", ["Thông tin cá nhân"]), padx=40
        )
        self.btn_logout = make_button(
            self.sidebar_frame, "Đăng xuất", self.icons["logout"],
            cmd=self.root.quit, padx=40
        )

        self.account_sub = [self.btn_profile, self.btn_logout]
        self.btn_account.config(command=self._toggle_account)

    # -------------------------------------------------------
    # TOGGLE CÁC PHẦN CON
    # -------------------------------------------------------
    def _toggle_courses(self):
        if self._courses_open:
            for b in self.courses_sub:
                b.pack_forget()
        else:
            for b in self.courses_sub:
                b.pack(fill="x", pady=2, after=self.btn_courses)
        self._courses_open = not self._courses_open

    def _toggle_practice(self):
        if self._practice_open:
            for b in self.practice_sub:
                b.pack_forget()
        else:
            for b in self.practice_sub:
                b.pack(fill="x", pady=2, after=self.btn_practice)
        self._practice_open = not self._practice_open

    def _toggle_account(self):
        if self._account_open:
            for b in self.account_sub:
                b.pack_forget()
        else:
            for b in self.account_sub:
                b.pack(fill="x", pady=2, after=self.btn_account)
        self._account_open = not self._account_open

    # -------------------------------------------------------
    # THU GỌN / MỞ SIDEBAR
    # -------------------------------------------------------
    def _toggle_sidebar(self, event=None):
        if not self._collapsed:
            for widget in self.sidebar_frame.winfo_children():
                widget.pack_forget()
            self.sidebar_frame.config(width=10, highlightthickness=0)
            self.toggle_icon.config(text=">")
            self._collapsed = True
        else:
            self.sidebar_frame.config(width=200, highlightthickness=1, highlightbackground="#e0e0e0")
            self._repack_widgets()
            self.toggle_icon.config(text="<")
            self._collapsed = False

    def _repack_widgets(self):
        """Phục hồi lại các phần khi mở sidebar"""
        # logo + mục học
        self._create_logo()
        self.btn_courses.pack(fill="x", pady=5)
        if self._courses_open:
            for b in self.courses_sub:
                b.pack(fill="x", pady=2, after=self.btn_courses)

        self.btn_practice.pack(fill="x", pady=5)
        if self._practice_open:
            for b in self.practice_sub:
                b.pack(fill="x", pady=2, after=self.btn_practice)

        self.btn_rank.pack(fill="x", pady=5)
        self.btn_more.pack(fill="x", pady=5)
        self.btn_account.pack(fill="x", pady=5)
        if self._account_open:
            for b in self.account_sub:
                b.pack(fill="x", pady=2, after=self.btn_account)
