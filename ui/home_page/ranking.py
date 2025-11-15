import tkinter as tk
from tkinter import ttk

# SỬA LẠI IMPORT ĐÚNG
from logic.user.UserManager import UserManager


class Ranking(tk.Frame):
    """Bảng xếp hạng người học"""

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Bảng xếp hạng",
                 font=("Arial", 18, "bold"),
                 bg="white", fg="#1da9fe").pack(pady=20)

        # Lấy danh sách user từ DB bằng UserManager
        user_mgr = UserManager()
        users = user_mgr.get_all()

        # Tạo bảng
        table = ttk.Treeview(
            self,
            columns=("rank", "username", "score"),
            show="headings",
            height=15
        )
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("rank", text="Hạng")
        table.heading("username", text="Tên người dùng")
        table.heading("score", text="Điểm")

        table.column("rank", width=80, anchor="center")
        table.column("username", width=200)
        table.column("score", width=100, anchor="center")

        # --------------------------------------
        # DỮ LIỆU → CHỈ ĐƠN GIẢN HÓA (đã sort)
        # --------------------------------------
        sorted_users = sorted(users, key=lambda u: u.get_user_rank(), reverse=True)

        for idx, user in enumerate(sorted_users, start=1):
            table.insert(
                "",
                "end",
                values=(idx, user.get_user_name(), user.get_user_rank())
            )
