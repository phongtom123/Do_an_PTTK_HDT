import tkinter as tk
from PIL import Image, ImageTk
import pandas, os
import random

BACKGROUND_COLOR = "#B1DDC6"
current_path = os.path.dirname(__file__)
current_card = {}
to_learn = {}

# try:
#     data = pandas.read_csv("data/words.csv")
# except FileNotFoundError:
#     original_data = pandas.read_csv("data/words.csv")
#     print(original_data)
#     to_learn = original_data.to_dict(orient="records")
# else:
#     to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

class FlashCardForm():
    def __init__(self, window):
        # setup
        self.window = window
        self.window.title("Flashcard")
        self.window.geometry("1166x718")
        self.window.state("zoomed") # Phóng to full màn hình, giống ấn ô vuông
        self.window.update()

        height = self.window.winfo_height()
        width = self.window.winfo_width()
        print(f"{width}x{height}")

        self.window.resizable(False, False) # Chú ý tắt resize sau khi đã chỉnh size\
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        
        # =================== Start menu =========
        menu = tk.Menu()
        self.window.config(menu = menu)
        menu.add_command(label="Tạo flashcard" )
        menu.add_command(label="Select Set")
        menu.add_command(label="Learn Mode")
        # =================End menu===============
        # layout setup
        # self.window.rowconfigure()
        # self.window.columnconfigure()
        # ========Start canvas================
        self.canvas = tk.Canvas(width=800, height=526)
        self.canvas.config(
            highlightthickness= 0,
        )
        # card front
        self.card_front_img = Image.open(current_path + "/../assets/flash_card/card_front.png")
        photo = ImageTk.PhotoImage(self.card_front_img) # Tạo imagetk
        
        self.card_background = self.canvas.create_image(400, 263, image=photo)
        self.canvas.place(relx=0.5, rely=0.4, anchor= "center")

        self.card_title = self.canvas.create_text(
            400, 150, 
            text="English", 
            font=("Ariel", 40, "italic")
        )
        self.card_word = self.canvas.create_text(
            400, 270, 
            text="こんにちは", 
            font=("Ariel", 60, "bold"))
        # ========End canvas================== 

        # ========Start unknown btn===========
        cross_image = Image.open(current_path + "/../assets/flash_card/wrong.png")
        photo = ImageTk.PhotoImage(cross_image)
        cross_image = photo
        unknown_button = tk.Button(image=cross_image, highlightthickness=0, command=next_card)
        unknown_button.place(x=400, y=700, anchor="center")
        # ========End uknown btn==========        

if __name__ == "__main__":
    window = tk.Tk()
    FlashCardForm(window)
    window.mainloop()

# flip_timer = window.after(3000, func=flip_card)

# canvas = tk.Canvas(width=800, height=526)
# card_front_img = PhotoImage(file= current_path + "/../assets/flash_card/card_front.png")
# card_back_img = PhotoImage(file= current_path + "/../assets/flash_card/card_back.png")
# card_background = canvas.create_image(400, 263, image=card_front_img)
# card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
# card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
# canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# canvas.grid(row=0, column=0, columnspan=2)

# cross_image = PhotoImage(file= current_path + "/../assets/flash_card/wrong.png")
# unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
# unknown_button.grid(row=1, column=0)

# check_image = PhotoImage(file= current_path + "/../assets/flash_card/right.png")
# known_button = Button(image=check_image, highlightthickness=0, command=is_known)
# known_button.grid(row=1, column=1)



