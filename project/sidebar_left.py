# sidebar_left.py
import tkinter as tk
from PIL import Image, ImageTk
from utils import make_button

def create_sidebar_left(root, show_in_main):
    """
    Tạo sidebar trái (pack(side='left') trực tiếp trong đây).
    Lưu icons vào attribute của frame để tránh GC.
    """
    # Tạo frame
    sidebar_left = tk.Frame(root, bg="#FFFFFF", width=220, highlightbackground="#e0e0e0", highlightthickness=1)
    sidebar_left.pack(side="left", fill="y")
    sidebar_left.pack_propagate(False)

    # Load icon (nếu file không tồn tại thì bỏ qua ảnh)
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
    # tránh GC: attach icons dict vào frame
    sidebar_left._icons = icons

    # Logo area
    logo_frame = tk.Frame(sidebar_left, bg="#FFFFFF", height=120)
    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)

    def go_home():
        # khi về home: reset highlight
        show_in_main("Home", ["Welcome to Home"])
        if getattr(make_button, "active_button", None):
            make_button.active_button.config(bg="#FFFFFF", font=("Arial", 12))
            make_button.active_button = None

    try:
        img2 = Image.open("./photos/2.png").resize((150,130))
        photo2 = ImageTk.PhotoImage(img2)
        btn_logo = tk.Button(logo_frame, image=photo2, bg="#FFFFFF", bd=0, activebackground="#FFFFFF", command=go_home)
        btn_logo.image = photo2
        btn_logo.pack(pady=20)
    except Exception:
        tk.Button(logo_frame, text="My Logo", font=("Arial", 16, "bold"),
                  fg="black", bg="#FFFFFF", bd=0, activebackground="#FFFFFF", command=go_home).pack(pady=20)

    # helper & các nút
    btn_courses = make_button(sidebar_left, "Học", icons["learn"])
    btn_courses.pack(fill="x", pady=5)

    btn_reading = make_button(sidebar_left, "Reading", icons["book"],
                              cmd=lambda: show_in_main("Reading", ["Unit 1","Unit 2","Unit 3"]), padx=40)
    btn_listening = make_button(sidebar_left, "Listening", icons["earphone"],
                                cmd=lambda: show_in_main("Listening", ["Unit 1","Unit 2","Unit 3"]), padx=40)
    btn_vocab = make_button(sidebar_left, "Từ vựng", icons["vocab"],
                            cmd=lambda: show_in_main("Từ vựng", ["Từ mới hôm nay","Ôn tập tuần"]), padx=40)
    courses_sub = [btn_reading, btn_listening, btn_vocab]
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

    # other buttons
    make_button(sidebar_left, "Luyện tập", icons["practice"],
                lambda: show_in_main("Luyện tập", ["Day 1"])).pack(fill="x", pady=5)
    make_button(sidebar_left, "Xếp hạng", icons["ranking"],
                lambda: show_in_main("Xếp hạng", ["Top 1: Nam","Top 2: Linh"])).pack(fill="x", pady=5)
    make_button(sidebar_left, "Xem thêm", icons["more"],
                lambda: show_in_main("Xem thêm", ["Profile","Security"])).pack(fill="x", pady=5)

    # account toggle
    btn_account = make_button(sidebar_left, "Tài khoản", icons["profile"])
    btn_account.pack(fill="x", pady=5)

    btn_profile = make_button(sidebar_left, "Hồ sơ", icons["profile1"],
                              cmd=lambda: show_in_main("Hồ sơ", ["Thông tin cá nhân"]), padx=40)
    btn_logout = make_button(sidebar_left, "Đăng xuất", icons["logout"],
                             cmd=root.quit, padx=40)
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

    # trả về frame để dễ truy cập (không bắt buộc)
    return sidebar_left
