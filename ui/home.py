from tkinter import *
from PIL import Image, ImageTk

ASSETS_ROOT = "../assets/"
HEIGHT = 600
WIDTH = 800

BACKGROUND_COLOR = "#ffffff"
FONT = ""

# Window
window = Tk()
window.minsize(width=WIDTH, height=HEIGHT)
# window.resizable(False, False)
window.title("App học tiếng anh")
window.config(padx=10, 
              pady=10,
              bg="#ffffff")


###### Logo
canvas = Canvas(highlightthickness=0, bg=BACKGROUND_COLOR, height=150, width= 200)

# # Thu nhỏ logo
logo = Image.open(ASSETS_ROOT + "logo_blue.png")
resized_logo = logo.resize((200,150), Image.Resampling.LANCZOS)

logo_img = ImageTk.PhotoImage(resized_logo)
canvas.create_image(0,0, image= logo_img, anchor="nw")
canvas.grid(column=0, row = 0, sticky="NSEW")

# ##### Home canvas
home_canvas = Canvas(highlightthickness = 0, height=90, width=200)
home_icon = Image.open(ASSETS_ROOT + "icons/home.png")
resized_home_icon = home_icon.resize((45,45),Image.Resampling.LANCZOS )
home_icon = ImageTk.PhotoImage(resized_home_icon)

home_canvas.create_image(50, 45, image=home_icon)
home_canvas.create_text(140, 45, text="Learn", font=("Sans-serif", 15))
home_canvas.grid(column=0, row=1, sticky="NSEW")


# ##### Flashcard canvas
flashcard_canvas = Canvas(highlightthickness = 0, height=90, width=200)
flashcard_icon = Image.open(ASSETS_ROOT + "icons/flashcard.png")
resized_flashcard_icon = flashcard_icon.resize((45,45),Image.Resampling.LANCZOS )
flashcard_icon = ImageTk.PhotoImage(resized_flashcard_icon)

flashcard_canvas.create_image(50, 45, image=flashcard_icon)
flashcard_canvas.create_text(140, 45, text="Flashcard", font=("Sans-serif", 15))
flashcard_canvas.grid(column=0, row=2, sticky="NSEW")

# ##### Game canvas
game_canvas = Canvas(highlightthickness = 0, height=90, width=200)
game_icon = Image.open(ASSETS_ROOT + "icons/competition.png")
resized_game_icon = game_icon.resize((45,45),Image.Resampling.LANCZOS )
game_icon = ImageTk.PhotoImage(resized_game_icon)

game_canvas.create_image(50, 45, image=game_icon)
game_canvas.create_text(140, 45, text="Game", font=("Sans-serif", 15))
game_canvas.grid(column=0, row=3, sticky="NSEW")

# ##### Rank canvas
rank_canvas = Canvas(highlightthickness = 0, height=90, width=200)
rank_icon = Image.open(ASSETS_ROOT + "icons/ranking.png")
resized_rank_icon = rank_icon.resize((45,45),Image.Resampling.LANCZOS )
rank_icon = ImageTk.PhotoImage(resized_rank_icon)

rank_canvas.create_image(50, 45, image=rank_icon)
rank_canvas.create_text(140, 45, text="Game", font=("Sans-serif", 15))
rank_canvas.grid(column=0, row=4, sticky="NSEW")

# ##### Profile canvas
profile_canvas = Canvas(highlightthickness = 0, height=90, width=200)
profile_icon = Image.open(ASSETS_ROOT + "icons/avatar.png")
resized_profile_icon = profile_icon.resize((45,45),Image.Resampling.LANCZOS )
profile_icon = ImageTk.PhotoImage(resized_profile_icon)

profile_canvas.create_image(50, 45, image=profile_icon)
profile_canvas.create_text(140, 45, text="Profile", font=("Sans-serif", 15))
profile_canvas.grid(column=0, row=5, sticky="NSEW")

# # Unit 1
button_1 = Button(text="Unit 1",  # Nội dung
                bg="#1cb0f6",      # Màu nền xanh lá
                fg="white",        # Màu chữ trắng
                font=("Arial", 16, "bold"),  # Font to, đậm
                relief="raised",   # Viền nổi (raised, sunken, flat, groove, ridge)
                bd=5,              # Độ dày viền 5px
                activebackground="#45a049",  # Màu khi hover
                activeforeground="white",    # Màu chữ khi hover
                width=45,
                anchor=CENTER
)
button_1.grid(column=1, row = 0)

button_2 = Button(text="Unit 2",  # Nội dung
                bg="#58cc02",      # Màu nền xanh lá
                fg="white",        # Màu chữ trắng
                font=("Arial", 16, "bold"),  # Font to, đậm
                relief="raised",   # Viền nổi (raised, sunken, flat, groove, ridge)
                bd=5,              # Độ dày viền 5px
                activebackground="#45a049",  # Màu khi hover
                activeforeground="white",    # Màu chữ khi hover
                width=45,
                anchor=CENTER
)
button_2.grid(column=1, row=1)

button_3 = Button(text="Unit 3",  # Nội dung
                bg="#ffc800",      # Màu nền xanh lá
                fg="white",        # Màu chữ trắng
                font=("Arial", 16, "bold"),  # Font to, đậm
                relief="raised",   # Viền nổi (raised, sunken, flat, groove, ridge)
                bd=5,              # Độ dày viền 5px
                activebackground="#45a049",  # Màu khi hover
                activeforeground="white",    # Màu chữ khi hover
                width=45,
                anchor=CENTER
)
button_3.grid(column=1, row=2, sticky="w")
window.mainloop()