import tkinter as tk

class SidebarLearning(tk.Frame):
    """Sidebar hiển thị câu hỏi thật khi học Reading hoặc Listening"""

    def __init__(self, root, current_user, mode="Reading", questions=None):
        super().__init__(root, bg="#FFFFFF", width=250,
                         highlightbackground="#d0d0d0",
                         highlightthickness=2, bd=0)
        self.pack(side="right", fill="y", padx=(10, 20), pady=10)
        self.pack_propagate(False)

        self.mode = mode
        self.questions = questions if questions else []

        # Vùng scroll
        self._create_scroll_area()

        # Sinh câu hỏi
        self._populate_questions()

        # Nút hoàn thành
        self._create_complete_button()

    # -------------------------------------------
    # VÙNG SCROLL
    # -------------------------------------------
    def _create_scroll_area(self):
        """Tạo canvas có scrollbar"""
        self.canvas = tk.Canvas(self, bg="#FFFFFF", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", on_frame_configure)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    # -------------------------------------------
    # CÂU HỎI
    # -------------------------------------------
    def _populate_questions(self):
        """Hiển thị câu hỏi từ DB hoặc dữ liệu mẫu"""
        questions_data = []

        # ✅ Có dữ liệu thật từ DB
        if self.questions and len(self.questions) > 0:
            print(f"[DEBUG] 🟢 Hiển thị {len(self.questions)} câu hỏi từ DB trong SidebarLearning.")
            for q in self.questions:
                content = getattr(q, "content", None) or getattr(q, "question_content", "No content")
                options = getattr(q, "options", []) or []
                questions_data.append({"q": content, "opts": options})
        else:
            print("[DEBUG] ⚠️ Không có dữ liệu thật, dùng câu hỏi mẫu.")
            # ❌ Không có dữ liệu thật → dùng mẫu
            if self.mode == "Reading":
                questions_data = [
                    {"q": "What is the main idea of the passage?",
                     "opts": ["A. Travel", "B. Food", "C. Sports", "D. Technology"]},
                    {"q": "How many animals were mentioned in this paragraph?",
                     "opts": ["A. 1", "B. 2", "C. 3", "D. None"]},
                    {"q": "Which color symbolizes peace?",
                     "opts": ["A. Red", "B. Green", "C. White", "D. Black"]},
                ]
            elif self.mode == "Listening":
                questions_data = [
                    {"q": "What did the speaker mention first?",
                     "opts": ["A. The weather", "B. His work", "C. A trip", "D. A song"]},
                    {"q": "Where does the conversation take place?",
                     "opts": ["A. At school", "B. At a cafe", "C. On a bus", "D. At home"]},
                    {"q": "What is the tone of the speaker?",
                     "opts": ["A. Angry", "B. Happy", "C. Sad", "D. Surprised"]},
                ]

        # 🧩 Nếu vẫn trống
        if not questions_data:
            tk.Label(self.scrollable_frame, text="Không có câu hỏi cho bài học này.",
                     bg="white", fg="#777", font=("Arial", 11, "italic")).pack(pady=15)
            return

        # 🧱 Tạo giao diện cho từng câu hỏi
        for i, q in enumerate(questions_data, start=1):
            self._create_question_card(self.scrollable_frame, i, q["q"], q["opts"])

    # -------------------------------------------
    # THẺ CÂU HỎI
    # -------------------------------------------
    def _create_question_card(self, parent, q_num, question, options):
        """Tạo một card câu hỏi"""
        outer = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#e0e0e0")
        outer.pack(pady=8, padx=8, fill="x")

        card = tk.Frame(outer, bg="white")
        card.pack(padx=4, pady=4, fill="x")

        tk.Label(card, text=f"Question {q_num}:", font=("Arial", 11, "bold"),
                 bg="white", anchor="w").pack(fill="x", padx=10, pady=(6, 0))
        tk.Label(card, text=question, font=("Arial", 10),
                 bg="white", wraplength=220, justify="left", anchor="w").pack(padx=10, pady=5, fill="x")

        selected_option = tk.StringVar(value="")
        for opt in options:
            self._create_circle_radiobutton(card, opt, selected_option, opt)

    # -------------------------------------------
    # RADIO BUTTON TÙY CHỈNH
    # -------------------------------------------
    def _create_circle_radiobutton(self, parent, text, var, value):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=10, pady=3)

        canvas = tk.Canvas(frame, width=18, height=18, bg="white", highlightthickness=0)
        canvas.pack(side="left", padx=(0, 8))
        circle = canvas.create_oval(2, 2, 16, 16, outline="#888", width=1.5, fill="white")

        label = tk.Label(frame, text=text, font=("Arial", 10), bg="white", anchor="w")
        label.pack(side="left", fill="x", expand=True)

        def update_circle():
            if var.get() == value:
                canvas.itemconfig(circle, fill="#000000", outline="#000000")
            else:
                canvas.itemconfig(circle, fill="white", outline="#888")

        def on_click(event=None):
            var.set(value)
            for w in parent.winfo_children():
                if hasattr(w, "update_circle_func"):
                    w.update_circle_func()

        def on_hover(event=None):
            if var.get() != value:
                canvas.itemconfig(circle, outline="#3498db")

        def on_leave(event=None):
            if var.get() != value:
                canvas.itemconfig(circle, outline="#888")

        frame.bind("<Button-1>", on_click)
        label.bind("<Button-1>", on_click)
        canvas.bind("<Button-1>", on_click)
        for widget in (frame, label, canvas):
            widget.bind("<Enter>", on_hover)
            widget.bind("<Leave>", on_leave)

        frame.update_circle_func = update_circle
        update_circle()

    # -------------------------------------------
    # NÚT HOÀN THÀNH
    # -------------------------------------------
    def _create_complete_button(self):
        """Nút hoàn thành bài học"""
        def on_complete():
            print(f"✅ {self.mode} practice completed!")

        complete_btn = tk.Button(
            self.scrollable_frame,
            text="Hoàn thành",
            command=on_complete,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            activebackground="#27ae60",
            activeforeground="white",
            cursor="hand2",
            pady=6,
            highlightthickness=1
        )
        complete_btn.pack(fill="x", padx=40, pady=20)
