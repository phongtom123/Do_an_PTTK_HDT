import tkinter as tk
import os
from PIL import Image, ImageTk
from utils.make_button import make_button

class SidebarLeft(tk.Frame):
    """Thanh sidebar bên trái có logo, menu con, và toggle"""

    def __init__(self, root, main_content, current_user):
        super().__init__(
            root,
            bg="#FFFFFF",
            width=200,
            highlightbackground="#e0e0e0",
            highlightthickness=1
        )
        self.root = root
        self.main_content = main_content
        self.current_user = current_user
        self.icons = {}
        self._collapsed = False
        self._courses_sub = []
        self._account_sub = []
        self.active_button = None

        self._load_icons()
        self._build_ui()

    # ======================================
    # LOAD ICONS
    # ======================================
    def _load_icons(self):
        """Nạp tất cả icon từ thư mục assets/main_page"""
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/main_page"))

        def load(name, filename, size):
            try:
                path = os.path.join(base_path, filename)
                img = Image.open(path).resize(size)
                self.icons[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"⚠️ Không thể tải {filename}: {e}")
                self.icons[name] = None

        load("learn", "Vocab.png", (35, 35))
        # load("practice", "Practice.png", (35, 35))
        load("game", "game_icon.png", (45, 35))
        load("fc", "fc_icon.png", (45, 35))
        load("profile", "avataaars.png", (35, 35))
        load("more", "More.png", (35, 35))
        load("ranking", "ranking.png", (35, 35))
        load("vocab", "fire.png", (25, 25))
        load("logout", "logout.png", (25, 25))
        load("profile1", "profile.png", (25, 25))
        load("book", "book.png", (25, 25))
        load("logo", "2.png", (150, 130))

    # ======================================
    # BUILD SIDEBAR UI
    # ======================================
    def _build_ui(self):
        """Tạo giao diện sidebar"""
        for w in self.winfo_children():
            w.destroy()

        # === Sidebar luôn ở bên trái ===
        self.pack(side="left", fill="y")
        self.pack_propagate(False)

        # === Toggle (nút < >) nằm bên phải sidebar ===
        self._toggle_frame = tk.Frame(self.master, bg="#FFFFFF", width=15)
        self._toggle_frame.pack(side="left", fill="y", before=self)
        self._toggle_icon = tk.Label(
            self._toggle_frame, text="❮",
            font=("Arial", 12, "bold"),
            bg="#FFFFFF", cursor="hand2"
        )
        self._toggle_icon.pack(padx=5, pady=10)
        self._toggle_icon.bind("<Button-1>", self._toggle_sidebar)

        # === Logo ===
        logo_frame = tk.Frame(self, bg="#FFFFFF", height=120)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        if self.icons.get("logo"):
            logo_label = tk.Label(logo_frame, image=self.icons["logo"], bg="#FFFFFF", cursor="hand2")
            logo_label.pack(pady=(15, 0))
            tk.Label(logo_frame, text="bleu", fg="#1da9fe", bg="#FFFFFF",
                     font=("Arial", 18, "bold")).pack()
            logo_label.bind("<Button-1>", lambda e: self._go_home())
        else:
            tk.Button(logo_frame, text="bleu", font=("Arial", 18, "bold"),
                      fg="#1da9fe", bg="#FFFFFF", bd=0,
                      command=self._go_home).pack(pady=20)

        # === Mục HỌC ===
        btn_courses = make_button(self, "Học", self.icons["learn"])
        btn_courses.pack(fill="x", pady=5)

        # 🟦 Submenu: Bài học
        self.btn_lesson = make_button(
            self, "Bài học", self.icons["book"],
            cmd=lambda: self._highlight_and_open(self.btn_lesson, "__BACK__", []),
            padx=40
        )

        # 🟩 Submenu: Từ vựng
        self.btn_vocab = make_button(
            self, "Từ vựng", self.icons["vocab"],
            cmd=lambda: self._highlight_and_open(self.btn_vocab, "Từ vựng", []),
            padx=40
        )

        self._courses_sub = [self.btn_lesson, self.btn_vocab]
        btn_courses.config(command=lambda: self._toggle_submenu(self._courses_sub, btn_courses))

        # === Luyện tập ===
        # btn_practice = make_button(
        #     self, "Luyện tập", self.icons["practice"],
        #     cmd=lambda: self._highlight_and_open(None, "Luyện tập", [])
        # )
        # btn_practice.pack(fill="x", pady=5)

        # =====Game =====
        self.btn_game = make_button(
            self, "Chơi trò chơi", self.icons["game"],
            cmd=lambda: self._highlight_and_open(self.btn_game, "Chơi trò chơi", [])
        )
        self.btn_game.pack(fill="x", pady=5)

        # =====Flashcard ===========
        self.btn_fc = make_button(
            self, "Thẻ từ vựng", self.icons["fc"],
            cmd=lambda: self._highlight_and_open(self.btn_fc, "Thẻ từ vựng", [])
        )
        self.btn_fc.pack(fill="x", pady=5)

        # === Xếp hạng ===
        btn_rank = make_button(
            self, "Xếp hạng", self.icons["ranking"],
            cmd=lambda: self._highlight_and_open(btn_rank, "Xếp hạng", [])
        )
        btn_rank.pack(fill="x", pady=5)

        # === Tài khoản ===
        btn_account = make_button(self, "Tài khoản", self.icons["profile"])
        btn_account.pack(fill="x", pady=5)

        self.btn_profile = make_button(
            self, "Hồ sơ", self.icons["profile1"],
            cmd=lambda: self._highlight_and_open(self.btn_profile, "Hồ sơ", []),
            padx=40
        )
        self.btn_logout = make_button(
            self, "Đăng xuất", self.icons["logout"],
            cmd=self._logout, padx=40
        )

        self._account_sub = [self.btn_profile, self.btn_logout]
        btn_account.config(command=lambda: self._toggle_submenu(self._account_sub, btn_account))

    # ======================================
    # HÀM HỖ TRỢ
    # ======================================

    def _logout(self):
        '''Dùng để logout'''
        self.root.destroy()
        window = tk.Tk()
        from ui.LoginForm import LoginForm
        login_form = LoginForm(window)
        window.mainloop()

    def _highlight_and_open(self, button, title, contents):
        """Làm nổi bật nút và mở nội dung"""
        if self.active_button and self.active_button != button:
            try:
                self.active_button.config(bg="#FFFFFF", fg="#000000")
            except Exception:
                pass

        if button:
            button.config(bg="#e8f6ff", fg="#1da9fe")
            self.active_button = button

        if title == "__BACK__":
            self.main_content.show_lesson_list()
        elif title == "Xếp hạng":
            self.main_content._show_ranking()
        elif title == "Thẻ từ vựng":
            self.main_content._show_decklist(self.current_user)
        else:
            self.main_content.show_lesson_list()
    def _toggle_submenu(self, buttons, parent_btn):
        """Ẩn/hiện submenu"""
        if buttons[0].winfo_ismapped():
            for b in buttons:
                b.pack_forget()
        else:
            for b in buttons:
                b.pack(fill="x", pady=2, after=parent_btn)

    def _go_home(self):
        """Quay về trang chủ"""
        if self.active_button:
            try:
                self.active_button.config(bg="#FFFFFF", fg="#000000")
            except Exception:
                pass
            self.active_button = None
        self.main_content.show_lesson_list()

    def _toggle_sidebar(self, event=None):
        """Thu gọn / mở rộng sidebar"""
        if not self._collapsed:
            self.pack_forget()
            self._toggle_icon.config(text="❯")
            self._collapsed = True
        else:
            # Sidebar luôn nằm bên trái toggle
            self.pack(side="left", fill="y", before=self._toggle_frame)
            self._toggle_icon.config(text="❮")
            self._collapsed = False
