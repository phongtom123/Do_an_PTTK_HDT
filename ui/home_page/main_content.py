import tkinter as tk

class MainContentFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="white")

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_lesson_list(self, units):
        for i, unit in enumerate(units, start=1):
            tk.Label(self, text=f"Unit {i}: {unit[1]}", bg="white", font=("Arial", 12)).pack(anchor="w", padx=30, pady=10)
