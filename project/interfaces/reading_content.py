import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sidebar_learning import create_sidebar_learning


def show_reading_practice(root, main_frame, sidebar_right_ref,
                          recreate_sidebar_right, show_in_main, in_learning_mode,
                          readings=None):

    # ✅ Đúng biến
    in_learning_mode[0] = True

    # Xóa nội dung cũ trong main_frame
    for w in main_frame.winfo_children():
        w.destroy()

    # Ẩn sidebar phải
    if sidebar_right_ref[0] is not None:
        try:
            sidebar_right_ref[0].pack_forget()
            sidebar_right_ref[0].destroy()
        except Exception:
            pass
        sidebar_right_ref[0] = None
    root.update_idletasks()

    # Tạo sidebar học tập bên phải
    sidebar_learning = create_sidebar_learning(root, mode="Reading")
    sidebar_right_ref[0] = sidebar_learning

    # ------------------ DỮ LIỆU BÀI ĐỌC ------------------
    if readings and len(readings) > 0:
        # Nếu có dữ liệu từ DB, lấy nội dung thật
        reading_texts = [r.get_reading_content() for r in readings]
    else:
        # Nếu chưa có dữ liệu trong DB, dùng dữ liệu mẫu
        reading_texts = [
            "Reading 1:\n\nThe elephant is the largest land animal...",
            "Reading 2:\n\nThe cheetah is the fastest land animal...",
            "Reading 3:\n\nThe penguin is a flightless bird...",
            "Reading 4:\n\nThe dolphin is an intelligent marine mammal...",
            "Reading 5:\n\nThe panda is native to China..."
        ]

    reading_index = 0
    highlight_data = {i: [] for i in range(len(reading_texts))}

    # ------------------ TỪ VỰNG QUAN TRỌNG ------------------
    vocab_data = {
        "elephant": ("noun", "con voi"),
        "cheetah": ("noun", "báo gê-pa"),
        "penguin": ("noun", "chim cánh cụt"),
        "dolphin": ("noun", "cá heo"),
        "panda": ("noun", "gấu trúc"),
        "fastest": ("adj", "nhanh nhất"),
        "flightless": ("adj", "không biết bay"),
        "intelligent": ("adj", "thông minh"),
    }

    current_popup = None  # popup đang mở

    # ------------------ LAYOUT ------------------
    progress_frame = tk.Frame(main_frame, bg="white", height=20)
    progress_frame.pack(fill="x", padx=20, pady=(15, 10))

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    button_frame = tk.Frame(main_frame, bg="white", height=70)
    button_frame.pack(fill="x", pady=(0, 15))

    BAR_HEIGHT = 10
    canvas = tk.Canvas(progress_frame, height=BAR_HEIGHT, bg="white", highlightthickness=0)
    canvas.place(relx=0.05, rely=0.1, relwidth=0.9)

    def draw_progress(value):
        canvas.delete("bar", "bg")
        width_all = canvas.winfo_width()
        canvas.create_rectangle(0, 0, width_all, BAR_HEIGHT, fill="#E0E0E0", outline="", tags="bg")
        width = int(width_all * value / 100) if width_all > 0 else 0
        canvas.create_rectangle(0, 0, width, BAR_HEIGHT, fill="#4CAF50", outline="", tags="bar")

    def calc_progress():
        if len(reading_texts) == 1:
            return 100
        return int((reading_index / (len(reading_texts) - 1)) * 100)

    # ------------------ HEADER ------------------
    top_row = tk.Frame(content_frame, bg="white")
    top_row.pack(fill="x", pady=(5, 10), padx=10)
    tk.Label(top_row, text="📖 Reading Practice",
             font=("Arial", 16, "bold"), bg="white").pack(anchor="w")

    # ------------------ NOTEBOOK ------------------
    notebook = ttk.Notebook(content_frame)
    notebook.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.75)

    tab_learn = tk.Frame(notebook, bg="white")
    tab_exercise = tk.Frame(notebook, bg="white")

    notebook.add(tab_learn, text="Tra từ vựng")
    notebook.add(tab_exercise, text="Chế độ Highlight")

    text_box = tk.Text(tab_learn, wrap="word", font=("Arial", 13),
                       bg="#F8F9FA", relief="flat", padx=10, pady=5)
    text_box.pack(fill="both", expand=True)
    text_box.configure(state="disabled")

    exercise_text = tk.Text(tab_exercise, wrap="word", font=("Arial", 13),
                           bg="#F8F9FA", relief="flat", padx=10, pady=5)
    exercise_text.pack(fill="both", expand=True)
    exercise_text.configure(state="disabled")

    # ------------------ POPUP TỪ VỰNG ------------------
    def show_vocab_popup(word, x, y):
        nonlocal current_popup

        if current_popup:
            try:
                current_popup.destroy()
            except:
                pass
            current_popup = None

        if word not in vocab_data:
            return

        pos, meaning = vocab_data[word]

        popup = tk.Toplevel(root)
        popup.wm_overrideredirect(True)
        popup.wm_geometry(f"+{x+10}+{y+10}")
        popup.config(bg="#FFF8DC", padx=8, pady=5)

        tk.Label(popup, text=word, font=("Arial", 12, "bold"), bg="#FFF8DC").pack(anchor="w")
        tk.Label(popup, text=f"Loại từ: {pos}", font=("Arial", 10), bg="#FFF8DC").pack(anchor="w")
        tk.Label(popup, text=f"Nghĩa: {meaning}", font=("Arial", 10), bg="#FFF8DC").pack(anchor="w")

        current_popup = popup

    # ------------------ UPDATE TEXT ------------------
    def update_text():
        nonlocal reading_index, current_popup

        if current_popup:
            try:
                current_popup.destroy()
            except:
                pass
            current_popup = None

        text_box.configure(state="normal")
        exercise_text.configure(state="normal")

        text_box.delete("1.0", "end")
        text_box.insert("1.0", reading_texts[reading_index])

        exercise_text.delete("1.0", "end")
        exercise_text.insert("1.0",
            f" Bài tập của Reading {reading_index + 1}\n\n"
            f"1. Trả lời câu hỏi.\n"
            f"2. Chọn đáp án đúng.\n"
            f"3. Tô sáng từ khóa quan trọng bằng chuột phải."
        )

        # Highlight từ vựng
        for word in vocab_data:
            start = "1.0"
            while True:
                pos = text_box.search(word, start, "end", nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                text_box.tag_add(word, pos, end)
                text_box.tag_config(word, foreground="#d00000", font=("Arial", 13, "bold"), underline=True)
                start = end

        # Click vào từ
        def on_word_click(event):
            index = text_box.index(f"@{event.x},{event.y}")
            for tag in text_box.tag_names(index):
                if tag in vocab_data:
                    show_vocab_popup(tag, event.x_root, event.y_root)
                    break

        text_box.bind("<Button-1>", on_word_click)

        # Highlight
        exercise_text.tag_delete("highlight")
        exercise_text.tag_config("highlight", background="yellow")
        for (s, e) in highlight_data[reading_index]:
            try:
                exercise_text.tag_add("highlight", s, e)
            except:
                pass

        text_box.configure(state="disabled")
        exercise_text.configure(state="disabled")
        draw_progress(calc_progress())

    # ------------------ MENU HIGHLIGHT ------------------
    highlight_menu = tk.Menu(root, tearoff=0)
    highlight_menu.add_command(label="Highlight", command=lambda: apply_highlight())
    highlight_menu.add_command(label="❌ Bỏ highlight", command=lambda: remove_highlight())

    def apply_highlight():
        try:
            start = exercise_text.index("sel.first")
            end = exercise_text.index("sel.last")
            exercise_text.tag_add("highlight", start, end)
            highlight_data[reading_index].append((start, end))
        except:
            pass

    def remove_highlight():
        try:
            start = exercise_text.index("sel.first")
            end = exercise_text.index("sel.last")
            exercise_text.tag_remove("highlight", start, end)
        except:
            pass

    exercise_text.bind("<Button-3>", lambda e: highlight_menu.tk_popup(e.x_root, e.y_root))

    # ------------------ NÚT CHUYỂN BÀI ------------------
    def go_prev():
        nonlocal reading_index
        if reading_index > 0:
            reading_index -= 1
            update_text()

    def go_next():
        nonlocal reading_index
        if reading_index < len(reading_texts) - 1:
            reading_index += 1
            update_text()

    tk.Button(button_frame, text="← Quay về", command=go_prev,
              bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="left", padx=40, pady=10)

    tk.Button(button_frame, text="Tiếp theo →", command=go_next,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="right", padx=40, pady=10)

    canvas.bind("<Configure>", lambda e: draw_progress(calc_progress()))
    update_text()
