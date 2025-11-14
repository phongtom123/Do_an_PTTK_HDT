import tkinter as tk
from tkinter import ttk
from db.db import db

# ==========================================================
# ===          CLASS TRANG LỊCH SỬ (HISTORYPAGE)         ===
# ==========================================================

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Cấu hình Style (Giữ nguyên) ---
        style = ttk.Style(self)
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
        self.config(bg="white")

        history_frame = tk.Frame(self, bg="white")
        history_frame.pack(expand=True, fill="both", pady=20, padx=50)

        # --- THAY ĐỔI 1: Sửa tiêu đề ---
        tk.Label(history_frame, text="Lịch sử Chơi Của Bạn", 
                 font=("Arial", 18, "bold"), 
                 bg="white").pack(pady=(10, 20))

        # --- THAY ĐỔI 2: Sửa các cột (Trả lại cột "Người chơi") ---
        columns = ("id", "nguoi_choi", "diem_so")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID Lượt Chơi")
        self.tree.heading("nguoi_choi", text="Người chơi") # Giữ "như cũ"
        self.tree.heading("diem_so", text="Điểm")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("nguoi_choi", width=200, anchor="w") # Giữ "như cũ"
        self.tree.column("diem_so", width=100, anchor="center")
        
        self.tree.pack(expand=True, fill="both")

        # --- Tải dữ liệu lần đầu ---
        self.refresh()

    def refresh(self):
        """Hàm này tải/tải lại dữ liệu từ DB, được gọi bởi controller."""
        
        # Xóa dữ liệu cũ trong bảng
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # --- THAY ĐỔI 3: Lấy user_id hiện tại từ controller ---
        current_user_id = self.controller.current_user_id
            
        # Tải dữ liệu mới
        db_conn = self.controller.db_class()
        
        # --- THAY ĐỔI 4: Cập nhật câu truy vấn (JOIN và WHERE) ---
        # (Lấy cả tên user và lọc theo ID)
        query = """
            SELECT 
                H.game_id, 
                U.user_name, 
                H.score
            FROM 
                games H
            JOIN 
                Users U ON H.game_user_id = U.user_id
            WHERE 
                H.game_user_id = %s
            ORDER BY 
                H.game_id DESC
            LIMIT 20
        """
        # Truyền user_id vào làm tham số
        df = db_conn.query(query, (current_user_id,))
        db_conn.close()

        if df.empty:
            # --- THAY ĐỔI 5: Cập nhật giá trị rỗng ---
            self.tree.insert("", "end", values=("Bạn chưa chơi lượt nào", "", ""))
        else:
            # --- THAY ĐỔI 6: Cập nhật cách đọc dữ liệu (3 cột) ---
            for index, row in df.iterrows():
                self.tree.insert("", "end", values=(
                    row['game_id'], 
                    row['user_name'], # Trả lại cột 'user_name'
                    row['score']
                ))