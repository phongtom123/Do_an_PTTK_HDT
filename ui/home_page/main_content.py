import tkinter as tk
from logic.unit_controller import get_all_units
from logic.unit_manager import UnitManager
from logic.lesson_manager import LessonManager
from logic.reading_controller import get_readings_by_lesson_id
from logic.word_controller import get_words_by_lesson_id
from logic.question_controller import QuestionController
from ui.home_page.ranking import Ranking
from ui.home_page.reading_content import ReadingPracticeFrame
from ui.home_page.listening_content import ListeningPracticeFrame
from ui.home_page.sidebar_right import SidebarRight
from ui.home_page.sidebar_learning import SidebarLearning


class MainContentFrame(tk.Frame):
    """Khung nội dung chính của trang học"""
    def __init__(self, root, current_user):
        super().__init__(root, bg="white")
        self.root = root
        self.current_user = current_user
        # Sidebar mặc định
        self.sidebar_right = SidebarRight(root)
        self.sidebar_right.pack(side="right", fill="y", padx=(10, 20), pady=10)

        # Trạng thái
        self.sidebar_learning = None
        self.in_learning_mode = False

        # Hiển thị danh sách bài học mặc định
        self.show_lesson_list()


    def _create_header(self, parent, part_text="Phần 1", title_text="Bài học hôm nay",
                       color="#1da9fe", back_callback=None):
        """Tạo header ở đầu mỗi trang"""
        wrapper = tk.Frame(parent, bg="#f9f9f9")
        wrapper.pack(fill="x", padx=20, pady=15)

        header = tk.Frame(wrapper, bg=color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        back_label = tk.Label(header, text=f"← {part_text}", bg=color, fg="white",
                              font=("Arial", 10, "bold"), anchor="w", cursor="hand2")
        back_label.pack(anchor="w", padx=20, pady=(10, 0))
        if back_callback:
            back_label.bind("<Button-1>", lambda e: back_callback())

        tk.Label(header, text=title_text, bg=color, fg="white",
                 font=("Arial", 14, "bold"), anchor="w").pack(anchor="w", padx=20, pady=(2, 10))
        return header

    # ==========================================================
    # DANH SÁCH UNIT
    # ==========================================================
    def show_lesson_list(self):
        """Hiển thị danh sách Unit"""
        self._restore_sidebar_right()

        for w in self.winfo_children():
            w.destroy()

        self._create_header(self, "Unit", "Danh sách bài học")

        # Lấy ds unit
        unit_manager = UnitManager()

        unit_list = unit_manager.unit_list

        container = tk.Frame(self, bg="#f9f9f9")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Nếu chưa có dữ liệu thì báo ra
        if not unit_list:
            tk.Label(container, text="Chưa có dữ liệu.", bg="#f9f9f9",
                     fg="#666", font=("Arial", 12, "italic")).pack(pady=20)
            return

        for unit in unit_list:
            unit_id, unit_name = unit.get_unit_id(), unit.get_unit_name()

            outer = tk.Frame(container, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")

            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)

            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)

            tk.Label(left, text=unit_name, font=("Arial", 13, "bold"),
                     bg="white", fg="#333").pack(anchor="w")
            
            # Cần chỉnh lại để kiểm tra user trước khi xuất ra
            tk.Button(inner, text="Học nào", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      activebackground="#ecf5ff", cursor="hand2",
                      width=10, height=1,
                      command=lambda u=unit: self._open_unit_lessons(u, self.current_user)).pack(side="right")

    # ==========================================================
    # DANH SÁCH BÀI HỌC THEO UNIT
    # ==========================================================
    def _open_unit_lessons(self, unit, current_user):
        """Hiển thị danh sách Lesson theo Unit"""
        self._restore_sidebar_right()

        for w in self.winfo_children():
            w.destroy()

        unit_id, unit_name = unit[0], unit[1]
        self._create_header(self, part_text="← Danh sách Unit", title_text=unit_name,
                            back_callback=self.show_lesson_list)

        container = tk.Frame(self, bg="#f9f9f9")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        lesson_manager = LessonManager()
        lessons = lesson_manager.get_unit_name()
        if not lessons:
            tk.Label(container, text="Không có bài học nào cho Unit này.",
                     bg="#f9f9f9", fg="#777", font=("Arial", 12, "italic")).pack(pady=30)
            return

        for lesson in lessons:
            lesson_id, lesson_name = lesson.lesson_id, lesson.lesson_name
            outer = tk.Frame(container, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")

            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)

            tk.Label(inner, text=lesson_name, font=("Arial", 13, "bold"),
                     bg="white", fg="#333").pack(anchor="w")

            tk.Button(inner, text="Reading", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      width=10, height=1,
                      command=lambda l=lesson_id: self._open_reading_practice(l)).pack(side="right", padx=10)

            tk.Button(inner, text="Listening", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      width=10, height=1,
                      command=lambda l=lesson_id: self._open_listening_practice(l)).pack(side="right", padx=10)

    # ==========================================================
    # HỌC READING
    # ==========================================================
    def _open_reading_practice(self, lesson_id):
        """Hiển thị giao diện học Reading (lấy nội dung, từ vựng, câu hỏi từ DB)"""
        if self.in_learning_mode:
            return
        self.in_learning_mode = True

        # 🔹 Lấy dữ liệu thực từ DB
        readings = get_readings_by_lesson_id(lesson_id)
        vocab_data = get_words_by_lesson_id(lesson_id)

        # 🔹 Lấy câu hỏi thật
        controller = QuestionController()
        questions = controller.get_by_lesson_id(lesson_id)
        controller.close()

        print(f"[DEBUG] 📚 Có {len(questions)} câu hỏi cho lesson_id={lesson_id}")

        # 🔹 Chuyển sang chế độ học (Sidebar có dữ liệu thật)
        self._switch_to_sidebar_learning("Reading", questions)

        # Xóa nội dung cũ
        for w in self.winfo_children():
            w.destroy()

        # 🔹 Gọi frame Reading
        frame = ReadingPracticeFrame(
            root=self.root,
            main_frame=self,
            sidebar_right_ref=[self.sidebar_learning],
            recreate_sidebar_right=self._restore_sidebar_right,
            show_in_main=lambda mode=None, data=None: self._close_learning_mode(),
            in_learning_mode=[True],
            readings=readings,
            vocab_data=vocab_data,
            lesson_id=lesson_id
        )
        frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=10)

    # ==========================================================
    # HỌC LISTENING
    # ==========================================================
    def _open_listening_practice(self, lesson_id):
        """Hiển thị giao diện học Listening"""
        if self.in_learning_mode:
            return
        self.in_learning_mode = True

        # 🔹 Dữ liệu mẫu (có thể sau này thay bằng DB thật)
        listenings = [{
            "title": f"Listening Sample for Lesson {lesson_id}",
            "audio_path": "./audio/sample.mp3",
            "transcript": "This is a static listening transcript used to test the Listening interface."
        }]

        # 🔹 Lấy câu hỏi thật
        qc = QuestionController()
        questions = qc.get_by_lesson_id(lesson_id)
        qc.close()

        print(f"[DEBUG] 🎧 Có {len(questions)} câu hỏi cho lesson_id={lesson_id}")

        # 🔹 Tạo sidebar học
        self._switch_to_sidebar_learning("Listening", questions)

        # Xóa nội dung cũ
        for w in self.winfo_children():
            w.destroy()

        # 🔹 Gọi frame Listening
        frame = ListeningPracticeFrame(
            root=self.root,
            main_frame=self,
            sidebar_right_ref=[self.sidebar_learning],
            recreate_sidebar_right=self._restore_sidebar_right,
            show_in_main=lambda mode, data: self._close_learning_mode(),
            in_learning_mode=[True],
            listenings=listenings
        )
        frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ==========================================================
    # QUẢN LÝ SIDEBAR
    # ==========================================================
    def _switch_to_sidebar_learning(self, mode, questions):
        """Ẩn sidebar_right và tạo sidebar_learning mới"""
        if self.sidebar_right and self.sidebar_right.winfo_exists():
            self.sidebar_right.pack_forget()

        # Xóa sidebar_learning cũ nếu có
        for child in list(self.root.winfo_children()) + list(self.winfo_children()):
            if isinstance(child, SidebarLearning):
                try:
                    child.destroy()
                except:
                    pass

        # ✅ Tạo sidebar mới với câu hỏi thật
        self.sidebar_learning = SidebarLearning(self.root, self.current_user, mode=mode, questions=questions)
        self.sidebar_learning.pack(side="right", fill="y", padx=(10, 20), pady=10)

    def _restore_sidebar_right(self):
        """Khôi phục sidebar_right khi thoát khỏi chế độ học"""
        for child in list(self.root.winfo_children()) + list(self.winfo_children()):
            if isinstance(child, SidebarLearning):
                try:
                    child.destroy()
                except:
                    pass

        self.sidebar_learning = None

        for child in self.root.winfo_children():
            if isinstance(child, SidebarRight):
                try:
                    child.destroy()
                except:
                    pass

        self.sidebar_right = SidebarRight(self.root)
        self.sidebar_right.pack(side="right", fill="y", padx=(10, 20), pady=10)
        self.in_learning_mode = False

    def _close_learning_mode(self):
        """Thoát khỏi chế độ học"""
        self._restore_sidebar_right()
        self.show_lesson_list()

    # ==========================================================
    # BẢNG XẾP HẠNG
    # ==========================================================
    def _show_ranking(self):
        """Hiển thị bảng xếp hạng"""
        self._restore_sidebar_right()

        for w in self.winfo_children():
            w.destroy()

        self._create_header(self, part_text="Bảng xếp hạng",
                            title_text="Top người học BLEU",
                            back_callback=self.show_lesson_list)

        rank_view = Ranking(self)
        rank_view.pack(fill="both", expand=True, padx=20, pady=10)

