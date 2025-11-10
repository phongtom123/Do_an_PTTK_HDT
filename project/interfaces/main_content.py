import tkinter as tk
from controller.unit_controller import get_all_units
from controller.lesson_controller import get_lessons_by_unit_id
from ranking import Ranking
from reading_content import show_reading_practice
from listening_content import show_listening_practice


def initialize_main_content(root):
    """Khởi tạo vùng nội dung chính và các hàm điều khiển."""

    main_frame = tk.Frame(root, bg="white")
    sidebar_right_ref = [None]
    in_learning_mode = [False]
    current_mode = [None]

    # === SIDEBAR PHẢI ===
    from sidebar_right import create_sidebar_right

    def recreate_sidebar_right():
        sidebar = create_sidebar_right(root)
        sidebar_right_ref[0] = sidebar
        return sidebar

    recreate_sidebar_right()

    def hide_sidebar_right():
        if sidebar_right_ref[0] is not None:
            try:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
            except Exception:
                pass
            sidebar_right_ref[0] = None
        root.update_idletasks()

    def reset_sidebar():
        hide_sidebar_right()
        recreate_sidebar_right()

    # === HEADER ===
    def create_header(parent, part_text="Phần 9", title_text="Bài mới mỗi ngày",
                      color="#1da9fe", back_callback=None):
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

    # === DANH SÁCH UNIT ===
    def show_lesson_list():
        current_mode[0] = None
        root.current_mode = None
        reset_sidebar()

        for w in main_frame.winfo_children():
            w.destroy()

        create_header(main_frame, part_text="Unit", title_text="Bài mới mỗi ngày")

        units = get_all_units()

        container_frame = tk.Frame(main_frame, bg="#f9f9f9")
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container_frame, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")
        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig(window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for unit in units:
            unit_name = unit[1] if isinstance(unit, (tuple, list)) else str(unit)

            outer = tk.Frame(scrollable_frame, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")

            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)

            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)

            tk.Label(left, text=unit_name, font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
            tk.Label(left, text="✅ HOÀN THÀNH", font=("Arial", 11, "bold"),
                     bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))

            def open_unit_lessons(u):
                if isinstance(u, (tuple, list)):
                    unit_id = u[0]
                    unit_name = u[1]
                elif hasattr(u, "get_unit_id"):
                    unit_id = u.get_unit_id()
                    unit_name = u.get_unit_name()
                else:
                    unit_id = None
                    unit_name = str(u)
                lessons = get_lessons_by_unit_id(unit_id)
                if not lessons:
                    lessons = [f"(Chưa có bài học trong {unit_name})"]
                show_in_main(unit_name, lessons, root.current_mode if hasattr(root, "current_mode") else None)

            tk.Button(inner, text="ÔN TẬP", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      activebackground="#ecf5ff", cursor="hand2",
                      width=10, height=1,
                      command=lambda u=unit: open_unit_lessons(u)).pack(side="right")

    # === HIỂN THỊ NỘI DUNG CHÍNH ===
    def show_in_main(title, contents, mode=None):
        if in_learning_mode[0]:
            reset_sidebar()

        if title in ("Reading", "Listening", "Từ vựng", "Xếp hạng", "Xem thêm", "Hồ sơ"):
            current_mode[0] = title
            root.current_mode = title

        if title == "__BACK__":
            show_lesson_list()
            return

        if title == "Xếp hạng":
            for w in main_frame.winfo_children():
                w.destroy()
            hide_sidebar_right()
            create_header(main_frame, part_text="Bảng xếp hạng",
                          title_text="Top người học BLEU", back_callback=show_lesson_list)
            ranking_view = Ranking(main_frame)
            ranking_view.pack(fill="both", expand=True, padx=20, pady=10)
            return

        if sidebar_right_ref[0] is None:
            recreate_sidebar_right()

        for w in main_frame.winfo_children():
            w.destroy()

        create_header(main_frame, part_text="Units",
                      title_text=f"Nội dung {title}", back_callback=show_lesson_list)

        lessons = []
        for item in contents:
            if hasattr(item, "get_lesson_name"):
                lesson_title = item.get_lesson_name()
            elif isinstance(item, (tuple, list)) and len(item) > 1:
                lesson_title = item[1]
            else:
                lesson_title = str(item)
            if "của Unit" in lesson_title:
                lesson_title = lesson_title.split("của Unit")[0].strip()

            def lesson_callback(x=item):
                if sidebar_right_ref[0] is not None:
                    sidebar_right_ref[0].pack_forget()
                    sidebar_right_ref[0].destroy()
                    sidebar_right_ref[0] = None
                show_lesson_modes(x)

            lessons.append({"title": lesson_title, "button_cmd": lesson_callback})

        container = tk.Frame(main_frame, bg="#f9f9f9")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        for lesson in lessons:
            outer = tk.Frame(container, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")
            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)
            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=lesson["title"], font=("Arial", 13, "bold"),
                     bg="white", fg="#333").pack(anchor="w")
            tk.Label(left, text="✅ Chưa học", font=("Arial", 11, "bold"),
                     bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))
            tk.Button(inner, text="HỌC", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      activebackground="#ecf5ff", cursor="hand2",
                      width=10, height=1, command=lesson["button_cmd"]).pack(side="right")

    # === LESSON MODES (READING/LISTENING) ===
    def show_lesson_modes(lesson_item):
        for w in main_frame.winfo_children():
            w.destroy()

        # ✅ Lấy đúng tên bài học (chỉ hiển thị tên)
        if hasattr(lesson_item, "get_lesson_name"):
            lesson_name = lesson_item.get_lesson_name()
        elif isinstance(lesson_item, (tuple, list)) and len(lesson_item) > 1:
            lesson_name = lesson_item[1]
        else:
            lesson_name = str(lesson_item)
        if "của Unit" in lesson_name:
            lesson_name = lesson_name.split("của Unit")[0].strip()

        create_header(main_frame, part_text="Lesson", title_text=lesson_name, back_callback=show_lesson_list)

        container = tk.Frame(main_frame, bg="#f9f9f9")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        modes = [
            {"key": "Reading", "label": "Reading", "desc": "Luyện đọc hiểu"},
            {"key": "Listening", "label": "Listening", "desc": "Luyện nghe hiểu"},
        ]

        for mode in modes:
            outer = tk.Frame(container, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            outer.pack(pady=10, fill="x")
            inner = tk.Frame(outer, bg="white")
            inner.pack(fill="x", padx=20, pady=15)
            left = tk.Frame(inner, bg="white")
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=mode["label"], font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
            tk.Label(left, text=mode["desc"], font=("Arial", 11), bg="white", fg="#666").pack(anchor="w", pady=(5, 0))
            tk.Button(inner, text="HỌC", font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", bd=1, relief="solid",
                      activebackground="#ecf5ff", cursor="hand2",
                      width=10, height=1,
                      command=lambda m=mode["key"]: open_learning_mode(m, lesson_item)).pack(side="right")

    def open_learning_mode(mode_name, lesson_item=None):
        """Khi người dùng chọn HỌC trên ô Reading/Listening"""
        if sidebar_right_ref[0] is not None:
            sidebar_right_ref[0].pack_forget()
            sidebar_right_ref[0].destroy()
            sidebar_right_ref[0] = None

        lesson_id = lesson_item[0] if isinstance(lesson_item, (tuple, list)) else None

        if mode_name == "Reading":
            from controller.reading_controller import get_readings_by_lesson_id
            readings = get_readings_by_lesson_id(lesson_id)
            show_reading_practice(root, main_frame, sidebar_right_ref,
                                  recreate_sidebar_right, show_in_main, in_learning_mode, readings)
        elif mode_name == "Listening":
            from controller.listening_controller import get_listenings_by_lesson_id
            listenings = get_listenings_by_lesson_id(lesson_id)
            show_listening_practice(root, main_frame, sidebar_right_ref,
                                    recreate_sidebar_right, show_in_main, in_learning_mode, listenings)
        else:
            from lesson_content import show_lesson_content
            show_lesson_content(root, main_frame, show_in_main, in_learning_mode)

    return main_frame, show_lesson_list, show_in_main
