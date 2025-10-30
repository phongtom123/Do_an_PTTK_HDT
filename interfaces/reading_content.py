import tkinter as tk
from PIL import Image, ImageTk
from sidebar_learning import create_sidebar_learning


def show_reading_practice(root, main_frame, sidebar_right_ref,
                          recreate_sidebar_right, show_in_main, in_reading_mode):
    """
    Hiển thị giao diện Reading Practice.
    Khi nhấn 'Thoát Unit' → quay lại danh sách Reading và phục hồi sidebar_right.
    Khi nhấn 'Quay về' → lùi thanh tiến độ.
    """
    in_reading_mode[0] = True  # ✅ bật cờ trạng thái học

    # 🧹 1. Xóa nội dung main hiện tại
    for w in main_frame.winfo_children():
        w.destroy()

    # 🧹 2. Hủy sidebar_right cũ
    if sidebar_right_ref[0] is not None:
        try:
            sidebar_right_ref[0].pack_forget()
            sidebar_right_ref[0].destroy()
        except Exception:
            pass
        sidebar_right_ref[0] = None
    root.update_idletasks()

    # 🧩 3. Tạo sidebar_learning mới thay thế
    sidebar_learning = create_sidebar_learning(root)
    sidebar_right_ref[0] = sidebar_learning

    # 📖 4. Dữ liệu Reading mẫu
    readings = [
        "Reading 1:\n\nThe elephant is the largest land animal...",
        "Reading 2:\n\nThe cheetah is the fastest land animal...",
        "Reading 3:\n\nThe penguin is a flightless bird...",
        "Reading 4:\n\nThe dolphin is an intelligent marine mammal...",
        "Reading 5:\n\nThe panda is native to China..."
    ]
    reading_index = 0

    # 🟩 5. Các khung giao diện
    progress_frame = tk.Frame(main_frame, bg="white", height=20)
    progress_frame.pack(fill="x", padx=20, pady=(15, 10))

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    button_frame = tk.Frame(main_frame, bg="white", height=70)
    button_frame.pack(fill="x", pady=(0, 15))

    BAR_HEIGHT = 10
    canvas = tk.Canvas(progress_frame, height=BAR_HEIGHT, bg="white", highlightthickness=0)
    canvas.place(relx=0.05, rely=0.1, relwidth=0.9)

    # 🟦 6. Hàm vẽ progress bar
    def draw_progress(value):
        canvas.delete("bar", "bg")
        width_all = canvas.winfo_width()
        canvas.create_rectangle(0, 0, width_all, BAR_HEIGHT, fill="#E0E0E0", outline="", tags="bg")
        width = int(width_all * value / 100) if width_all > 0 else 0
        canvas.create_rectangle(0, 0, width, BAR_HEIGHT, fill="#4CAF50", outline="", tags="bar")

    def calc_progress():
        if len(readings) == 1:
            return 100
        return int((reading_index / (len(readings) - 1)) * 100)

    # 🖼️ 7. Tiêu đề + ảnh + nút “Thoát Unit”
    top_row = tk.Frame(content_frame, bg="white")
    top_row.pack(fill="x", pady=(5, 10), padx=10)

    title_frame = tk.Frame(top_row, bg="white")
    title_frame.pack(side="left", anchor="w")

    try:
        img = Image.open("./photos/Tiger.png")
    except Exception:
        img = Image.new("RGB", (100, 100), "#4CAF50")
    img = img.resize((150, 100))
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(title_frame, image=photo, bg="white")
    img_label.image = photo
    img_label.pack(side="left", padx=(0, 10))

    tk.Label(
        title_frame, text="📖 Reading Practice",
        font=("Arial", 16, "bold"), bg="white"
    ).pack(side="left")

    # 🟥 Nút Thoát Unit
    def exit_unit():
        # Xóa nội dung main
        for w in main_frame.winfo_children():
            w.destroy()
        # Hủy sidebar_learning
        if sidebar_right_ref[0] is not None:
            try:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
            except Exception:
                pass
            sidebar_right_ref[0] = None
        root.update_idletasks()
        # Tạo lại sidebar_right
        recreate_sidebar_right()
        in_reading_mode[0] = False  # 🟥 reset trạng thái học
        # Quay lại danh sách Unit
        from controller.unit_controller import get_all_units
        if callable(show_in_main):
            show_in_main("Reading", get_all_units())

    # 🟨 8. Vùng nội dung
    text_box = tk.Text(
        content_frame, wrap="word", font=("Arial", 13),
        bg="#F8F9FA", relief="flat", padx=10, pady=5
    )
    text_box.place(relx = 0.01, rely=0.2)

    def update_text():
        text_box.delete("1.0", "end")
        text_box.insert("1.0", readings[reading_index])
        draw_progress(calc_progress())

    update_text()

    # 🟦 9. Các nút điều hướng
    def go_prev():
        nonlocal reading_index
        if reading_index > 0:
            reading_index -= 1
            update_text()

    def go_next():
        nonlocal reading_index
        if reading_index < len(readings) - 1:
            reading_index += 1
            update_text()

    tk.Button(
        button_frame, text="← Quay về", command=go_prev,
        bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="left", padx=40, pady=10)

    tk.Button(
        button_frame, text="Tiếp theo →", command=go_next,
        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="right", padx=40, pady=10)

    # Cập nhật progress khi canvas resize
    canvas.bind("<Configure>", lambda e: draw_progress(calc_progress()))
