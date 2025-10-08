# sidebar_right.py
import tkinter as tk

def create_sidebar_right(root):
    sidebar = tk.Frame(root, bg="#FFFFFF", width=220)
    sidebar.pack(side="right", fill="y", padx=(10,20), pady=10)
    sidebar.pack_propagate(False)

    def create_card(parent, title, options):
        outer = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#e0e0e0", highlightthickness=1, bd=0)
        outer.pack(pady=10, padx=10, fill="x")
        card = tk.Frame(outer, bg="white", bd=0)
        card.pack(padx=3, pady=3, fill="x")
        tk.Label(card, text=title, font=("Arial",12,"bold"), bg="white").pack(pady=(10,5), padx=10)
        for opt in options:
            tk.Button(card, text=opt, font=("Arial",11), bg="#3498db", fg="white", bd=0, activebackground="#2980b9").pack(fill="x", padx=10, pady=5)
        return outer

    create_card(sidebar, "🔥 Streak", ["Chuỗi 5 ngày", "Thưởng hôm nay"])
    create_card(sidebar, "🏆 Bảng xếp hạng", ["Top 1: Nam","Top 2: Linh"])
    return sidebar
