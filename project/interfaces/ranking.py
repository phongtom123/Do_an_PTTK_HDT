import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# --- THAY ĐỔI 1: IMPORT CLASS 'db' TỪ FILE db.py ---
from db.db import db 

class Ranking(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")

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

        tk.Label(self, text="🏆 BẢNG XẾP HẠNG 🏆",
                 font=("Arial", 22, "bold"), bg="#f0f0f0").pack(pady=20)
        
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Cấu hình Treeview (Giữ nguyên) ---
        columns = ('rank', 'name', 'score')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')

        self.tree.heading('rank', text='Hạng', anchor="center")
        self.tree.column('rank', width=120, anchor="center", stretch=False)

        self.tree.heading('#0', text='', anchor="center")
        self.tree.column('#0', width=30, anchor="center", stretch=False)

        self.tree.heading('name', text='Tên', anchor="w")
        self.tree.column('name', width=160, anchor="w")

        # --- THAY ĐỔI 2: Sửa tiêu đề cột điểm ---
        self.tree.heading('score', text='Điểm Cao Nhất', anchor="center")
        self.tree.column('score', width=120, anchor="center") # Cho cột rộng hơn 1 chút

        self.tree.pack(side="left", fill="both", expand=True)

        # --- Cấu hình Tags (Giữ nguyên) ---
        self.tree.tag_configure('top1', background='#FFD700', font=('Arial', 12, 'bold'))
        self.tree.tag_configure('top2', background='#C0C0C0', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('top3', background='#CD7F32', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('evenrow', background='#E8F5FF')

        # --- Lưu ảnh để tránh bị thu hồi ---
        self.avatar_images = []

        # --- Nạp dữ liệu ---
        self.populate_ranking()

    # --- THAY ĐỔI 3: VIẾT LẠI HÀM ĐỂ LẤY DỮ LIỆU THẬT ---
    def populate_ranking(self):
        """Hàm lấy BXH (điểm cao nhất) từ GameHistory và chèn vào Treeview."""
        
        # 1. Kết nối và truy vấn DB
        db_conn = db()
        
        # --- THAY ĐỔI 4: CẬP NHẬT CÂU TRUY VẤN SQL ---
        # Lấy điểm MAX (cao nhất) của mỗi user từ GameHistory
        query = """
            SELECT 
                U.user_name,
                MAX(H.score) AS highest_score
            FROM 
                GameHistory H
            JOIN 
                Users U ON H.user_id = U.user_id
            GROUP BY 
                U.user_id, U.user_name
            ORDER BY 
                highest_score DESC
            LIMIT 20
        """
        
        df = db_conn.query(query)
        db_conn.close()

        # 2. Chuẩn bị thư mục ảnh (Giữ nguyên)
        self.image_dir = "photos"
        icons = [] 

        # 3. Kiểm tra nếu không có dữ liệu
        if df.empty:
            self.tree.insert('', 'end', values=("", "Chưa có dữ liệu", ""))
            return

        # 4. Lặp qua DataFrame (dữ liệu thật) và chèn vào bảng
        for i, row in df.iterrows():
            # --- THAY ĐỔI 5: CẬP NHẬT TÊN CỘT ĐỂ KHỚP VỚI TRUY VẤN ---
            name = row['user_name']
            score = row['highest_score'] # Lấy điểm cao nhất (thay vì user_rank)
            rank_index = i + 1
            
            # (Phần còn lại giữ nguyên)
            if rank_index <= len(icons):
                rank_text = f"{icons[i]} Top {rank_index}"
            else:
                rank_text = f"Top {rank_index}"

            tags = ()
            if i == 0:
                tags = ('top1',)
            elif i == 1:
                tags = ('top2',)
            elif i == 2:
                tags = ('top3',)
            elif i % 2 != 0:
                tags = ('evenrow',)

            image_file = 'avataaars.png'
            image_path = os.path.join(self.image_dir, image_file)

            try:
                img = Image.open(image_path).resize((30, 30), Image.Resampling.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                self.avatar_images.append(photo_img)
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score),
                                 image=photo_img,
                                 tags=tags)
            except FileNotFoundError:
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score),
                                 tags=tags)
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh: {e}")
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score),
                                 tags=tags)