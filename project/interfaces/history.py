import tkinter as tk
from tkinter import ttk

def create_history_screen(parent):
    
    # Xóa mọi thứ đang có trên frame 'parent' trước khi vẽ
    for widget in parent.winfo_children():
        widget.destroy()

    # Đặt màu nền cho frame cha
    parent.config(bg="white")

    # --- Frame cho nội dung ---
    history_frame = tk.Frame(parent, bg="white")
    history_frame.pack(expand=True, fill="both", pady=20, padx=50)

    # --- Tiêu đề ---
    tk.Label(history_frame, text="Lịch sử Game", 
             font=("Arial", 18, "bold"), 
             bg="white").pack(pady=(10, 20))

    # --- Bảng Lịch sử ---
    columns = ("stt", "thoi_gian", "ngay_choi", "dung", "sai")
    
    tree = ttk.Treeview(history_frame, columns=columns, show="headings")
    
    # Định nghĩa tiêu đề cột
    tree.heading("stt", text="STT")
    tree.heading("thoi_gian", text="Thời gian")
    tree.heading("ngay_choi", text="Ngày chơi")
    tree.heading("dung", text="Đáp án đúng")
    tree.heading("sai", text="Đáp án sai")

    # Định nghĩa độ rộng và căn lề
    tree.column("stt", width=50, anchor="center")
    tree.column("thoi_gian", width=100, anchor="center")
    tree.column("ngay_choi", width=150, anchor="center")
    tree.column("dung", width=100, anchor="center")
    tree.column("sai", width=100, anchor="center")

    # --- Thêm dữ liệu giả vào bảng ---
    dummy_data = [
        (1, "0:59", "2023-10-10", 120, 12),
        (2, "0:55", "2023-10-09", 80, 8),
        (3, "1:00", "2023-10-09", 150, 0),
        (4, "0:45", "2023-10-08", 50, 5)
    ]
    
    for item in dummy_data:
        tree.insert("", "end", values=item)

    tree.pack(expand=True, fill="both")
