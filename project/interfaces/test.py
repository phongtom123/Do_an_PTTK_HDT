import tkinter as tk
from tkinter import ttk

def show_reading_practice(root, main_frame, sidebar_right_ref,
                          recreate_sidebar_right, show_in_main, in_reading_mode):

    in_reading_mode[0] = True

    # Xóa nội dung cũ
    for w in main_frame.winfo_children():
        w.destroy()

    # ------------------ Dữ liệu từ vựng ------------------
    vocab = {
        "elephant": ("noun", "con voi"),
        "largest": ("adj", "lớn nhất"),
        "animal": ("noun", "động vật"),
        "land": ("noun", "đất liền"),
        "cheetah": ("noun", "báo săn"),
        "fastest": ("adj", "nhanh nhất"),
    }

    readings = [
        "Reading 1:\n\nThe elephant is the largest land animal.",
        "Reading 2:\n\nThe cheetah is the fastest land animal.",
    ]
    reading_index = 0

    # Layout chính
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    notebook = ttk.Notebook(content_frame)
    notebook.pack(fill="both", expand=True)

    tab_learn = tk.Frame(notebook, bg="white")
    tab_exercise = tk.Frame(notebook, bg="white")
    notebook.add(tab_learn, text="Tra từ vựng")
    notebook.add(tab_exercise, text="Chế độ Highlight")

    text_box = tk.Text(tab_learn, wrap="word", font=("Arial", 13),
                       bg="#F8F9FA", relief="flat", padx=10, pady=5)
    text_box.pack(fill="both", expand=True)
    text_box.configure(state="disabled")

    # --------- Popup tra từ vựng ---------
    current_popup = None

    def close_popup(event=None):
        nonlocal current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None

    def show_popup(x, y, word):
        nonlocal current_popup
        close_popup()

        word_lower = word.lower()
        if word_lower not in vocab:
            return

        pos, meaning = vocab[word_lower]

        popup = tk.Toplevel(root)
        popup.wm_overrideredirect(True)
        popup.wm_geometry(f"+{x + 10}+{y + 10}")
        popup.configure(bg="#ffffe0", padx=8, pady=5)

        tk.Label(popup, text=word, font=("Arial", 12, "bold"), bg="#ffffe0").pack(anchor="w")
        tk.Label(popup, text=f"Loại từ: {pos}", font=("Arial", 10), bg="#ffffe0").pack(anchor="w")
        tk.Label(popup, text=f"Nghĩa: {meaning}", font=("Arial", 10), bg="#ffffe0").pack(anchor="w")

        current_popup = popup

        root.bind("<Button-1>", close_popup, add="+")

    def on_click_word(event):
        index = text_box.index(f"@{event.x},{event.y}")
        tags = text_box.tag_names(index)
        for t in tags:
            if t.startswith("word_"):
                word = t.replace("word_", "")
                x = root.winfo_pointerx()
                y = root.winfo_pointery()
                show_popup(x, y, word)
                break

    def update_text():
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.insert("1.0", readings[reading_index])

        for word in vocab:
            start = "1.0"
            while True:
                idx = text_box.search(word, start, "end", nocase=1)
                if not idx:
                    break
                end = f"{idx}+{len(word)}c"
                tag = f"word_{word}"
                text_box.tag_add(tag, idx, end)
                text_box.tag_config(tag, foreground="blue", underline=True)
                start = end

        text_box.configure(state="disabled")

    text_box.bind("<Button-1>", on_click_word)

    nav = tk.Frame(main_frame, bg="white")
    nav.pack(fill="x")

    def prev():
        nonlocal reading_index
        if reading_index > 0:
            reading_index -= 1
            close_popup()
            update_text()

    def next():
        nonlocal reading_index
        if reading_index < len(readings) - 1:
            reading_index += 1
            close_popup()
            update_text()

    tk.Button(nav, text="← Trước", command=prev, width=10).pack(side="left", padx=20, pady=10)
    tk.Button(nav, text="Sau →", command=next, width=10).pack(side="right", padx=20, pady=10)

    update_text()
