import tkinter as tk
import sys, os
from PIL import Image, ImageTk

# (Import Ranking và get_all_units không còn cần thiết ở đây,
# vì main.py (controller) sẽ xử lý việc đó)
# from ranking import Ranking 
# from controller.unit_controller import get_all_units

from utils.make_button import make_button

# --- THAY ĐỔI 1: Sửa tham số đầu vào ---
# Bỏ 'show_in_main', thay bằng 'controller' (chính là class App)
def create_sidebar_left(root, controller): 
    # === Tạo container chứa sidebar + toggle ===
    container = tk.Frame(root, bg="#FFFFFF")
    container.pack(side="left", fill="y")

    # === Sidebar chính ===
    sidebar_left = tk.Frame(
        container,
        bg="#FFFFFF",
        width=200,
        highlightbackground="#e0e0e0",
        highlightthickness=1
    )
    sidebar_left.pack(side="left", fill="y")
    sidebar_left.pack_propagate(False)

    # === Khung toggle (Giữ nguyên) ===
    toggle_frame = tk.Frame(container, bg="#FFFFFF", width=15)
    toggle_frame.pack(side="left", fill="y")
    toggle_icon = tk.Label(
        toggle_frame,
        text="<",
        font=("Arial", 12, "bold"),
        bg="#FFFFFF",
        cursor="hand2"
    )
    toggle_icon.pack(padx=5, pady=10)
    collapsed = [False]

    # === Load icon (Giữ nguyên) ===
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
    load("trochoi", "./photos/icon_trochoi.png", (35,35))
    load("ranking", "./photos/ranking.png", (35,35))
    load("vocab", "./photos/vocab.png", (25,25))
    load("logout", "./photos/logout.png", (25,25))
    load("profile1", "./photos/profile.png", (25,25))
    load("book", "./photos/book.png", (25,25))
    load("earphone", "./photos/earphone.png", (20,20))
    load("history", "./photos/history.png", (25,25))
    sidebar_left._icons = icons

    # === Logo (Giữ nguyên) ===
    logo_frame = tk.Frame(sidebar_left, bg="#FFFFFF", height=120)
    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)

    def go_home():
        # --- THAY ĐỔI 2: Gọi controller ---
        controller.show_page_from_sidebar("__BACK__", [])

    try:
        img2 = Image.open("./photos/2.png").resize((150,130))
        photo2 = ImageTk.PhotoImage(img2)
        btn_logo = tk.Button(
            logo_frame, image=photo2, bg="#FFFFFF", bd=0,
            activebackground="#FFFFFF", command=go_home
        )
        btn_logo.image = photo2
        btn_logo.pack(pady=20)
    except Exception:
        tk.Button(
            logo_frame, text="My Logo", font=("Arial", 16, "bold"),
            fg="black", bg="#FFFFFF", bd=0, activebackground="#FFFFFF",
            command=go_home
        ).pack(pady=20)

    # === MỤC HỌC (Giữ nguyên logic toggle) ===
    btn_courses = make_button(sidebar_left, "Học", icons["learn"])
    btn_courses.pack(fill="x", pady=5)

    btn_vocab = make_button(
        sidebar_left, "Từ vựng", icons["vocab"],
        # --- THAY ĐỔI 3: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Từ vựng", []), 
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

    # === MỤC LUYỆN TẬP (Giữ nguyên logic toggle) ===
    btn_practice = make_button(
        sidebar_left, "Luyện tập", icons["practice"]
    )
    btn_practice.pack(fill="x", pady=5)

    btn_reading = make_button(
        sidebar_left, "Reading", icons["book"],
        # --- THAY ĐỔI 4: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Reading", []), 
        padx=40
    )
    btn_listening = make_button(
        sidebar_left, "Listening", icons["earphone"],
        # --- THAY ĐỔI 5: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Listening", []), 
        padx=40
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

    # === MỤC TRÒ CHƠI (Giữ nguyên logic toggle) ===
    btn_trochoi = make_button(
        sidebar_left, "Trò chơi", icons["trochoi"]
    )
    btn_trochoi.pack(fill="x", pady=5)

    # Nút con "Chơi Game"
    btn_game = make_button(
        sidebar_left, "Chơi Game", icons["book"], 
        # --- THAY ĐỔI 6: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Game", []), 
        padx=40
    )

    # Nút con "Lịch sử"
    btn_history = make_button(
        sidebar_left, "Lịch sử", icons["history"],
        # --- THAY ĐỔI 7: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("lịch sử", []), 
        padx=40
    )

    # (Logic toggle giữ nguyên)
    trochoi_sub = [btn_history, btn_game] # (Bạn đã đảo thứ tự 2 nút này, tôi giữ nguyên)
    trochoi_open = False
    def toggle_trochoi():
        nonlocal trochoi_open
        if trochoi_open:
            for b in trochoi_sub:
                b.pack_forget()
            trochoi_open = False
        else:
            for b in trochoi_sub:
                b.pack(fill="x", pady=2, after=btn_trochoi) 
            trochoi_open = True
    btn_trochoi.config(command=toggle_trochoi)

    # === CÁC MỤC KHÁC ===
    btn_rank = make_button(
        sidebar_left, "Xếp hạng", icons["ranking"],
        # --- THAY ĐỔI 8: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Xếp hạng", [])
    )
    btn_rank.pack(fill="x", pady=5)

    btn_more = make_button(
        sidebar_left, "Xem thêm", icons["more"],
        # --- THAY ĐỔI 9: Gọi controller ---
        lambda: controller.show_page_from_sidebar("Xem thêm", [])
    )
    btn_more.pack(fill="x", pady=5)

    # === Account toggle (Giữ nguyên logic toggle) ===
    btn_account = make_button(sidebar_left, "Tài khoản", icons["profile"])
    btn_account.pack(fill="x", pady=5)

    btn_profile = make_button(
        sidebar_left, "Hồ sơ", icons["profile1"],
        # --- THAY ĐỔI 10: Gọi controller ---
        cmd=lambda: controller.show_page_from_sidebar("Hồ sơ", []), 
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

    # === Toggle Sidebar (Giữ nguyên logic) ===
    def toggle_sidebar(event=None):
        if not collapsed[0]:
            # Đóng sidebar
            for widget in sidebar_left.winfo_children():
                widget.pack_forget()
            sidebar_left.config(width=10, highlightthickness=0)
            toggle_icon.config(text=">")
            collapsed[0] = True
        else:
            # Mở lại sidebar
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
            
            # --- THAY ĐỔI 11: Thêm lại nút Trò chơi khi mở ---
            btn_trochoi.pack(fill="x", pady=5)
            if trochoi_open:
                for b in trochoi_sub:
                    b.pack(fill="x", pady=2, after=btn_trochoi)
            # --- Hết ---

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