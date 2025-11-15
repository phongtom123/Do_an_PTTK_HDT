import tkinter as tk
from PIL import Image, ImageTk
import os


class SidebarRight(tk.Frame):
    """
    Sidebar bên phải (OOP version)
    Hiển thị thông tin streak, xếp hạng, ... giống phong cách SidebarLeft.
    """

    def __init__(self, root, user_name="Bạn", streak_days=0, rank=0, total_users=0, sidebar_width=250):
        super().__init__(root, bg="#FFFFFF", width=sidebar_width)
        self.root = root
        self.user_name = user_name
        self.streak_days = streak_days
        self.rank = rank
        self.total_users = total_users
        self.sidebar_width = sidebar_width

        # Đường dẫn tới thư mục chứa ảnh assets/main_page/
        self.current_path = os.path.dirname(__file__)
        self.asset_path = os.path.abspath(os.path.join(self.current_path, "../../assets/main_page"))

        # Nạp icon
        self._load_icons()

        # Bố cục
        self.pack(side="right", fill="y", padx=(10, 20), pady=10)
        self.pack_propagate(False)

        # Giao diện
        self._create_ui()

    # =========================================================
    # Load icon
    # =========================================================
    def _load_icons(self):
        """Tải icon và gán vào thuộc tính của sidebar"""
        try:
            fire_img = Image.open(os.path.join(self.asset_path, "fire.png")).resize((28, 28))
            trophy_img = Image.open(os.path.join(self.asset_path, "trophy.png")).resize((28, 28))
            self.fire_icon = ImageTk.PhotoImage(fire_img)
            self.trophy_icon = ImageTk.PhotoImage(trophy_img)
        except Exception as e:
            print(f"⚠️ Không thể tải icon từ {self.asset_path}: {e}")
            self.fire_icon = None
            self.trophy_icon = None

    # =========================================================
    # UI: các card thông tin
    # =========================================================
    def _create_card(self, title, contents, icon=None):
        """Tạo khung thông tin (card)"""
        outer = tk.Frame(self, bg="#FFFFFF", highlightbackground="#e0e0e0", highlightthickness=1, bd=0)
        outer.pack(pady=10, padx=10, fill="x")

        card = tk.Frame(outer, bg="white", bd=0)
        card.pack(padx=3, pady=3, fill="x")

        # Tiêu đề
        title_frame = tk.Frame(card, bg="white")
        title_frame.pack(pady=(10, 5), padx=10, fill="x")

        if icon:
            tk.Label(title_frame, image=icon, bg="white").pack(side="left", padx=(0, 8))
        tk.Label(title_frame, text=title, font=("Arial", 12, "bold"), fg="#1da9fe", bg="white").pack(side="left")

        # Nội dung
        for line in contents:
            tk.Label(card, text=line, font=("Arial", 11), bg="white",
                     anchor="w", justify="left").pack(fill="x", padx=10, pady=3)

        return outer

    # =========================================================
    # Tạo toàn bộ giao diện
    # =========================================================
    def _create_ui(self):
        """Tạo các thẻ hiển thị thông tin"""
        streak_info = [
            f"{self.user_name}",
            f"Chuỗi hiện tại: {self.streak_days} ngày",
            "🔥 Giữ vững phong độ nhé!"
        ]
        self._create_card("Streak hiện tại", streak_info, icon=self.fire_icon)

        rank_info = [
            f"{self.user_name}",
            f"Thứ hạng: {self.rank}/{self.total_users}" if self.total_users > 0 else f"Thứ hạng: {self.rank}",
            "🏆 Cố gắng lên để vào top!"
        ]
        self._create_card("xếp hạng cá nhân", rank_info, icon=self.trophy_icon)

    # =========================================================
    # Hàm cập nhật thông tin động
    # =========================================================
    def update_info(self, user_name=None, streak_days=None, rank=None, total_users=None):
        """Cập nhật dữ liệu và làm mới giao diện"""
        if user_name is not None:
            self.user_name = user_name
        if streak_days is not None:
            self.streak_days = streak_days
        if rank is not None:
            self.rank = rank
        if total_users is not None:
            self.total_users = total_users

        # Xóa tất cả widget con và vẽ lại
        for widget in self.winfo_children():
            widget.destroy()
        self._create_ui()


# =========================================================
# Test độc lập
# =========================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Demo SidebarRight (OOP Version)")
    root.geometry("900x500")

    sidebar = SidebarRight(root, user_name="Linh", streak_days=10, rank=2, total_users=50, sidebar_width=300)

    # Test cập nhật thông tin sau 3 giây
    def update_later():
        sidebar.update_info(streak_days=15, rank=1)
    root.after(3000, update_later)

    root.mainloop()
