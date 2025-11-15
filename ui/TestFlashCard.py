import tkinter as tk
from tkinter import ttk, messagebox
from logic.deck_manager import DeckManager

FONT = "yu gothic ui"
BG = "#B1DDC6"
BG1 = "#1e293b"

class DeckManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deck Manager")
        self.root.geometry("500x400")
        self.root.config(bg="#04395E")
        self.root.state("zoomed")

        # === Kết nối tới logic ===
        self.deck_mngr = DeckManager()

        # === Giao diện ===
        self.title = tk.Label(
            root,
            text="Kho từ vựng (Flashcard Manager)",
            bg=BG1,
            fg="white",
            font=("Segoe UI", 18, "bold"),
        )
        self.title.place(relx=0.5, y=50, anchor="center")

        table_frame = tk.Frame(root, bg="white")
        table_frame.place(relx=0.5, y=420, anchor="center", width=1400, height=650)

        style = ttk.Style()
        style.configure("Treeview", background="#B1DDC6", foreground="black", rowheight=28)
        style.map("Treeview", background=[("selected", "#ddf4ff")])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Id", "Name", "Total", "Known", "Unknown", "Actions"),
            show="headings",
        )
        self.tree.heading("Id", text="ID")
        self.tree.heading("Name", text="Tên Deck")
        self.tree.heading("Total", text="Tổng số từ")
        self.tree.heading("Known", text="Đã nhớ")
        self.tree.heading("Unknown", text="Chưa nhớ")
        self.tree.heading("Actions", text="Thao tác")

        self.tree.column("Id", width=60, anchor="center")
        self.tree.column("Name", width=250, anchor="w")
        self.tree.column("Total", width=120, anchor="center")
        self.tree.column("Known", width=120, anchor="center")
        self.tree.column("Unknown", width=120, anchor="center")
        self.tree.column("Actions", width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # === Nút tạo deck mới ===
        tk.Button(
            root,
            text="➕ Tạo Deck mới",
            bg="#3b82f6",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            command=self.add_deck_popup,
        ).place(relx=0.5, y=800)

        # Tải dữ liệu ban đầu
        self.refresh_table()

    def refresh_table(self):
        """Tải lại danh sách deck và thống kê từ"""
        self.deck_mngr.get_deck_db()
        decks_df = self.deck_mngr.deck_df

        for row in self.tree.get_children():
            self.tree.delete(row)

        if decks_df is None or decks_df.empty:
            print("⚠️ Không có deck nào trong cơ sở dữ liệu.")
            return

        for _, row in decks_df.iterrows():
            deck_id = row["deck_id"]

            # Query đếm số từ
            q_total = f"SELECT COUNT(*) AS cnt FROM fc_Words WHERE word_deck_id = {deck_id};"
            q_known = f"SELECT COUNT(*) AS cnt FROM fc_Words WHERE word_deck_id = {deck_id} AND word_status = 1;"
            q_unknown = f"SELECT COUNT(*) AS cnt FROM fc_Words WHERE word_deck_id = {deck_id} AND word_status = 0;"

            total = int(self.deck_mngr._DeckManager__my_db.query(q_total).iloc[0, 0])
            known = int(self.deck_mngr._DeckManager__my_db.query(q_known).iloc[0, 0])
            unknown = int(self.deck_mngr._DeckManager__my_db.query(q_unknown).iloc[0,0])

            self.tree.insert(
                "",
                "end",
                values=(
                    deck_id,
                    row["deck_name"],
                    total,
                    known,
                    unknown,
                    "✏️  🗑️",
                ),
            )

        self.tree.bind("<Double-1>", self.handle_click)

    def handle_click(self, event):
        """Xử lý khi người dùng double-click"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            row_id = self.tree.identify_row(event.y)
            if not row_id:
                return
            values = self.tree.item(row_id, "values")
            deck_id = values[0]
            if col == "#6":
                self.show_action_menu(deck_id, event)

    def show_action_menu(self, deck_id, event):
        """Menu thao tác Sửa / Xóa"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="✏️  Sửa Deck", command=lambda: self.edit_deck(deck_id))
        menu.add_command(label="🗑️  Xóa Deck", command=lambda: self.delete_deck(deck_id))
        menu.tk_popup(event.x_root, event.y_root)

    def add_deck_popup(self):
        """Popup thêm deck"""
        popup = tk.Toplevel(self.root)
        popup.title("Tạo Deck mới")
        popup.geometry("300x180")
        popup.config(bg="#1e293b")

        tk.Label(popup, text="Tên Deck:", fg="white", bg="#1e293b").pack(pady=10)
        entry = tk.Entry(popup, width=30)
        entry.pack()

        def add():
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("Thiếu thông tin", "Hãy nhập tên deck.")
                return
            # giả định user_id = 2 (bạn có thể thay sau khi có hệ thống login)
            self.deck_mngr.add_deck_db(name, user_id=2)
            self.refresh_table()
            popup.destroy()

        tk.Button(popup, text="Thêm", bg="#3b82f6", fg="white", command=add).pack(pady=15)

    def edit_deck(self, deck_id):
        """Sửa tên deck"""
        popup = tk.Toplevel(self.root)
        popup.title("Sửa Deck")
        popup.geometry("300x180")
        popup.config(bg="#1e293b")

        tk.Label(popup, text="Tên Deck:", fg="white", bg="#1e293b").pack(pady=10)
        entry = tk.Entry(popup, width=30)
        entry.pack()

        def save_edit():
            new_name = entry.get().strip()
            if new_name:
                query = "UPDATE fc_Decks SET deck_name=%s WHERE deck_id=%s;"
                self.deck_mngr._DeckManager__my_db.dml_ddl_operator(query, (new_name, deck_id))
                self.refresh_table()
                popup.destroy()

        tk.Button(popup, text="Lưu", bg="#22c55e", fg="white", command=save_edit).pack(pady=15)

    def delete_deck(self, deck_id):
        """Xóa deck"""
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa deck ID={deck_id} không?")
        if confirm:
            self.deck_mngr.delete_deck_db(deck_id)
            self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeckManagerApp(root)
    root.mainloop()
