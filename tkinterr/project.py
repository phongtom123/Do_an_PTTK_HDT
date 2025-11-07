import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1024x768")
root.configure(bg="#FFFFFF")

# ===== Load icon =====
icon_learn = ImageTk.PhotoImage(Image.open("./photos/Home.png").resize((35, 35)))
icon_practice = ImageTk.PhotoImage(Image.open("./photos/Practice.png").resize((35, 35)))
icon_profile = ImageTk.PhotoImage(Image.open("./photos/avataaars.png").resize((35, 35)))
icon_more = ImageTk.PhotoImage(Image.open("./photos/More.png").resize((35, 35)))
icon_ranking= ImageTk.PhotoImage(Image.open("./photos/ranking.png"). resize((35,35)))
icon_vocab= ImageTk.PhotoImage(Image.open("./photos/vocab.png"). resize((25,25)))
icon_logout = ImageTk.PhotoImage(Image.open("./photos/logout.png"). resize((25,25)))
icon_profile1 = ImageTk.PhotoImage(Image.open("./photos/profile.png"). resize((25,25)))
icon_book = ImageTk.PhotoImage(Image.open("./photos/book.png"). resize((25,25)))
icon_earphone= ImageTk.PhotoImage(Image.open("./photos/earphone.png"). resize((20,20)))

# ===== Sidebar Trái =====
sidebar_left = tk.Frame(root, bg="#FFFFFF", width=220, highlightbackground="#e0e0e0", highlightthickness=1)
sidebar_left.pack(side="left", fill="y")
sidebar_left.pack_propagate(False)

# ===== Logo =====
logo_frame = tk.Frame(sidebar_left, bg="#FFFFFF", height=120)
logo_frame.pack(fill="x")
logo_frame.pack_propagate(False)

def go_home():
    show_in_main("Home", ["Welcome to Home"])

try:
    logo_img = Image.open("./photos/2.png").resize((150, 130))
    logo_photo = ImageTk.PhotoImage(logo_img)
    # Đổi từ Label sang Button để có thể click
    logo_button = tk.Button(
        logo_frame,
        image=logo_photo,
        bg="#FFFFFF",
        bd=0,
        activebackground="#FFFFFF",
        command=go_home
    )
    logo_button.image = logo_photo
    logo_button.pack(pady=20)
except:
    logo_label = tk.Button(
        logo_frame,
        text="My Logo",
        font=("Arial", 16, "bold"),
        fg="black",
        bg="#FFFFFF",
        bd=0,
        activebackground="#FFFFFF",
        command=go_home
    )
    logo_label.pack(pady=20)

# ===== Main Frame =====
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="left", fill="both", expand=True, padx=(0, 0))

def show_message(msg):
    messagebox.showinfo("Menu", f"Bạn chọn: {msg}")

def show_in_main(title, options):
    for widget in main_frame.winfo_children():
        widget.destroy()
    lbl = tk.Label(main_frame, text=title, font=("Arial", 16, "bold"), bg="white")
    lbl.pack(pady=10)
    colors = ["#3498db", "#2ecc71", "#f1c40f"]
    for i, opt in enumerate(options):
        btn = tk.Button(
            main_frame,
            text=opt,
            font=("Arial", 14, "bold"),
            command=lambda x=opt: show_message(f"{title} - {x}"),
            bg=colors[i % len(colors)],
            fg="white" if colors[i] != "#f1c40f" else "black",
            width=30,
            height=2,
            relief="raised",
            bd=4,
            highlightthickness=0,
            activebackground="#666"
        )
        btn.pack(pady=15)

# ===== Style helper có highlight =====
active_button = None  # Biến toàn cục để lưu nút hiện tại

def make_button(parent, text, icon=None, cmd=None, padx=20, anchor="w"):
    def on_click():
        global active_button
        # Nếu đã có nút đang chọn → reset màu cũ
        if active_button and active_button != btn:
            active_button.config(bg="#FFFFFF", font=("Arial", 12))
        # Đổi màu nút hiện tại
        btn.config(bg="#e8f4ff", font=("Arial", 12, "bold"))
        active_button = btn
        if cmd:
            cmd()
    btn = tk.Button(
        parent,
        image=icon,
        text=f"  {text}" if icon else text,
        compound="left",
        command=on_click,
        font=("Arial", 12),
        fg="black",
        bg="#FFFFFF",
        activebackground="#f0f0f0",
        bd=0,
        anchor=anchor,
        padx=padx
    )
    return btn


# ===== Nút chính Sidebar trái =====

# ===== Toggle Courses =====
courses_open = False
btn_courses = make_button(sidebar_left, "Học", icon_learn)
btn_courses.pack(fill="x", pady=5)

# Các mục con Courses
btn_reading = make_button(
    sidebar_left,
    "Reading",
    icon_book,
    cmd=lambda: show_in_main("Reading", ["Unit 1", "Unit 2", "Unit 3"]),
    padx=40
)
btn_listening = make_button(
    sidebar_left,
    "Listening",
    icon_earphone,
    cmd=lambda: show_in_main("Listening", ["Unit 1", "Unit 2", "Unit 3"]),
    padx=40
)
btn_vocab = make_button(
    sidebar_left,
    "Từ vựng",
    icon_vocab,
    cmd=lambda: show_in_main("Từ vựng", ["Từ mới hôm nay", "Ôn tập tuần"]),
    padx=40
)

# Gom lại thành nhóm con của "Học"
courses_sub = [btn_reading, btn_listening, btn_vocab]

def toggle_courses():
    global courses_open
    if courses_open:
        for btn in courses_sub:
            btn.pack_forget()
        courses_open = False
    else:
        # Hiển thị tất cả các nút con sau "Học"
        for btn in courses_sub:
            btn.pack(fill="x", pady=2, after=btn_courses)
        courses_open = True

btn_courses.config(command=toggle_courses)


# ===== Nút khác Sidebar trái =====
btn_streak = make_button(sidebar_left, "Luyện Tập", icon_practice, lambda: show_in_main("Streak", ["Day 1"]))
btn_streak.pack(fill="x", pady=5)

# ===== Nút Xếp hạng =====
btn_leaderboard = make_button(
    sidebar_left,
    "Xếp hạng",
    icon_ranking,   # bạn có thể thay bằng icon riêng (vd: trophy.png)
    lambda: show_in_main("Leaderboard", ["Top 1: Nam", "Top 2: Linh"])
)
btn_leaderboard.pack(fill="x", pady=5)

# ===== Nút Xem thêm =====
btn_settings = make_button(sidebar_left, "Xem thêm", icon_more, lambda: show_in_main("Settings", ["Profile", "Security"]))
btn_settings.pack(fill="x", pady=5)

# ===== Toggle Account =====
account_open = False
btn_account = make_button(sidebar_left, "Tài khoản", icon_profile)
btn_account.pack(fill="x", pady=5)

# Các mục con Account
btn_logout = make_button(sidebar_left, "Đăng xuất", icon_logout, cmd=root.quit, padx=40)
btn_profile = make_button(sidebar_left, "Hồ sơ", icon_profile1, cmd=lambda: show_in_main("Profile", ["Thông tin cá nhân"]), padx=40)
account_sub = [btn_profile, btn_logout]

def toggle_account():
    global account_open
    if account_open:
        for btn in account_sub:
            btn.pack_forget()
        account_open = False
    else:
        for btn in account_sub:
            btn.pack(fill="x", pady=2, after=btn_account)
        account_open = True

btn_account.config(command=toggle_account)

# ===== Sidebar Phải =====
sidebar_right = tk.Frame(root, bg="#FFFFFF", width=200)
sidebar_right.pack(side="right", fill="y", padx=(10, 20), pady=10)
sidebar_right.pack_propagate(False)

# ===== Hàm tạo card bo tròn =====
def create_rounded_card(parent, title, options):
    outer = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#e0e0e0",
                     highlightthickness=1, bd=0)
    outer.pack(pady=10, padx=10, fill="x")
    card = tk.Frame(outer, bg="white", bd=0)
    card.pack(padx=3, pady=3, fill="x")
    lbl = tk.Label(card, text=title, font=("Arial", 12, "bold"), bg="white")
    lbl.pack(pady=(10,5), padx=10)
    for opt in options:
        btn = tk.Button(card, text=opt, font=("Arial", 11),
                        bg="#3498db", fg="white",
                        activebackground="#2980b9", bd=0)
        btn.pack(fill="x", padx=10, pady=5)
    return outer

# ===== Tạo các card Sidebar phải =====
create_rounded_card(sidebar_right, "🔥 Streak", ["Chuỗi 5 ngày", "Thưởng hôm nay"])
create_rounded_card(sidebar_right, "🏆 Bảng xếp hạng", ["Top 1: Nam", "Top 2: Linh"])

# ===== Mặc định hiển thị Home =====
show_in_main("Home", ["Welcome to Home"])

root.mainloop()
