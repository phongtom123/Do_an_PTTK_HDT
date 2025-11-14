import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# --- IMPORT DB ---
from db.db import db 

class Ranking(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")

        # (Phần Style và UI giữ nguyên)
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

        columns = ('rank', 'name', 'score')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')
        self.tree.heading('rank', text='Hạng', anchor="center")
        self.tree.column('rank', width=120, anchor="center", stretch=False)
        self.tree.heading('#0', text='', anchor="center")
        self.tree.column('#0', width=30, anchor="center", stretch=False)
        self.tree.heading('name', text='Tên', anchor="w")
        self.tree.column('name', width=160, anchor="w")
        self.tree.heading('score', text='Điểm Cao Nhất', anchor="center")
        self.tree.column('score', width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.tag_configure('top1', background='#FFD700', font=('Arial', 12, 'bold'))
        self.tree.tag_configure('top2', background='#C0C0C0', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('top3', background='#CD7F32', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('evenrow', background='#E8F5FF')

        self.avatar_images = []
        self.populate_ranking()

    def populate_ranking(self):
        """Hàm lấy BXH (điểm cao nhất) từ DB và chèn vào Treeview."""
        
        db_conn = db()
        
        # --- THAY ĐỔI: CẬP NHẬT CÂU TRUY VẤN SQL ---
        # Sửa tên bảng: GameHistory -> games
        # Sửa tên cột: H.user_id -> H.game_user_id
        query = """
            SELECT 
                U.user_name,
                MAX(H.score) AS highest_score
            FROM 
                games H
            JOIN 
                Users U ON H.game_user_id = U.user_id
            GROUP BY 
                U.user_id, U.user_name
            ORDER BY 
                highest_score DESC
            LIMIT 20
        """
        
        df = db_conn.query(query)
        db_conn.close()

        self.image_dir = "photos"
        icons = [] 

        if df.empty:
            self.tree.insert('', 'end', values=("", "Chưa có dữ liệu", ""))
            return

        # (Phần lặp và chèn dữ liệu giữ nguyên)
        for i, row in df.iterrows():
            name = row['user_name']
            score = row['highest_score'] 
            rank_index = i + 1
            
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