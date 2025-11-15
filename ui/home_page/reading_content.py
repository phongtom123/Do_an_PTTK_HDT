import tkinter as tk
from tkinter import ttk
from ui.home_page.sidebar_learning import SidebarLearning
from logic.word_controller import get_words_by_lesson_id


class ReadingPracticeFrame(tk.Frame):
    """Khung Reading Practice có highlight từ thực tế theo Lesson (sửa lỗi popup chỉ hiển thị ở bài đầu)"""

    def __init__(self, root, main_frame, sidebar_right_ref,
                 recreate_sidebar_right, show_in_main, in_learning_mode,
                 readings=None, vocab_data=None, lesson_id=None):
        super().__init__(main_frame, bg="white")

        self.root = root
        self.main_frame = main_frame
        self.sidebar_right_ref = sidebar_right_ref
        self.recreate_sidebar_right = recreate_sidebar_right
        self.show_in_main = show_in_main
        self.in_learning_mode = in_learning_mode
        self.lesson_id = lesson_id
        self.vocab_data = vocab_data if vocab_data else {}

        try:
            self.in_learning_mode[0] = True
        except Exception:
            pass

        # ===================== DỮ LIỆU =====================
        self.reading_texts = []
        if readings and len(readings) > 0:
            for r in readings:
                if isinstance(r, dict):
                    title = r.get("title", "Reading Practice")
                    content = r.get("content", r.get("reading_content", ""))
                    self.reading_texts.append({"title": title, "content": content})
                else:
                    try:
                        content = getattr(r, "reading_content", "") or getattr(r, "content", "")
                    except Exception:
                        content = ""
                    title_val = getattr(r, "reading_title", "") or getattr(r, "title", "Reading Practice")
                    self.reading_texts.append({"title": title_val, "content": content})
        else:
            self.reading_texts = [
                {"title": "Reading 1", "content": "Reading 1:\n\nThe elephant is the largest land animal..."},
            ]

        self.reading_index = 0
        self.highlight_data = {i: [] for i in range(len(self.reading_texts))}
        self.current_popup = None

        # ===================== GIAO DIỆN =====================
        self._setup_sidebar()
        self._create_layout()
        self._update_text()

    # ============================================================
    def _setup_sidebar(self):
        """Thay sidebar phải bằng SidebarLearning nếu cần"""
        if self.sidebar_right_ref and isinstance(self.sidebar_right_ref, (list, tuple)) and len(self.sidebar_right_ref) > 0:
            existing = self.sidebar_right_ref[0]
            if existing is not None:
                try:
                    if hasattr(existing, "winfo_exists") and existing.winfo_exists():
                        try:
                            existing.pack(side="right", fill="y", padx=(10, 20), pady=10)
                        except Exception:
                            pass
                        return
                except Exception:
                    pass

        try:
            self.sidebar_right_ref[0] = SidebarLearning(self.root, mode="Reading")
        except Exception:
            self.sidebar_right_ref[0] = None

    # ============================================================
    def _create_layout(self):
        """Tạo bố cục giao diện chính"""
        self.progress_frame = tk.Frame(self, bg="white", height=20)
        self.progress_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self.button_frame = tk.Frame(self, bg="white", height=70)
        self.button_frame.pack(fill="x", pady=(0, 15))

        # Thanh tiến trình
        self.BAR_HEIGHT = 10
        self.canvas = tk.Canvas(self.progress_frame, height=self.BAR_HEIGHT,
                                bg="white", highlightthickness=0)
        self.canvas.place(relx=0.05, rely=0.1, relwidth=0.9)
        self.canvas.bind("<Configure>", lambda e: self._draw_progress())

        # Header
        top_row = tk.Frame(self.content_frame, bg="white")
        top_row.pack(fill="x", pady=(5, 10), padx=10)
        tk.Label(top_row, text="📖 Reading Practice",
                 font=("Arial", 16, "bold"), bg="white").pack(anchor="w")

        # Notebook (2 tab)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.75)

        self.tab_learn = tk.Frame(self.notebook, bg="white")
        self.tab_exercise = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_learn, text="Tra từ vựng")
        self.notebook.add(self.tab_exercise, text="Chế độ Highlight")

        # Text chính (Tab 1)
        self.text_box = tk.Text(self.tab_learn, wrap="word", font=("Arial", 13),
                                bg="#F8F9FA", relief="flat", padx=10, pady=5)
        self.text_box.pack(fill="both", expand=True)
        self.text_box.configure(state="disabled")

        # Text highlight (Tab 2)
        self.exercise_text = tk.Text(self.tab_exercise, wrap="word", font=("Arial", 13),
                                     bg="#F8F9FA", relief="flat", padx=10, pady=5)
        self.exercise_text.pack(fill="both", expand=True)
        self.exercise_text.configure(state="disabled")

        # Menu chuột phải
        self.highlight_menu = tk.Menu(self.root, tearoff=0)
        self.highlight_menu.add_command(label="Highlight", command=self._apply_highlight)
        self.highlight_menu.add_command(label="❌ Bỏ highlight", command=self._remove_highlight)
        self.exercise_text.bind("<Button-3>", lambda e: self.highlight_menu.tk_popup(e.x_root, e.y_root))

        # Nút điều hướng
        tk.Button(self.button_frame, text="← Quay về", command=self._go_prev,
                  bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12
                  ).pack(side="left", padx=40, pady=10)
        tk.Button(self.button_frame, text="Tiếp theo →", command=self._go_next,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12
                  ).pack(side="right", padx=40, pady=10)

    # ============================================================
    def _draw_progress(self):
        self.canvas.delete("bar", "bg")
        width_all = self.canvas.winfo_width()
        self.canvas.create_rectangle(0, 0, width_all, self.BAR_HEIGHT,
                                     fill="#E0E0E0", outline="", tags="bg")
        progress = (self.reading_index / (len(self.reading_texts) - 1)) * 100 if len(self.reading_texts) > 1 else 100
        width = int(width_all * progress / 100)
        self.canvas.create_rectangle(0, 0, width, self.BAR_HEIGHT,
                                     fill="#4CAF50", outline="", tags="bar")

    # ============================================================
    def _update_text(self):
        """Cập nhật nội dung Reading và popup từ thực tế (fix tag/bind issues)"""
        # đóng popup cũ
        if self.current_popup:
            try:
                self.current_popup.destroy()
            except Exception:
                pass
            self.current_popup = None

        self.text_box.configure(state="normal")
        self.exercise_text.configure(state="normal")

        data = self.reading_texts[self.reading_index]
        content = data.get("content", "") if isinstance(data, dict) else str(data)

        # reset nội dung
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", content)
        self.exercise_text.delete("1.0", "end")
        self.exercise_text.insert("1.0", content)

        # --------- xoá tag vocab cũ (nếu có) để tránh xung đột ----------
        try:
            for tag in list(self.text_box.tag_names()):
                if str(tag).startswith("vocab_"):
                    try:
                        self.text_box.tag_delete(tag)
                    except Exception:
                        pass
        except Exception:
            pass

        # 🔹 CHỈ lấy từ theo bài học hiện tại
        db_words = []
        if self.lesson_id:
            try:
                db_words = get_words_by_lesson_id(self.lesson_id) or []
            except Exception as e:
                print(f"[DEBUG] Lỗi lấy từ vựng cho lesson_id={self.lesson_id}: {e}")
                db_words = []
        else:
            db_words = []

        # debug
        # print số lượng từ lấy được - bạn có thể comment dòng sau khi ổn
        # (giữ print để bạn dễ test)
        print(f"[DEBUG] Reading idx={self.reading_index}, lesson_id={self.lesson_id}, words={len(db_words)}")

        # Thêm tag + bind cho từng từ (dùng tag unique để tránh reuse)
        for i, word in enumerate(db_words):
            # Hỗ trợ cả object và dict/tuple: cố gắng lấy thuộc tính
            try:
                word_text = getattr(word, "word", None) or (word.get("word") if isinstance(word, dict) else None) or str(word)
            except Exception:
                word_text = str(word)
            try:
                meaning = getattr(word, "word_meaning", None) or (word.get("word_meaning") if isinstance(word, dict) else "") or ""
            except Exception:
                meaning = ""

            word_text = word_text.strip()
            if not word_text:
                continue

            tag_name = f"vocab_{self.reading_index}_{i}"

            # định dạng tag
            try:
                self.text_box.tag_config(tag_name, foreground="#d00000", font=("Arial", 13, "bold"), underline=True)
            except Exception:
                pass

            # tìm và gắn tag cho mọi vị trí xuất hiện (nocase)
            start = "1.0"
            while True:
                pos = self.text_box.search(word_text, start, "end", nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(word_text)}c"
                try:
                    self.text_box.tag_add(tag_name, pos, end)
                except Exception:
                    pass
                start = end

            # bind sự kiện click cho tag (dùng default args để tránh closure problem)
            try:
                self.text_box.tag_bind(tag_name, "<Button-1>", lambda e, w=word_text, m=meaning: self._show_vocab_popup_db(w, m, e.x_root, e.y_root))
            except Exception:
                pass

        # Load highlight cũ
        self.exercise_text.tag_config("highlight", background="yellow")
        for (s, e) in self.highlight_data.get(self.reading_index, []):
            try:
                self.exercise_text.tag_add("highlight", s, e)
            except Exception:
                pass

        self.text_box.configure(state="disabled")
        self.exercise_text.configure(state="disabled")
        self._draw_progress()

    # ============================================================
    def _show_vocab_popup_db(self, word, meaning, x, y):
        """Hiển thị popup nghĩa của từ vựng thật"""
        if self.current_popup:
            try:
                self.current_popup.destroy()
            except Exception:
                pass
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.wm_geometry(f"+{x+10}+{y+10}")
        popup.config(bg="#FFF8DC", padx=8, pady=5)
        tk.Label(popup, text=word, font=("Arial", 12, "bold"), bg="#FFF8DC").pack(anchor="w")
        tk.Label(popup, text=f"Nghĩa: {meaning}", font=("Arial", 10), bg="#FFF8DC").pack(anchor="w")
        self.current_popup = popup

    # ============================================================
    def _apply_highlight(self):
        try:
            start = self.exercise_text.index("sel.first")
            end = self.exercise_text.index("sel.last")
            self.exercise_text.tag_add("highlight", start, end)
            self.highlight_data[self.reading_index].append((start, end))
        except Exception:
            pass

    def _remove_highlight(self):
        try:
            start = self.exercise_text.index("sel.first")
            end = self.exercise_text.index("sel.last")
            self.exercise_text.tag_remove("highlight", start, end)
        except Exception:
            pass

    def _go_prev(self):
        if self.reading_index > 0:
            self.reading_index -= 1
            self._update_text()

    def _go_next(self):
        if self.reading_index < len(self.reading_texts) - 1:
            self.reading_index += 1
            self._update_text()
