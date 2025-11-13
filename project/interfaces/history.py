import tkinter as tk
from tkinter import ttk
# --- IMPORT DB ---
# (Đã sửa để trỏ đúng 'db.db' như yêu cầu)
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

    # --- THAY ĐỔI 1: SỬA TIÊU ĐỀ ---
    tk.Label(history_frame, text="Lịch sử Chơi Game", 
             font=("Arial", 18, "bold"), 
             bg="white").pack(pady=(10, 20))

    # --- THAY ĐỔI 2: SỬA CÁC CỘT ---
    columns = ("id", "nguoi_choi", "diem_so", "ngay_choi")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings")
    
    tree.heading("id", text="ID")
    tree.heading("nguoi_choi", text="Người chơi")
    tree.heading("diem_so", text="Điểm")
    tree.heading("ngay_choi", text="Ngày chơi")

    tree.column("id", width=50, anchor="center")
    tree.column("nguoi_choi", width=150, anchor="w")
    tree.column("diem_so", width=100, anchor="center")
    tree.column("ngay_choi", width=180, anchor="center")

    # --- THAY ĐỔI 3: TRUY VẤN LỊCH SỬ TỪ GameHistory ---
    
    db_conn = db()
    query = """
        SELECT 
            H.history_id, 
            U.user_name, 
            H.score,
            DATE_FORMAT(H.game_date, '%Y-%m-%d %H:%i') AS ngay_choi
        FROM 
            GameHistory H
        JOIN 
            Users U ON H.user_id = U.user_id
        ORDER BY 
            H.game_date DESC
        LIMIT 20
    """
    
    df = db_conn.query(query)
    db_conn.close()

    if df.empty:
        tree.insert("", "end", values=("", "Chưa có lịch sử chơi", "", ""))
    else:
        # --- THAY ĐỔI 4: ĐỌC DỮ LIỆU TỪ DATAFRAME ---
        for index, row in df.iterrows():
            tree.insert("", "end", values=(
                row['history_id'], 
                row['user_name'], 
                row['score'],
                row['ngay_choi'] # Tên cột đã được đặt AS 'ngay_choi'
            ))

    tree.pack(expand=True, fill="both")