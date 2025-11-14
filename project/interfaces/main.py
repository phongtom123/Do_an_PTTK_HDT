import sys, os

# --- (Phần code sửa sys.path của bạn giữ nguyên) ---
interfaces_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(interfaces_dir)
sys.path.insert(0, project_dir) 
root_dir = os.path.dirname(project_dir)
sys.path.insert(0, root_dir)

import tkinter as tk
from tkinter import ttk

# --- IMPORT CÁC MODULE GIAO DIỆN ---
from sidebar_left import create_sidebar_left
from controller.unit_controller import get_all_units

# --- IMPORT CÁC TRANG (PAGE CLASSES) ---
from game import GamePage
from history import HistoryPage
from ranking import RankingPage # Đổi tên từ 'Ranking' để rõ ràng
from db.db import db # Import class 'db'

# ==========================================================
# === LỚP (CLASS) TRANG DANH SÁCH BÀI HỌC (THAY THẾ show_lesson_list) ===
# ==========================================================
class LessonListPage(tk.Frame):
    """Trang hiển thị danh sách tất cả các Unit."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Header ---
        self.create_header(self, part_text="Unit", title_text="Bài mới mỗi ngày")

        # --- Lấy dữ liệu Units ---
        units = get_all_units()

        container_frame = tk.Frame(self, bg="#f9f9f9")
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container_frame, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")
        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig(window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for unit in units:
            unit_name = unit[1] if isinstance(unit, (tuple, list)) else str(unit)
            outer = tk.Frame(scrollable_frame, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")
            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)
            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=unit_name, font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
            tk.Label(left, text="✅ HOÀN THÀNH", font=("Arial", 11, "bold"),
                     bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))

            tk.Button(inner, text="ÔN TẬP", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      activebackground="#ecf5ff", cursor="hand2",
                      width=10, height=1,
                      command=lambda u=unit_name: self.controller.show_lesson_details(u)
            ).pack(side="right")

    def create_header(self, parent, part_text, title_text, color="#1da9fe", back_callback=None):
        wrapper = tk.Frame(parent, bg="#f9f9f9")
        wrapper.pack(fill="x", padx=20, pady=15)
        header = tk.Frame(wrapper, bg=color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        back_label = tk.Label(header, text=f"← {part_text}", bg=color, fg="white",
                              font=("Arial", 10, "bold"), anchor="w", cursor="hand2")
        back_label.pack(anchor="w", padx=20, pady=(10, 0))
        if back_callback:
            back_label.bind("<Button-1>", lambda e: back_callback())
        tk.Label(header, text=title_text, bg=color, fg="white",
                 font=("Arial", 14, "bold"), anchor="w").pack(anchor="w", padx=20, pady=(2, 10))
        return header

# ==========================================================
# ===          LỚP (CLASS) ỨNG DỤNG CHÍNH (APP)          ===
# ==========================================================

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("BulaBuluuuu")
        self.geometry("1100x700")
        self.configure(bg="#FFFFFF")

        self.db_class = db
        self.current_user_id = 1 # Tạm thời hard-code user_id
        self.current_mode = None
        self.in_learning_mode = False
        
        # --- Tạo Sidebar ---
        # **QUAN TRỌNG: Truyền 'self' (chính là App object) làm controller**
        create_sidebar_left(self, self)

        # --- Tạo Container Frame ---
        self.container = tk.Frame(self)
        self.container.pack(side="left", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- Chuẩn bị tất cả các trang ---
        self.frames = {}
        for F in (LessonListPage, GamePage, HistoryPage, RankingPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LessonListPage")

    def show_frame(self, page_name):
        """Hiển thị một frame (trang) dựa theo tên Class của nó."""
        frame = self.frames[page_name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

    def show_page_from_sidebar(self, title, contents=None, mode=None):
        """
        Hàm này được 'sidebar_left' gọi.
        'self' ở đây là 'App', nó CÓ thuộc tính 'show_page_from_sidebar'.
        """
        print(f"Sidebar gọi: {title}")
        if title == "Game":
            self.show_frame("GamePage")
        elif title == "lịch sử":
            self.show_frame("HistoryPage")
        elif title == "Xếp hạng":
            self.show_frame("RankingPage")
        elif title == "Reading":
            # (Bạn sẽ cần tạo 1 trang ReadingPage và gọi nó ở đây)
            # self.current_mode = "Reading"
            # self.show_frame("ReadingListPage")
            print("Chưa lập trình trang Reading")
            pass
        elif title == "Listening":
            print("Chưa lập trình trang Listening")
            pass
        elif title == "__BACK__":
            self.show_frame("LessonListPage")
        else:
            self.show_frame("LessonListPage")

    def show_lesson_details(self, unit_name):
        """(Chưa lập trình)"""
        print(f"Mở chi tiết cho: {unit_name}")


# --- Chạy ứng dụng ---
if __name__ == "__main__":
    app = App()
    app.mainloop()