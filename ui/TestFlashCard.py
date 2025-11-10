import tkinter as tk
from tkinter import ttk, messagebox


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

        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

        # ====== Sample Data ======
        self.decks = [
            {"name": "Spanish Basics", "words": 15},
            {"name": "Animals", "words": 8},
            {"name": "Fruits", "words": 10},
        ]

        # ====== Start title ===========
        self.title = tk.Label(
            root,
            text="Kho từ vựng",
            bg=BG1,
            fg="white",
            font=("Segoe UI", 18, "bold"),
        )
        self.title.place(relx=0.5, y=50, anchor= "center")
        # =========End title==============

        # =========Start table=============
        
        #Frame
        table_frame = tk.Frame(root, bg="white")
        table_frame.place(
            relx=0.5, 
            y=420, 
            anchor="center",
            width= 1400,
            height=650
        )

        # ====== Treeview ======
        style = ttk.Style()
        style.configure("Treeview", background="#B1DDC6", foreground="black", fieldbackground="#0f172a", rowheight=28)
        style.map("Treeview", background=[("selected", "#ddf4ff")])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Id", "Name", "Count","KnownCount", "UnknownCount", "Actions"),
            show="headings",
        )
        self.tree.heading("Id", text="Số thứ tự") # Id noi bo khac voi text hien thi ra user
        self.tree.heading("Name", text="Tên Deck")
        self.tree.heading("Count", text="Số từ")
        self.tree.heading("KnownCount", text="Số từ đã nhớ")
        self.tree.heading("UnknownCount", text="Số từ chưa nhớ")
        self.tree.heading("Actions", text="Thao tác")

        self.tree.column("Id", width=60, anchor="center", minwidth=60, stretch=False)
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Count", width=80, anchor="center")
        self.tree.column("KnownCount", width=80, anchor="center")
        self.tree.column("UnknownCount", width=80, anchor="center")

        self.tree.column("Actions", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # ====== Button Add Deck ======
        tk.Button(
            root,
            text="➕ Tạo Deck mới",
            bg="#3b82f6",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            command=self.add_deck_popup,
        )
        # .pack(pady=5)

        self.refresh_table()

    def refresh_table(self):
        """Hiển thị lại danh sách deck"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, deck in enumerate(self.decks, start=1):
            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    deck["name"],
                    deck["words"],
                    "✏️  🗑️"
                ),
            )

        # Gắn sự kiện click
        self.tree.bind("<Double-1>", self.handle_click)

    def handle_click(self, event):
        """Nhận biết cột bấm vào"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            row_id = self.tree.identify_row(event.y)
            if not row_id:
                return
            index = int(self.tree.item(row_id, "values")[0]) - 1

            if col == "#4":  # Cột "Thao tác"
                self.show_action_menu(index, event)

    def show_action_menu(self, index, event):
        """Hiện menu popup Edit/Delete"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="✏️  Sửa Deck", command=lambda: self.edit_deck(index))
        menu.add_command(label="🗑️  Xóa Deck", command=lambda: self.delete_deck(index))
        menu.tk_popup(event.x_root, event.y_root)

    def add_deck_popup(self):
        """Popup thêm deck mới"""
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
            self.decks.append({"name": name, "words": 0})
            self.refresh_table()
            popup.destroy()

        tk.Button(popup, text="Thêm", bg="#3b82f6", fg="white", command=add).pack(pady=15)

    def edit_deck(self, index):
        deck = self.decks[index]
        popup = tk.Toplevel(self.root)
        popup.title("Sửa Deck")
        popup.geometry("300x180")
        popup.config(bg="#1e293b")

        tk.Label(popup, text="Tên Deck:", fg="white", bg="#1e293b").pack(pady=10)
        entry = tk.Entry(popup, width=30)
        entry.insert(0, deck["name"])
        entry.pack()

        def save_edit():
            new_name = entry.get().strip()
            if new_name:
                deck["name"] = new_name
                self.refresh_table()
                popup.destroy()

        tk.Button(popup, text="Lưu", bg="#22c55e", fg="white", command=save_edit).pack(pady=15)

    def delete_deck(self, index):
        deck_name = self.decks[index]["name"]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{deck_name}' không?")
        if confirm:
            del self.decks[index]
            self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeckManagerApp(root)
    root.mainloop()
