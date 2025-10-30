import tkinter as tk
from PIL import Image, ImageTk  # 🖼️ Thêm để xử lý ảnh
from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_learning import create_sidebar_learning
from controller.unit_controller import get_all_units


root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

# --------------------------------------
# 1) Tạo main_frame TRƯỚC nhưng KHÔNG pack
# --------------------------------------
main_frame = create_main_frame(root)

# --------------------------------------
# 2) Hàm show_in_main — Reading + Progress tách riêng
# --------------------------------------
def show_in_main(title, contents):
    for w in main_frame.winfo_children():
        w.destroy()

    readings = [
        "Reading 1:\n\nThe elephant is the largest land animal on Earth. It has a trunk, big ears, and thick grey skin. Elephants live in herds and are known for their intelligence and strong social bonds.",
        "Reading 2:\n\nThe cheetah is the fastest land animal. It can run up to 120 kilometers per hour in short bursts. Its spotted coat helps it blend in with the tall grass while hunting.",
        "Reading 3:\n\nThe penguin is a flightless bird that lives in cold regions like Antarctica. Although it cannot fly, it is an excellent swimmer and uses its wings to move through the water.",
        "Reading 4:\n\nThe dolphin is a friendly and intelligent marine mammal. Dolphins communicate through clicks and whistles, and they often travel together in groups called pods.",
        "Reading 5:\n\nThe panda is native to China and is known for its distinctive black-and-white fur. Pandas mainly eat bamboo and spend most of their day eating and resting."
    ]

    reading_index = 0

    # 🟩 FRAME chia bố cục
    progress_frame = tk.Frame(main_frame, bg="white", height=20)
    progress_frame.pack(fill="x", padx=20, pady=(15, 10))

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    button_frame = tk.Frame(main_frame, bg="white", height=70)
    button_frame.pack(fill="x", pady=(0, 15))

    # --------------------------------------
    # 🟩 THANH TIẾN ĐỘ
    # --------------------------------------
    BAR_HEIGHT = 10
    RADIUS = 100

    canvas = tk.Canvas(progress_frame, height=BAR_HEIGHT, bg="white", highlightthickness=0)
    canvas.place(relx=0.05, rely=0.1, relwidth=0.9)

    def create_round_rect(canvas, x1, y1, x2, y2, r=10, **kwargs):
        r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
        return [
            canvas.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x2-r*2, y1, x2, y1+r*2, start=0, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x2-r*2, y2-r*2, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x1, y2-r*2, x1+r*2, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs),
            canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)
        ]

    def draw_progress_bar(value):
        canvas.delete("bar", "bg")
        BAR_WIDTH = canvas.winfo_width()
        create_round_rect(canvas, 0, 0, BAR_WIDTH, BAR_HEIGHT, r=RADIUS, fill="#E0E0E0", outline="", tags="bg")

        width = (BAR_WIDTH / 100) * value
        if value > 0:
            create_round_rect(canvas, 0, 0, width, BAR_HEIGHT, r=RADIUS, fill="#4CAF50", outline="", tags="bar")

    # --------------------------------------
    # 📖 TIÊU ĐỀ + ẢNH
    # --------------------------------------
    title_frame = tk.Frame(content_frame, bg="white")
    title_frame.pack(pady=(5, 10))

    try:
        img = Image.open("./photos/Tiger.png")  # 🖼️ Ảnh của bạn (đường dẫn tùy chỉnh)
    except:
        img = Image.new("RGB", (40, 40), "#4CAF50")

    img = img.resize((150, 100), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(title_frame, image=photo, bg="white")
    img_label.image = photo
    img_label.pack(side="left", padx=(0, 10))

    title_label = tk.Label(
        title_frame,
        text="📖 Reading Practice",
        font=("Arial", 16, "bold"),
        bg="white"
    )
    title_label.pack(side="left")

    # --------------------------------------
    # 🟦 VÙNG NỘI DUNG
    # --------------------------------------
    text_box = tk.Text(
        content_frame,
        wrap="word",
        font=("Arial", 13),
        bg="#F8F9FA",
        relief="flat",
        padx=20,
        pady=10,
        height=15
    )
    text_box.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    def update_reading():
        text_box.delete("1.0", "end")
        text_box.insert("1.0", readings[reading_index])

    update_reading()

    # --------------------------------------
    # 🟨 NÚT Ở DƯỚI CÙNG + TIẾN ĐỘ
    # --------------------------------------
    def calc_progress():
        if len(readings) == 1:
            return 100
        return int((reading_index / (len(readings) - 1)) * 100)

    def update_reading_and_progress():
        text_box.delete("1.0", "end")
        text_box.insert("1.0", readings[reading_index])
        draw_progress_bar(calc_progress())

    def increase_progress():
        nonlocal reading_index
        if reading_index < len(readings) - 1:
            reading_index += 1
            update_reading_and_progress()
        else:
            draw_progress_bar(100)

    def decrease_progress():
        nonlocal reading_index
        if reading_index > 0:
            reading_index -= 1
            update_reading_and_progress()

    canvas.bind("<Configure>", lambda e: draw_progress_bar(calc_progress()))

    tk.Button(
        button_frame,
        text="Quay về",
        command=decrease_progress,
        bg="#f44336",
        fg="white",
        font=("Arial", 12, "bold"),
        width=10
    ).pack(side="left", padx=80, pady=10)

    tk.Button(
        button_frame,
        text="Tiếp theo",
        command=increase_progress,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        width=10
    ).pack(side="right", padx=80, pady=10)

    draw_progress_bar(calc_progress())

# --------------------------------------
# 3) Sidebar trái & phải
# --------------------------------------
create_sidebar_left(root, show_in_main)
create_sidebar_learning(root)

# --------------------------------------
# 4) Hiển thị main_frame
# --------------------------------------
main_frame.pack(side="left", fill="both", expand=True)

# --------------------------------------
# 5) Mặc định hiển thị
# --------------------------------------
show_in_main("", [])

root.mainloop()
