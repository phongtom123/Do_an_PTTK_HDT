import tkinter as tk
from .sidebar_left import SidebarLeft
from .sidebar_right import SidebarRight
from .main_content import MainContentFrame

# from unit_controller import get_all_units
from db.db import db

class HomePage:
    def __init__(self, window):
        self.root = window
        self.root.title("Trang chủ")
        self.root.geometry("1100x700")
        self.root.state("zoomed")
        self.root.update()
        self.root.configure(bg="#FFFFFF")

        # Lấy width, height
        height = self.root.winfo_height()
        width = self.root.winfo_width()

        # trạng thái
        self.current_mode = None
        self.in_learning_mode = False

        # giao diện chính
        self.sidebar_left = SidebarLeft(self.root, self)
        self.main_content = MainContentFrame(self.root)
        self.sidebar_right = SidebarRight(self.root)

        self.main_content.pack(side="left", fill="both", expand=True)

        # # hiển thị danh sách bài học ban đầu
        # self.show_lesson_list()

if __name__ == "__main__":
    window = tk.Tk()
    HomePage(window)
    window.mainloop()
    # -----------------
    # CHUYỂN VIEW
    # -----------------
    # def show_lesson_list(self):
    #     self.reset_sidebar()
    #     self.main_content.clear()
    #     self.main_content.show_lesson_list(get_all_units())

    # def show_mode(self, mode):
    #     self.current_mode = mode
    #     self.reset_sidebar()
    #     self.main_content.clear()

    #     if mode == "Reading":
    #         from reading_content import ReadingView
    #         ReadingView(self.root, self.main_content, self)
    #     elif mode == "Listening":
    #         from listening_content import ListeningView
    #         ListeningView(self.root, self.main_content, self)
    #     else:
    #         from lesson_content import LessonView
    #         LessonView(self.root, self.main_content, self)

    # def reset_sidebar(self):
    #     if hasattr(self, "sidebar_right"):
    #         self.sidebar_right.destroy()
    #     self.sidebar_right = SidebarRight(self.root)

    # def run(self):
    #     self.root.mainloop()

    # def get_all_units(self):
    #     pass