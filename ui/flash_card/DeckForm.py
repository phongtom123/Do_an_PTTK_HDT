import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from logic.deck.DeckManager import DeckManager

class DeckList(tk.Frame):
    def __init__(self, master, user_id):
        super().__init__(master, bg="#f0f0f0")
        self.user_id = user_id.get_user_id()
        
        # ===========Tiêu đề=========
        header = tk.Label(
            self,
            text="📚 Danh sách Deck từ vựng",
            font=("Arial", 20, "bold"),
            bg="#1e3a8a",
            fg="white",
            pady=12
        )
        header.pack(fill="x")

        # --- Style Treeview ---
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading",
            font=("Arial", 14, "bold"),
            background="#2c3e50",
            foreground="white",
            relief="flat"
        )
        style.map("Treeview.Heading", background=[('active', '#34495e')])
        style.configure(
            "Treeview",
            highlightthickness=0,
            bd=0,
            font=('Arial', 12),
            rowheight=45,
            fieldbackground="#ffffff"
        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # --- Frame chứa bảng ---
        tree_frame = tk.Frame(self, bg="#f0f0f0")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Định nghĩa cột ---
        columns = ('stt', 'name', 'total', 'known', 'unknown', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        self.tree.heading('stt', text='Stt', anchor="center")
        self.tree.column('stt', width=40, anchor="center", stretch=False)

        # self.tree.heading('id', text='Stt', anchor="center")
        # self.tree.column('id', width=80, anchor="center")

        self.tree.heading('name', text='Tên Deck', anchor="w")
        self.tree.column('name', width=280, anchor="w")

        self.tree.heading('total', text='Tổng số từ', anchor="center")
        self.tree.column('total', width=140, anchor="center")

        self.tree.heading('known', text='Đã nhớ', anchor="center")
        self.tree.column('known', width=120, anchor="center")

        self.tree.heading('unknown', text='Chưa nhớ', anchor="center")
        self.tree.column('unknown', width=120, anchor="center")

        # self.tree.heading('status', text='Trạng thái', anchor="center")
        # self.tree.column('status', width=150, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")




        #==== Tag màu xen kẽ ===
        self.tree.tag_configure('active', background='#E8F5FF', font=('Arial', 12, 'bold'))
        self.tree.tag_configure('inactive', background='#FFEBEE', font=('Arial', 12))
        self.tree.tag_configure('evenrow', background='#F5F5F5')

        # Load dữ liệu
        self.populate_decks()


    # ===============LOGIC +===========
    def populate_decks(self):
        """Lấy danh sách deck và hiển thị"""
        deck_mngr = DeckManager(self.user_id)

        # Xóa bảng cũ
        for row in self.tree.get_children():
            self.tree.delete(row)

        if deck_mngr.is_deck_list_empty():
            self.tree.insert('', 'end', values=("Không có deck nào", "", "", "", "", ""), tags=())
            return

        for i,deck in enumerate(deck_mngr.deck_list):
            deck_id = deck.get_deck_id()
            deck_name = deck.get_deck_name()

            # Đếm từ trong mỗi deck
            total = deck.count_total_card()
            known = deck.count_known_card() 
            unknown = deck.count_unknown_card()

            # Nếu đã học hết thì đổi màu
            deck_status = ''
            if known == total:
                tag = "inactive"
                deck_status = 1
            else:
                tag = "active"
                # deck_status = 'Chưa hoàn thành'
                deck_status = 0
            if i % 2 == 0:
                tag = 'evenrow'

            # Insert dữ liệu ra bảng
            self.tree.insert(
                '',
                'end',
                values=(i+1, deck_name, total, f"{known}/{total}", f"{unknown}/{total}", deck_status),
                tags=(tag,)
            )

if __name__ == "__main__":
    from logic.user.UserManager import UserManager
    root = tk.Tk()
    root.title("Danh sách Deck")
    root.geometry("900x600")
    user_mgr = UserManager()
    thanh_user = user_mgr.auth("thanh", "thanhbodoi")
    frame = DeckList(root, thanh_user)
    frame.pack(fill="both", expand=True)
    root.mainloop()
