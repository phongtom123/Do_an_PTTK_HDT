import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class LessonContentFrame(tk.Frame):
    """Khung học bài Reading"""
    def __init__(self, parent, show_in_main):
        super().__init__(parent, bg="white")
        self.show_in_main = show_in_main
        self.in_reading_mode = True
        self.current_index = 0
        self.current_popup = None

        # --- Dữ liệu mô phỏng ---
        self.readings = [
            "Reading 1:\n\nThe elephant is the largest land animal...",
            "Reading 2:\n\nThe cheetah is the fastest land animal...",
            "Reading 3:\n\nThe penguin is a flightless bird...",
            "Reading 4:\n\nThe dolphin is an intelligent marine mammal...",
            "Reading 5:\n\nThe panda is native to China..."
        ]

        self.highlight_data = {i: [] for i in range(len(self.readings))}
        self.vocab_data = {
            "elephant": ("noun", "con voi"),
            "cheetah": ("noun", "báo gê-pa"),
            "penguin": ("noun", "chim cánh cụt"),
            "dolphin": ("noun", "cá heo"),
            "panda": ("noun", "gấu trúc"),
            "fastest": ("adj", "nhanh nhất"),
            "flightless": ("adj", "không biết bay"),
            "intelligent": ("adj", "thông minh"),
        }

        self._create_widgets()
        self._update_text()

    # ===============================================
    # Giao diện
    # ===============================================
    def _create_widgets(self):
        """Tạo bố cục"""
        # --- Thanh tiến trình ---
        progress_frame = tk.Frame(self, bg="white", height=20)
        progress_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.canvas = tk.Canvas(progress_frame, height=10, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.05, rely=0.1, relwidth=0.9)

        self.lesson_title_label = tk.Label(
            progress_frame,
            text="Đang học: Reading 1",
            font=("Arial", 12, "bold"),
            fg="#333333",
            bg="white"
        )
        self.lesson_title_label.pack(pady=(25, 0))

        # --- Tabs ---
        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self.notebook = ttk.Notebook(content_frame)
        self.notebook.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.9)

        self.tab_learn = tk.Frame(self.notebook, bg="white")
        self.tab_exercise = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_learn, text="Tra từ vựng")
        self.notebook.add(self.tab_exercise, text="Chế độ Highlight")

        self.text_box = tk.Text(self.tab_learn, wrap="word", font=("Arial", 13),
                                bg="#F8F9FA", relief="flat", padx=10, pady=5)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.configure(state="disabled")

        self.exercise_text = tk.Text(self.tab_exercise, wrap="word", font=("Arial", 13),
                                     bg="#F8F9FA", relief="flat", padx=10, pady=5)
        self.exercise_text.pack(fill="both", expand=True)
        self.exercise_text.configure(state="disabled")

        # --- Nút điều khiển ---
        button_frame = tk.Frame(self, bg="white", height=70)
        button_frame.pack(fill="x", pady=(0, 15))

        tk.Button(button_frame, text="← Quay về", command=self._prev_reading,
                  bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12
        ).pack(side="left", padx=40, pady=10)

        self.complete_btn = tk.Button(button_frame, text="✅ Hoàn thành",
                                      command=self._complete_lesson,
                                      bg="#2196F3", fg="white",
                                      font=("Arial", 12, "bold"), width=14)

        tk.Button(button_frame, text="Tiếp theo →", command=self._next_reading,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12
        ).pack(side="right", padx=40, pady=10)

        self.canvas.bind("<Configure>", lambda e: self._draw_progress())

        # --- Menu chuột phải highlight ---
        self.highlight_menu = tk.Menu(self, tearoff=0)
        self.highlight_menu.add_command(label="Highlight", command=self._apply_highlight)
        self.highlight_menu.add_command(label="❌ Bỏ highlight", command=self._remove_highlight)
        self.exercise_text.bind("<Button-3>", lambda e: self.highlight_menu.tk_popup(e.x_root, e.y_root))

    # ===============================================
    # Cập nhật nội dung
    # ===============================================
    def _update_text(self):
        """Cập nhật text khi đổi bài"""
        if self.current_popup:
            self.current_popup.destroy()
            self.current_popup = None

        self.text_box.configure(state="normal")
        self.exercise_text.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.exercise_text.delete("1.0", "end")

        # === Nội dung bài ===
        self.text_box.insert("1.0", self.readings[self.current_index])
        self.exercise_text.insert("1.0", f"Bài tập Reading {self.current_index + 1}\n\n"
                                         f"1. Câu hỏi 1?\n2. Câu hỏi 2?\n3. Hãy tô sáng từ khóa!")

        # === Tô màu các từ vựng ===
        for word in self.vocab_data:
            start = "1.0"
            while True:
                pos = self.text_box.search(word, start, "end", nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                self.text_box.tag_add(word, pos, end)
                self.text_box.tag_config(word, foreground="#d00000", font=("Arial", 13, "bold"), underline=True)
                start = end

        def on_word_click(event):
            index = self.text_box.index(f"@{event.x},{event.y}")
            for tag in self.text_box.tag_names(index):
                if tag in self.vocab_data:
                    self._show_vocab_popup(tag, event.x_root, event.y_root)
                    break

        self.text_box.bind("<Button-1>", on_word_click)

        # === Highlight trong bài tập ===
        self.exercise_text.tag_delete("highlight")
        self.exercise_text.tag_config("highlight", background="yellow")
        for (s, e) in self.highlight_data[self.current_index]:
            self.exercise_text.tag_add("highlight", s, e)

        # === Cập nhật thanh tiến trình ===
        self.lesson_title_label.config(text=f"Đang học: Reading {self.current_index + 1}")
        self._draw_progress()

        # === Ẩn/hiện nút hoàn thành ===
        if self.current_index == len(self.readings) - 1:
            self.complete_btn.pack(side="left", padx=10)
        else:
            self.complete_btn.pack_forget()

        self.text_box.configure(state="disabled")
        self.exercise_text.configure(state="disabled")

    # ===============================================
    # Popup & Highlight
    # ===============================================
    def _show_vocab_popup(self, word, x, y):
        """Hiển thị popup tra nghĩa"""
        if self.current_popup:
            self.current_popup.destroy()
            self.current_popup = None

        if word not in self.vocab_data:
            return

        pos, meaning = self.vocab_data[word]
        popup = tk.Toplevel(self)
        popup.wm_overrideredirect(True)
        popup.wm_geometry(f"+{x+10}+{y+10}")
        popup.config(bg="#FFF8DC", padx=8, pady=5)

        tk.Label(popup, text=word, font=("Arial", 12, "bold"), bg="#FFF8DC").pack(anchor="w")
        tk.Label(popup, text=f"Loại từ: {pos}", font=("Arial", 10), bg="#FFF8DC").pack(anchor="w")
        tk.Label(popup, text=f"Nghĩa: {meaning}", font=("Arial", 10), bg="#FFF8DC").pack(anchor="w")

        self.current_popup = popup

    def _apply_highlight(self):
        try:
            start = self.exercise_text.index("sel.first")
            end = self.exercise_text.index("sel.last")
            self.exercise_text.tag_add("highlight", start, end)
            self.highlight_data[self.current_index].append((start, end))
        except:
            pass

    def _remove_highlight(self):
        try:
            start = self.exercise_text.index("sel.first")
            end = self.exercise_text.index("sel.last")
            self.exercise_text.tag_remove("highlight", start, end)
        except:
            pass

    # ===============================================
    # Nút điều hướng
    # ===============================================
    def _prev_reading(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._update_text()

    def _next_reading(self):
        if self.current_index < len(self.readings) - 1:
            self.current_index += 1
            self._update_text()

    def _complete_lesson(self):
        messagebox.showinfo("🎉 Hoàn thành", "Chúc mừng bạn đã hoàn thành bài học!")
        self.show_in_main("__BACK__", [])

    # ===============================================
    # Tiến trình
    # ===============================================
    def _draw_progress(self):
        """Vẽ thanh tiến trình"""
        self.canvas.delete("bar", "bg")
        width_all = self.canvas.winfo_width()
        self.canvas.create_rectangle(0, 0, width_all, 10, fill="#E0E0E0", outline="", tags="bg")
        value = (self.current_index / (len(self.readings) - 1)) * 100 if len(self.readings) > 1 else 100
        width = int(width_all * value / 100)
        self.canvas.create_rectangle(0, 0, width, 10, fill="#4CAF50", outline="", tags="bar")


# --- Chạy thử độc lập ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = LessonContentFrame(root, show_in_main=lambda *args: print("Back:", args))
    app.pack(fill="both", expand=True)
    root.mainloop()
