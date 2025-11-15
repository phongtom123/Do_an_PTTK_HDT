import tkinter as tk

from logic.unit.UnitManager import UnitManager
from logic.lesson.LessonManager import LessonManager
from logic.reading.ReadingManager import ReadingManager
from logic.listening.ListeningManager import ListeningManager
from logic.test.TestManager import TestManager
from logic.question.QuestionManager import QuestionManager
from logic.word.WordManager import WordManager   # ← THÊM VÀO


class TestAfterLogin(tk.Toplevel):

    def __init__(self, user):
        super().__init__()
        self.title("TEST LOGIN → USER + UNIT + LESSON")
        self.geometry("650x700")
        self.configure(bg="white")

        self.user = user

        # MANAGERS
        self.lesson_mgr = LessonManager()
        self.unit_mgr = UnitManager()
        self.reading_mgr = ReadingManager()
        self.listening_mgr = ListeningManager()
        self.test_mgr = TestManager()
        self.question_mgr = QuestionManager()
        self.word_mgr = WordManager()     # ← THÊM VÀO

        self.show_main_screen()

    # ============================
    # CLEAR
    # ============================
    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ============================
    # MÀN HÌNH USER + UNIT
    # ============================
    def show_main_screen(self):
        self.clear()

        tk.Label(self, text="THÔNG TIN ĐĂNG NHẬP",
                 font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        tk.Label(self, text=f"User Name: {self.user.get_user_name()}",
                 font=("Arial", 14), bg="white").pack()

        tk.Label(self, text=f"User ID: {self.user.get_user_id()}",
                 font=("Arial", 14), bg="white").pack()

        tk.Label(self, text="\nDanh sách Unit:",
                 font=("Arial", 16, "bold"), bg="white").pack()

        units = self.unit_mgr.get_all()

        if not units:
            tk.Label(self, text="Không có Unit!", fg="red",
                     bg="white", font=("Arial", 12)).pack()
            return

        for unit in units:
            frame = tk.Frame(self, bg="white",
                             highlightbackground="#ccc",
                             highlightthickness=1)
            frame.pack(fill="x", padx=20, pady=6)

            tk.Label(frame,
                     text=f"{unit.get_unit_name()} (ID: {unit.get_unit_id()})",
                     font=("Arial", 12),
                     bg="white").pack(side="left", padx=10)

            tk.Button(frame, text="Học",
                      bg="#1da9fe", fg="white",
                      font=("Arial", 11, "bold"),
                      command=lambda u=unit: self.open_lessons(u)
                      ).pack(side="right", padx=10)

    # ============================
    # MÀN HÌNH HIỂN THỊ LESSON + WORD
    # ============================
    def open_lessons(self, unit):
        self.clear()

        tk.Label(self,
                 text=f"Các bài học của Unit: {unit.get_unit_name()}",
                 font=("Arial", 18, "bold"),
                 bg="white").pack(pady=10)

        # ============================
        # HIỂN THỊ TỪ VỰNG TRONG UNIT
        # ============================
        tk.Label(self, text="📘 Từ vựng của Unit:",
                 font=("Arial", 15, "bold"),
                 bg="white").pack(pady=5)

        words = self.word_mgr.get_by_unit_id(unit.get_unit_id())

        if words:
            for w in words:
                w_frame = tk.Frame(self, bg="white",
                                   highlightbackground="#ddd",
                                   highlightthickness=1)
                w_frame.pack(fill="x", padx=25, pady=3)

                tk.Label(
                    w_frame,
                    text=f"{w.get_word()} → {w.get_word_meaning()}",
                    font=("Arial", 12),
                    bg="white"
                ).pack(anchor="w", padx=10, pady=3)
        else:
            tk.Label(self, text="(Không có từ vựng)",
                     font=("Arial", 11), fg="gray", bg="white").pack()

        # ============================
        # DANH SÁCH LESSON
        # ============================
        tk.Label(self, text="\nDanh sách Lesson:",
                 font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        lessons = self.lesson_mgr.get_by_unit_id(unit.get_unit_id())

        if not lessons:
            tk.Label(self, text="Unit này chưa có Lesson!",
                     font=("Arial", 14),
                     fg="red", bg="white").pack(pady=20)
            return

        for lesson in lessons:
            frame = tk.Frame(self, bg="white",
                             highlightbackground="gray",
                             highlightthickness=1)
            frame.pack(fill="x", padx=20, pady=7)

            tk.Label(frame,
                     text=f"{lesson.get_lesson_name()} (ID: {lesson.get_lesson_id()})",
                     font=("Arial", 14),
                     bg="white").pack(side="left", padx=10)

            tk.Button(frame, text="Reading",
                      bg="#00a65a", fg="white",
                      font=("Arial", 11, "bold"),
                      command=lambda ls=lesson: self.show_readings(ls)
                      ).pack(side="right", padx=5)

            tk.Button(frame, text="Listening",
                      bg="#f39c12", fg="white",
                      font=("Arial", 11, "bold"),
                      command=lambda ls=lesson: self.show_listenings(ls)
                      ).pack(side="right", padx=5)

        tk.Button(self, text="← Quay lại Unit",
                  bg="#1da9fe", fg="white",
                  font=("Arial", 12, "bold"),
                  command=self.show_main_screen).pack(pady=20)

    # ============================
    # HIỂN THỊ READING
    # ============================
    def show_readings(self, lesson):
        self.clear()

        tk.Label(self,
                 text=f"Reading của Lesson: {lesson.get_lesson_name()}",
                 font=("Arial", 18, "bold"),
                 bg="white").pack(pady=10)

        test_id = self.test_mgr.get_test_id_by_lesson(lesson.get_lesson_id())

        if test_id is None:
            tk.Label(self, text="❌ Lesson này chưa có Reading Test!",
                     fg="red", bg="white", font=("Arial", 14)).pack(pady=20)
            tk.Button(self, text="← Quay lại Lessons",
                      bg="#1da9fe", fg="white",
                      font=("Arial", 12, "bold"),
                      command=lambda: self.open_lessons(
                          self.unit_mgr.get_by_id(lesson.get_unit_id()))
                      ).pack(pady=20)
            return

        readings = self.reading_mgr.get_by_test_id(test_id)

        if readings:
            for rd in readings:
                frame = tk.Frame(self, bg="white",
                                 highlightbackground="#ccc",
                                 highlightthickness=1)
                frame.pack(fill="x", padx=20, pady=6)

                tk.Label(frame, text=rd.get_content(),
                         bg="white", font=("Arial", 13),
                         wraplength=500, justify="left").pack(padx=10, pady=10)
        else:
            tk.Label(self, text="Không có Reading!",
                     fg="red", bg="white", font=("Arial", 14)).pack(pady=20)

        tk.Button(self, text="← Quay lại Lessons",
                  bg="#1da9fe", fg="white",
                  font=("Arial", 12, "bold"),
                  command=lambda: self.open_lessons(
                      self.unit_mgr.get_by_id(lesson.get_unit_id()))
                  ).pack(pady=20)

        # ============================
    # HIỂN THỊ LISTENING + QUESTIONS (CÓ KIỂM TRA ĐÚNG SAI)
    # ============================
    def show_listenings(self, lesson):
        self.clear()

        tk.Label(self,
                 text=f"Listening của Lesson: {lesson.get_lesson_name()}",
                 font=("Arial", 18, "bold"),
                 bg="white").pack(pady=10)

        test_id = self.test_mgr.get_test_id_by_lesson(lesson.get_lesson_id())

        if test_id is None:
            tk.Label(self, text="❌ Lesson này chưa có Listening Test!",
                     fg="red", bg="white", font=("Arial", 14)).pack(pady=20)
            tk.Button(self, text="← Quay lại Lessons",
                      bg="#1da9fe", fg="white",
                      font=("Arial", 12, "bold"),
                      command=lambda: self.open_lessons(
                          self.unit_mgr.get_by_id(lesson.get_unit_id()))
                      ).pack(pady=20)
            return

        # === LISTENING CONTENT ===
        listenings = self.listening_mgr.get_by_test_id(test_id)
        if listenings:
            for ls in listenings:
                fr = tk.Frame(self, bg="white",
                              highlightbackground="#ccc",
                              highlightthickness=1)
                fr.pack(fill="x", padx=20, pady=6)

                tk.Label(fr, text=f"Nội dung: {ls.get_content()}",
                         font=("Arial", 12), bg="white",
                         wraplength=500, justify="left").pack(padx=10, pady=5)

                tk.Label(fr, text=f"Audio: {ls.get_audio()}",
                         fg="blue", bg="white",
                         font=("Arial", 12)).pack(padx=10, pady=5)

        # ============================
        # HIỂN THỊ CÂU HỎI TRẮC NGHIỆM ABCD
        # ============================
        tk.Label(self, text="Câu hỏi:",
                 font=("Arial", 16, "bold"),
                 bg="white").pack(pady=10)

        questions = self.question_mgr.get_by_test_id(test_id)

        answers = {}                 # user answers: {question_id: "A"}
        question_frames = []         # để hiển thị đáp án đúng
        chosen_state = {}            # khóa nút mỗi câu

        if not questions:
            tk.Label(self, text="(Không có câu hỏi)",
                     fg="gray", bg="white").pack()
        else:
            for q in questions:
                chosen_state[q.get_question_id()] = False  # chưa trả lời

                q_frame = tk.Frame(
                    self, bg="white",
                    highlightbackground="#bbb",
                    highlightthickness=1,
                    pady=5
                )
                q_frame.pack(fill="x", padx=20, pady=10)
                question_frames.append((q, q_frame))

                # Nội dung câu hỏi
                tk.Label(
                    q_frame,
                    text=q.get_question_content(),
                    font=("Arial", 12),
                    bg="white",
                    wraplength=500,
                    justify="left"
                ).pack(padx=10, pady=5)

                # Xử lý chọn đáp án
                def choose_option(q_obj, key, btn):
                    if chosen_state[q_obj.get_question_id()]:
                        return  # đã trả lời → không cho chọn lại

                    chosen_state[q_obj.get_question_id()] = True
                    answers[q_obj.get_question_id()] = key

                    # Tô màu
                    if key == q_obj.get_question_answer():
                        btn.config(bg="#28a745", fg="white")   # xanh: đúng
                    else:
                        btn.config(bg="#dc3545", fg="white")   # đỏ: sai

                # HIỂN THỊ A/B/C/D
                options = q.get_question_opt()
                if options:
                    for opt_dict in options:
                        for key, value in opt_dict.items():

                            btn = tk.Button(
                                q_frame,
                                text=f"{key}. {value}",
                                bg="#eeeeee",
                                anchor="w",
                                font=("Arial", 12),
                                width=40
                            )
                            btn.pack(anchor="w", padx=20, pady=3)

                            btn.config(
                                command=lambda k=key, b=btn, q_obj=q:
                                choose_option(q_obj, k, b)
                            )
                else:
                    tk.Label(q_frame,
                             text="(Không có lựa chọn)",
                             fg="gray", bg="white",
                             font=("Arial", 11)
                             ).pack(anchor="w", padx=20)

        # ============================
        # NÚT HOÀN THÀNH
        # ============================
        def finish_test():
            correct = 0
            total = len(questions)

            # Hiển thị đáp án đúng
            for q, frame in question_frames:
                correct_ans = q.get_question_answer()
                if answers.get(q.get_question_id()) == correct_ans:
                    correct += 1

                tk.Label(
                    frame,
                    text=f"Đáp án đúng: {correct_ans}",
                    fg="blue",
                    bg="white",
                    font=("Arial", 11)
                ).pack(pady=3)

            # Hiển thị điểm tổng
            tk.Label(
                self,
                text=f"🎉 Kết quả: {correct}/{total} câu đúng",
                font=("Arial", 14, "bold"),
                fg="#28a745",
                bg="white"
            ).pack(pady=10)

            finish_button.pack_forget()
            back_button.pack(pady=20)

        finish_button = tk.Button(
            self,
            text="Hoàn thành",
            font=("Arial", 13, "bold"),
            bg="#007bff",
            fg="white",
            command=finish_test
        )
        finish_button.pack(pady=20)

        # ============================
        # NÚT QUAY LẠI LESSON
        # ============================
        back_button = tk.Button(
            self,
            text="← Quay lại Unit",
            bg="#1da9fe",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: self.open_lessons(
                self.unit_mgr.get_by_id(lesson.get_unit_id()))
        )
