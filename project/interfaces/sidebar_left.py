import tkinter as tk
import sys, os
from PIL import Image, ImageTk

# thêm đường dẫn cha để import controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.unit_controller import get_all_units
from utils.make_button import make_button


# === HÀM PHỤ CẦN CÓ TRƯỚC ===
def highlight_and_open(root, button, show_in_main, title, contents):
    """Làm nổi bật nút được chọn, cập nhật trạng thái và mở nội dung"""
    # Bỏ highlight cũ
    if hasattr(root, "active_button") and root.active_button is not None:
        try:
            root.active_button.config(bg="#FFFFFF", fg="#000000")
        except Exception:
            pass

    # Highlight nhẹ nút hiện tại
    try:
        button.config(bg="#e8f6ff", fg="#1da9fe")
    except Exception:
        pass

    root.active_button = button
    root.current_mode = title
    show_in_main(title, contents)


def create_sidebar_left(root, show_in_main):
    # === Container chính ===
    container = tk.Frame(root, bg="#FFFFFF")
    container.pack(side="left", fill="y")

    sidebar_left = tk.Frame(
        container,
        bg="#FFFFFF",
        width=200,
        highlightbackground="#e0e0e0",
        highlightthickness=1
    )
    sidebar_left.pack(side="left", fill="y")
    sidebar_left.pack_propagate(False)

    # === Toggle (mở / đóng sidebar) ===
    toggle_frame = tk.Frame(container, bg="#FFFFFF", width=15)
    toggle_frame.pack(side="left", fill="y")

    toggle_icon = tk.Label(
        toggle_frame, text="<", font=("Arial", 12, "bold"),
        bg="#FFFFFF", cursor="hand2"
    )
    toggle_icon.pack(padx=5, pady=10)

    collapsed = [False]

    # === Load icon ===
    icons = {}
    def load(name, path, size):
        try:
            img = Image.open(path).resize(size)
            icons[name] = ImageTk.PhotoImage(img)
        except Exception:
            icons[name] = None

    load("learn", "./photos/Home.png", (35,35))
    load("practice", "./photos/Practice.png", (35,35))
    load("profile", "./photos/avataaars.png", (35,35))
    load("more", "./photos/More.png", (35,35))
    load("ranking", "./photos/ranking.png", (35,35))
    load("vocab", "./photos/vocab.png", (25,25))
    load("logout", "./photos/logout.png", (25,25))
    load("profile1", "./photos/profile.png", (25,25))
    load("book", "./photos/book.png", (25,25))
    load("earphone", "./photos/earphone.png", (20,20))
    sidebar_left._icons = icons

    # === Logo ===
    logo_frame = tk.Frame(sidebar_left, bg="#FFFFFF", height=120)
    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)

    def go_home():
        """Khi click logo → bỏ highlight, reset current_mode, quay về trang chủ"""
        try:
            if hasattr(root, "active_button") and root.active_button is not None:
                try:
                    root.active_button.config(bg="#FFFFFF", fg="#000000")
                except Exception:
                    pass
                root.active_button = None

            root.current_mode = None
            show_in_main("__BACK__", [])
        except Exception as e:
            print("⚠️ Lỗi khi click logo:", e)
            try:
                show_in_main("__BACK__", [])
            except Exception:
                pass

    try:
        img2 = Image.open("./photos/2.png").resize((150,130))
        photo2 = ImageTk.PhotoImage(img2)
        logo_label = tk.Label(logo_frame, image=photo2, bg="#FFFFFF", cursor="hand2")
        logo_label.image = photo2
        logo_label.pack(pady=(15, 0))
        tk.Label(logo_frame, text="bleu", fg="#1da9fe", bg="#FFFFFF",
                 font=("Arial", 18, "bold")).pack()
        logo_label.bind("<Button-1>", lambda e: go_home())
    except Exception:
        tk.Button(
            logo_frame, text="bleu", font=("Arial", 18, "bold"),
            fg="#1da9fe", bg="#FFFFFF", bd=0, activebackground="#FFFFFF",
            command=go_home
        ).pack(pady=20)

    # === MỤC HỌC ===
    btn_courses = make_button(sidebar_left, "Học", icons["learn"])
    btn_courses.pack(fill="x", pady=5)

    btn_vocab = make_button(
        sidebar_left, "Từ vựng", icons["vocab"],
        cmd=lambda: highlight_and_open(root, btn_vocab, show_in_main,
                                       "Từ vựng", ["Từ mới hôm nay","Ôn tập tuần"]),
        padx=40
    )

    courses_sub = [btn_vocab]
    courses_open = False
    def toggle_courses():
        nonlocal courses_open
        if courses_open:
            for b in courses_sub:
                b.pack_forget()
            courses_open = False
        else:
            for b in courses_sub:
                b.pack(fill="x", pady=2, after=btn_courses)
            courses_open = True
    btn_courses.config(command=toggle_courses)

    # === MỤC LUYỆN TẬP ===
    btn_practice = make_button(sidebar_left, "Luyện tập", icons["practice"])
    btn_practice.pack(fill="x", pady=5)

    btn_reading = make_button(
        sidebar_left, "Reading", icons["book"],
        cmd=lambda: highlight_and_open(root, btn_reading, show_in_main,
                                       "Reading", get_all_units()), padx=40
    )
    btn_listening = make_button(
        sidebar_left, "Listening", icons["earphone"],
        cmd=lambda: highlight_and_open(root, btn_listening, show_in_main,
                                       "Listening", get_all_units()), padx=40
    )

    practice_sub = [btn_reading, btn_listening]
    practice_open = False
    def toggle_practice():
        nonlocal practice_open
        if practice_open:
            for b in practice_sub:
                b.pack_forget()
            practice_open = False
        else:
            for b in practice_sub:
                b.pack(fill="x", pady=2, after=btn_practice)
            practice_open = True
    btn_practice.config(command=toggle_practice)

    # === CÁC MỤC KHÁC ===
    btn_rank = make_button(
        sidebar_left, "Xếp hạng", icons["ranking"],
        lambda: highlight_and_open(root, btn_rank, show_in_main,
                                   "Xếp hạng", ["Top 1: Nam","Top 2: Linh"])
    )
    btn_rank.pack(fill="x", pady=5)

    btn_more = make_button(
        sidebar_left, "Xem thêm", icons["more"],
        lambda: highlight_and_open(root, btn_more, show_in_main,
                                   "Xem thêm", ["Profile","Security"])
    )
    btn_more.pack(fill="x", pady=5)

    # === Tài khoản ===
    btn_account = make_button(sidebar_left, "Tài khoản", icons["profile"])
    btn_account.pack(fill="x", pady=5)

    btn_profile = make_button(
        sidebar_left, "Hồ sơ", icons["profile1"],
        cmd=lambda: highlight_and_open(root, btn_profile, show_in_main,
                                       "Hồ sơ", ["Thông tin cá nhân"]),
        padx=40
    )
    btn_logout = make_button(
        sidebar_left, "Đăng xuất", icons["logout"],
        cmd=root.quit, padx=40
    )

    account_sub = [btn_profile, btn_logout]
    account_open = False
    def toggle_account():
        nonlocal account_open
        if account_open:
            for b in account_sub:
                b.pack_forget()
            account_open = False
        else:
            for b in account_sub:
                b.pack(fill="x", pady=2, after=btn_account)
            account_open = True
    btn_account.config(command=toggle_account)

    # === Toggle Sidebar ===
    def toggle_sidebar(event=None):
        if not collapsed[0]:
            for widget in sidebar_left.winfo_children():
                widget.pack_forget()
            sidebar_left.config(width=10, highlightthickness=0)
            toggle_icon.config(text=">")
            collapsed[0] = True
        else:
            sidebar_left.config(width=200, highlightthickness=1, highlightbackground="#e0e0e0")
            logo_frame.pack(fill="x")
            btn_courses.pack(fill="x", pady=5)
            if courses_open:
                for b in courses_sub:
                    b.pack(fill="x", pady=2, after=btn_courses)
            btn_practice.pack(fill="x", pady=5)
            if practice_open:
                for b in practice_sub:
                    b.pack(fill="x", pady=2, after=btn_practice)
            btn_rank.pack(fill="x", pady=5)
            btn_more.pack(fill="x", pady=5)
            btn_account.pack(fill="x", pady=5)
            if account_open:
                for b in account_sub:
                    b.pack(fill="x", pady=2, after=btn_account)
            toggle_icon.config(text="<")
            collapsed[0] = False

    toggle_icon.bind("<Button-1>", toggle_sidebar)

    return container
