import tkinter as tk
from PIL import Image, ImageTk   # Cần Pillow: pip install pillow

def create_sidebar_right(root, user_name="Bạn", streak_days=0, rank=0, total_users=0, sidebar_width=250):
    sidebar = tk.Frame(root, bg="#FFFFFF", width=sidebar_width)
    sidebar.pack(side="right", fill="y", padx=(10,20), pady=10)
    sidebar.pack_propagate(False)

    # Nạp icon 
    fire_img = Image.open("./photos/fire.png").resize((24, 24))
    trophy_img = Image.open("./photos/trophy.png").resize((24, 24))
    fire_icon = ImageTk.PhotoImage(fire_img)
    trophy_icon = ImageTk.PhotoImage(trophy_img)

    # Để giữ icon không bị thu hồi bộ nhớ (Tkinter bug thường gặp)
    sidebar.fire_icon = fire_icon
    sidebar.trophy_icon = trophy_icon

    def create_card(parent, title, contents, icon=None):
        outer = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#e0e0e0", highlightthickness=1, bd=0)
        outer.pack(pady=10, padx=10, fill="x")

        card = tk.Frame(outer, bg="white", bd=0)
        card.pack(padx=3, pady=3, fill="x")

        # Tiêu đề với icon
        title_frame = tk.Frame(card, bg="white")
        title_frame.pack(pady=(10,5), padx=10, fill="x")

        if icon:
            tk.Label(title_frame, image=icon, bg="white").pack(side="left", padx=(0,8))
        tk.Label(title_frame, text=title, font=("Arial",12,"bold"), bg="white").pack(side="left")

        # Nội dung
        for line in contents:
            tk.Label(card, text=line, font=("Arial",11), bg="white", anchor="w", justify="left").pack(fill="x", padx=10, pady=3)

        return outer

    # Streak cá nhân 
    streak_info = [
        f"{user_name}",
        f"Chuỗi hiện tại: {streak_days} ngày",
        "Giữ vững phong độ nhé!"
    ]
    create_card(sidebar, "Streak hiện tại", streak_info, icon=fire_icon)

    # Xếp hạng cá nhân
    rank_info = [
        f"{user_name}",
        f"Thứ hạng: {rank}/{total_users}" if total_users > 0 else f"Thứ hạng: {rank}",
        "Cố gắng lên để vào top!"
    ]
    create_card(sidebar, "Bảng xếp hạng cá nhân", rank_info, icon=trophy_icon)

    return sidebar

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    root.title("Demo Sidebar Right")

    create_sidebar_right(root, user_name="Linh", streak_days=10, rank=2, total_users=50, sidebar_width=300)

    root.mainloop()
