import tkinter as tk

class SidebarRight(tk.Frame):
    def __init__(self, root, user_name="Bạn", rank=0):
        super().__init__(root, bg="#FFFFFF", width=250)
        self.pack(side="right", fill="y", padx=(10, 20), pady=10)
        self._build_info(user_name, rank)

    def _build_info(self, user_name, rank):
        tk.Label(self, text=f"Xin chào {user_name}", bg="white", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self, text=f"Hạng: {rank}", bg="white", font=("Arial", 11)).pack()
