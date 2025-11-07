import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sidebar_learning import create_sidebar_learning


def show_reading_practice(root, main_frame, sidebar_right_ref,
                          recreate_sidebar_right, show_in_main, in_reading_mode):

    in_reading_mode[0] = True

    #  Xóa nội dung cũ 
    for w in main_frame.winfo_children():
        w.destroy()

    if sidebar_right_ref[0] is not None:
        try:
            sidebar_right_ref[0].pack_forget()
            sidebar_right_ref[0].destroy()
        except:
            pass
        sidebar_right_ref[0] = None
    root.update_idletasks()

    sidebar_learning = create_sidebar_learning(root)
    sidebar_right_ref[0] = sidebar_learning

    #  Dữ liệu bài đọc
    readings = [
        "Reading 1:\n\nThe elephant is the largest land animal...",
        "Reading 2:\n\nThe cheetah is the fastest land animal...",
        "Reading 3:\n\nThe penguin is a flightless bird...",
        "Reading 4:\n\nThe dolphin is an intelligent marine mammal...",
        "Reading 5:\n\nThe panda is native to China..."
    ]
    reading_index = 0

    #  Lưu highlight của từng bài đọc 
    highlight_data = {i: [] for i in range(len(readings))}

    # Layout 
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
        if len(readings) == 1:
            return 100
        return int((reading_index / (len(readings) - 1)) * 100)

    # Header 
    top_row = tk.Frame(content_frame, bg="white")
    top_row.pack(fill="x", pady=(5, 10), padx=10)

    title_frame = tk.Frame(top_row, bg="white")
    title_frame.pack(side="left", anchor="w")

    tk.Label(
        title_frame, text="📖 Reading Practice",
        font=("Arial", 16, "bold"), bg="white"
    ).pack(side="left")

    # Notebook 
    notebook = ttk.Notebook(content_frame)
    notebook.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.75)

    tab_learn = tk.Frame(notebook, bg="white")
    tab_exercise = tk.Frame(notebook, bg="white")

    notebook.add(tab_learn, text=" Chế độ học")
    notebook.add(tab_exercise, text=" Bài tập")

    text_box = tk.Text(tab_learn, wrap="word", font=("Arial", 13),
                       bg="#F8F9FA", relief="flat", padx=10, pady=5)
    text_box.pack(fill="both", expand=True)
    text_box.configure(state="disabled")

    exercise_text = tk.Text(tab_exercise, wrap="word", font=("Arial", 13),
                           bg="#F8F9FA", relief="flat", padx=10, pady=5)
    exercise_text.pack(fill="both", expand=True)
    exercise_text.configure(state="disabled")

    # Popup highlight 
    highlight_menu = tk.Menu(root, tearoff=0)
    highlight_menu.add_command(label="Highlight", command=lambda: apply_highlight())
    highlight_menu.add_command(label="❌ Bỏ highlight", command=lambda: remove_highlight())

    def show_highlight_menu(event):
        try:
            if exercise_text.tag_ranges("sel"):
                highlight_menu.tk_popup(event.x_root, event.y_root)
        finally:
            highlight_menu.grab_release()

    def apply_highlight():
        try:
            start = exercise_text.index("sel.first")
            end = exercise_text.index("sel.last")
            exercise_text.tag_add("highlight", start, end)
            exercise_text.tag_config("highlight", background="yellow")

            # Lưu vị trí highlight cho bài hiện tại
            highlight_data[reading_index].append((start, end))
        except tk.TclError:
            pass

    def remove_highlight():
        try:
            start = exercise_text.index("sel.first")
            end = exercise_text.index("sel.last")
            exercise_text.tag_remove("highlight", start, end)

            # Xóa các đoạn nằm trong khoảng này
            new_ranges = []
            for (s, e) in highlight_data[reading_index]:
                if not (exercise_text.compare(s, ">=", start) and exercise_text.compare(e, "<=", end)):
                    new_ranges.append((s, e))
            highlight_data[reading_index] = new_ranges
        except tk.TclError:
            pass

    exercise_text.bind("<Button-3>", show_highlight_menu)

    # Cập nhật nội dung 
    def update_text():
        nonlocal reading_index

        text_box.configure(state="normal")
        exercise_text.configure(state="normal")

        text_box.delete("1.0", "end")
        text_box.insert("1.0", readings[reading_index])

        exercise_text.delete("1.0", "end")
        exercise_text.insert("1.0",
            f" Bài tập của Reading {reading_index + 1}\n\n"
            f"1. Câu hỏi mẫu?\n"
            f"2. Câu hỏi mẫu khác?\n"
            f"3. Bạn có thể chọn và tô sáng từ khóa bằng chuột phải!"
        )

        exercise_text.tag_delete("highlight")
        exercise_text.tag_config("highlight", background="yellow")

        # Khôi phục highlight cũ
        for (s, e) in highlight_data[reading_index]:
            try:
                exercise_text.tag_add("highlight", s, e)
            except tk.TclError:
                pass

        text_box.configure(state="disabled")
        exercise_text.configure(state="disabled")
        draw_progress(calc_progress())

    #  Nút điều hướng 
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

    tk.Button(button_frame, text="← Quay về", command=go_prev,
              bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="left", padx=40, pady=10)

    tk.Button(button_frame, text="Tiếp theo →", command=go_next,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12
    ).pack(side="right", padx=40, pady=10)

    canvas.bind("<Configure>", lambda e: draw_progress(calc_progress()))
    update_text()
