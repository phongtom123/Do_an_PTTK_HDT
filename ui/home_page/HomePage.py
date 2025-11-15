import tkinter as tk
from ui.home_page.sidebar_left import SidebarLeft
from ui.home_page.main_content import MainContentFrame

class HomePage(tk.Tk):
    """Giao diện chính gồm sidebar trái, nội dung chính, và sidebar phải"""
    def __init__(self, current_user):
        super().__init__()
        self.title("BLEU - Learning App")
        self.geometry("1400x800")
        self.state("zoomed")
        self.current_user = current_user
        self.configure(bg="#FFFFFF")

        # === Sidebar trái phải được pack TRƯỚC ===
        self.sidebar_left = SidebarLeft(self, None, current_user= current_user)
        self.sidebar_left.pack(side="left", fill="y")

        # === Nội dung chính ===
        self.main_content = MainContentFrame(self, current_user= current_user)
        self.main_content.pack(side="left", fill="both", expand=True)

        # Gán ngược lại tham chiếu cho sidebar
        self.sidebar_left.main_content = self.main_content


if __name__ == "__main__":
    from model.user import User
    user = User("thanh", "thanhbodoi") 
    app = HomePage(user)
    app.mainloop()
