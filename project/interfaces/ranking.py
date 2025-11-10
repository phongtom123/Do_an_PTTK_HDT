import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class Ranking(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")

        # --- Cấu hình Style ---
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

        # --- Cấu hình Treeview ---
        # Ta hiển thị thêm cột '#0' để có thể hiện ảnh giữa các cột
        columns = ('rank', 'name', 'score')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')

        # Thứ tự mong muốn: Hạng | Ảnh | Tên | Điểm
        self.tree.heading('rank', text='Hạng', anchor="center")
        self.tree.column('rank', width=120, anchor="center", stretch=False)

        self.tree.heading('#0', text='', anchor="center")  # Hiện tiêu đề "Ảnh"
        self.tree.column('#0', width=30, anchor="center", stretch=False)

        self.tree.heading('name', text='Tên', anchor="w")
        self.tree.column('name', width=160, anchor="w")

        self.tree.heading('score', text='Điểm Số', anchor="center")
        self.tree.column('score', width=100, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # --- Cấu hình Tags ---
        self.tree.tag_configure('top1', background='#FFD700', font=('Arial', 12, 'bold'))
        self.tree.tag_configure('top2', background='#C0C0C0', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('top3', background='#CD7F32', font=('Arial', 11, 'bold'))
        self.tree.tag_configure('evenrow', background='#E8F5FF')

        # --- Lưu ảnh để tránh bị thu hồi ---
        self.avatar_images = []

        # --- Nạp dữ liệu ---
        self.populate_ranking()

    def populate_ranking(self):
        """Hàm tạo dữ liệu và chèn vào Treeview."""
        base_data = [
            ("Lê Minh An", "99"),
            ("Trần Tuấn Bình", "96"),
            ("Nguyễn Phương Chi", "94"),
        ]
        
        self.image_dir = "photos"
        # icons = ["🥇", "🥈", "🥉"]  # Gắn icon cho top bảng xếp hạng
        icons = []

        for i in range(20):  # 20 hàng
            name, score = base_data[i % len(base_data)]
            rank_index = i + 1

            if rank_index <= len(icons):
                rank_text = f"{icons[i]} Top {rank_index}"
            else:
                rank_text = f"Top {rank_index}"

            # Chọn tag màu
            tags = ()
            if i == 0:
                tags = ('top1',)
            elif i == 1:
                tags = ('top2',)
            elif i == 2:
                tags = ('top3',)
            elif i % 2 != 0:
                tags = ('evenrow',)

            # Thêm ảnh
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
                print(f"Lỗi: Không tìm thấy ảnh tại '{image_path}'")
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score),
                                 tags=tags)

