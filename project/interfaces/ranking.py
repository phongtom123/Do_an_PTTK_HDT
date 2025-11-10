import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from controller.user_controller import get_all_users  # ✅ lấy dữ liệu người dùng thật


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
        
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Cấu hình Treeview ---
        # ➕ Thêm cột 'finish_time'
        columns = ('rank', 'name', 'score', 'finish_time')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')

        # === Các tiêu đề cột ===
        self.tree.heading('rank', text='Hạng', anchor="center")
        self.tree.column('rank', width=100, anchor="center", stretch=False)

        self.tree.heading('#0', text='', anchor="center")  # cột ảnh
        self.tree.column('#0', width=40, anchor="center", stretch=False)

        self.tree.heading('name', text='Tên người dùng', anchor="w")
        self.tree.column('name', width=200, anchor="w")

        self.tree.heading('score', text='Điểm số', anchor="center")
        self.tree.column('score', width=100, anchor="center")

        self.tree.heading('finish_time', text='Thời gian hoàn thành', anchor="center")
        self.tree.column('finish_time', width=200, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # --- Tags cho các top ---
        self.tree.tag_configure('top1', background='#FFD700', font=('Arial', 12, 'bold'))  # vàng
        self.tree.tag_configure('top2', background='#C0C0C0', font=('Arial', 12, 'bold'))  # bạc
        self.tree.tag_configure('top3', background='#CD7F32', font=('Arial', 12, 'bold'))  # đồng
        self.tree.tag_configure('evenrow', background='#E8F5FF')  # hàng xen kẽ nhạt

        self.avatar_images = []  # tránh GC
        self.populate_ranking()

    def populate_ranking(self):
        """Hiển thị danh sách người dùng từ DB, sắp xếp theo rank."""
        users = get_all_users()

        # 🔽 Sắp xếp theo user_rank (cao nhất trước)
        users.sort(key=lambda u: u.get_user_rank(), reverse=True)

        if not users:
            self.tree.insert('', 'end', values=("Không có dữ liệu", "", "", ""), tags=())
            return

        # Thư mục chứa ảnh
        self.image_dir = "photos"
        image_file = "avataaars.png"

        for i, user in enumerate(users, start=1):
            name = user.get_user_name()
            score = user.get_user_rank()  # dùng rank làm điểm
            rank_text = f"Top {i}"

            # ✅ Nếu bạn có thời gian hoàn thành thật từ DB, có thể lấy:
            # finish_time = user.get_finish_time()
            # Nếu chưa có, ta hiển thị tạm thời là None hoặc chuỗi mô phỏng
            finish_time = getattr(user, "finish_time", "—")

            # --- Tag màu theo thứ hạng ---
            if i == 1:
                tags = ('top1',)
            elif i == 2:
                tags = ('top2',)
            elif i == 3:
                tags = ('top3',)
            elif i % 2 == 0:
                tags = ('evenrow',)
            else:
                tags = ()

            # --- Ảnh đại diện ---
            image_path = os.path.join(self.image_dir, image_file)
            try:
                img = Image.open(image_path).resize((30, 30), Image.Resampling.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                self.avatar_images.append(photo_img)
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score, finish_time),
                                 image=photo_img,
                                 tags=tags)
            except FileNotFoundError:
                print(f"Lỗi: Không tìm thấy ảnh tại '{image_path}'")
                self.tree.insert('', 'end',
                                 values=(rank_text, name, score, finish_time),
                                 tags=tags)
