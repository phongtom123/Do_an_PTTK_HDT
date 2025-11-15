import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from logic.deck.DeckManager import DeckManager

BACKGROUND_COLOR = "#B1DDC6"
FLIP_TIMER = 3000

current_path = os.path.dirname(__file__)
current_card = {}


class FlashcardReview(tk.Frame):
    def __init__(self, master, user_id, deck_id):
        super().__init__(master, bg=BACKGROUND_COLOR)
        
        # setup
        self.user_id = user_id
        self.deck_id = deck_id
        self.card_deck = self.populate_card()


        self.flip_timer = self.after(FLIP_TIMER, self.flip_card) # after tự gọi hàm sau 3s
        self.master.state("zoomed")
        self.card_title = tk.StringVar(value="default")
        self.card_word = tk.StringVar(value="default")

        # Tạo canvas
        self.canvas = tk.Canvas(self, width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.canvas.place(relx=0.5, rely=0.4, anchor="center")

        # Tải hình
        self.card_front_img = Image.open(os.path.join(current_path, "../../assets/flash_card/card_front.png"))
        self.card_front_photo = ImageTk.PhotoImage(self.card_front_img)

        self.card_back_img = Image.open((os.path.join(current_path, "../../assets/flash_card/card_back.png")))
        self.card_back_photo = ImageTk.PhotoImage(self.card_back_img)

        # Hình nền flashcard
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_photo)

        # Text
        self.card_title = self.canvas.create_text(
            400, 150,
            text=self.card_title.get(),
            font=("Ariel", 40, "italic")
        )

        self.card_word = self.canvas.create_text(
            400, 270,
            text=self.card_word.get(),
            font=("Ariel", 60, "bold")
        )

        # Button
        self.btn_frame = tk.Frame(self, background= BACKGROUND_COLOR)
        self.btn_frame.place(in_=self.canvas, relx=0.5, rely=1.1, anchor="n") # in_ để tương đối với canvas
        
        # Nút quay lại từ trước
        self.left_arrow_img = Image.open(os.path.join(current_path,"../../assets/flash_card/left_arrow.png")).resize((100,100))
        self.left_arrow_photo = ImageTk.PhotoImage(self.left_arrow_img)
        tk.Button(
            self.btn_frame,
            image= self.left_arrow_photo,
            font=("Arial", 14, "bold"),
            bg=BACKGROUND_COLOR,
            fg=BACKGROUND_COLOR,
            padx=20,
            highlightthickness= 0,
            bd = 0,
            command=self.next_card
        ).pack(side="left", padx=20)
        
        # Nút mark là chưa nhớ
        self.unkhown_btn_icon =  Image.open(os.path.join(current_path,"../../assets/flash_card/unknown_btn_icon.png")).resize((100,100))
        self.unkhown_btn_photo = ImageTk.PhotoImage(self.unkhown_btn_icon)
        tk.Button(
            self.btn_frame,
            image = self.unkhown_btn_photo,
            font=("Arial", 14, "bold"),
            bg=BACKGROUND_COLOR,
            fg=BACKGROUND_COLOR,
            padx=20,
            highlightthickness= 0,
            bd = 0,
            command=self.flip_card
        ).pack(side="left", padx=20)

        # Nút mark là đã nhớ
        self.khown_btn_icon = Image.open(os.path.join(current_path,"../../assets/flash_card/known_btn_icon.png")).resize((100,100))
        self.khown_btn_photo = ImageTk.PhotoImage(self.khown_btn_icon)
        tk.Button(
            self.btn_frame,
            image= self.khown_btn_photo,
            font=("Arial", 14, "bold"),
            bg=BACKGROUND_COLOR,
            fg=BACKGROUND_COLOR,
            padx=20,
            command=self.flip_card,
            highlightthickness= 0,
            bd = 0
        ).pack(side="left", padx=20)

        # Nút chuyển đến từ tiếp theo
        self.right_arrow_img = Image.open(os.path.join(current_path,"../../assets/flash_card/right_arrow.png")).resize((100,100))
        self.right_arrow_photo = ImageTk.PhotoImage(self.right_arrow_img)
        tk.Button(
            self.btn_frame,
            image= self.right_arrow_photo,
            font=("Arial", 14, "bold"),
            bg=BACKGROUND_COLOR,
            fg=BACKGROUND_COLOR,
            padx=20,
            highlightthickness= 0,
            bd = 0,
            command=self.flip_card
        ).pack(side="left", padx=20)
    
    
    # ============ LOGIC ======================

    def populate_card(self):
        '''Lấy ra danh sách card chưa nhớ của deck_id'''
        deck_mgr = DeckManager(user_id= self.user_id)
        current_deck = deck_mgr.find_deck(deck_id= self.deck_id)
        return current_deck.filter_card(status = 0)

    def next_card(self):
        """Load từ tiếp theo (demo: thay text tạm)"""
        self.canvas.itemconfig(self.card_title, text="New Title")
        self.canvas.itemconfig(self.card_word, text="New Word")

    def flip_card(self):
        self.canvas.itemconfig(self.card_title, text="Tiếng Việt", fill="white")
        self.canvas.itemconfig(self.card_word, text=current_card["Tiếng Việt"], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Flashcard Test")
    window.geometry("900x700")

    # user_id = 2
    # deck_id = 1 (bạn sửa theo deck thật)
    frame = FlashcardReview(window, 2, 1)
    frame.pack(fill="both", expand=True)

    window.mainloop()
