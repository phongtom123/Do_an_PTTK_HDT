import tkinter as tk
from tkinter import ttk
# --- IMPORT DB ---
from db.db import db

def create_history_screen(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    # (Style giữ nguyên)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#2c3e50",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', '#34495e')])
    style.configure("Treeview",
                    highlightthickness=0,
                    bd=0,
                    font=('Arial', 12),
                    rowheight=40,
                    fieldbackground="#ffffff")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    parent.config(bg="white")

    history_frame = tk.Frame(parent, bg="white")
    history_frame.pack(expand=True, fill="both", pady=20, padx=50)

    tk.Label(history_frame, text="Lịch sử Chơi Game", 
             font=("Arial", 18, "bold"), 
             bg="white").pack(pady=(10, 20))

    # --- THAY ĐỔI 1: XÓA CỘT "Ngày chơi" ---
    columns = ("id", "nguoi_choi", "diem_so")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings")
    
    tree.heading("id", text="ID Lượt Chơi")
    tree.heading("nguoi_choi", text="Người chơi")
    tree.heading("diem_so", text="Điểm")

    tree.column("id", width=100, anchor="center")
    tree.column("nguoi_choi", width=200, anchor="w")
    tree.column("diem_so", width=100, anchor="center")

    # --- THAY ĐỔI 2: CẬP NHẬT CÂU TRUY VẤN ---
    
    db_conn = db()
    # Sửa tên bảng: GameHistory -> games
    # Sửa tên cột: H.history_id -> H.game_id
    # Sửa tên cột: H.user_id -> H.game_user_id
    # Xóa cột 'DATE_FORMAT' (vì không tồn tại)
    query = """
        SELECT 
            H.game_id, 
            U.user_name, 
            H.score
        FROM 
            games H
        JOIN 
            Users U ON H.game_user_id = U.user_id
        ORDER BY 
            H.game_id DESC
        LIMIT 20
    """
    
    df = db_conn.query(query)
    db_conn.close()

    if df.empty:
        # --- THAY ĐỔI 3: Cập nhật giá trị rỗng ---
        tree.insert("", "end", values=("", "Chưa có lịch sử chơi", ""))
    else:
        # --- THAY ĐỔI 4: Cập nhật cách đọc dữ liệu ---
        for index, row in df.iterrows():
            tree.insert("", "end", values=(
                row['game_id'], 
                row['user_name'], 
                row['score']
            ))

    tree.pack(expand=True, fill="both")