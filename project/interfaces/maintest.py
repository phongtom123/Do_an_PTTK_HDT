import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

# =================== MOCK / IMPORT ===================
try:
    from main_content import create_main_frame, show_message
except ImportError:
    def create_main_frame(root):
        frame = tk.Frame(root, bg="#FFFFFF")
        return frame

    def show_message(msg):
        popup = tk.Toplevel()
        popup.title("Thông báo")
        tk.Label(popup, text=msg, font=("Arial", 12)).pack(padx=20, pady=20)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=(0, 15))

try:
    from sidebar_left import create_sidebar_left
except ImportError:
    def create_sidebar_left(root, show_in_main):
        sidebar = tk.Frame(root, bg="#f5f5f5", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="📚 DANH MỤC", bg="#f5f5f5",
                 font=("Arial", 12, "bold"), pady=10).pack()

        tk.Button(sidebar, text="🏠 Trang chính", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", relief="flat", cursor="hand2",
                  command=lambda: show_in_main("__BACK__", [])
                  ).pack(fill="x", padx=15, pady=(5, 15))

        for name in ["Reading", "Listening", "Writing"]:
            tk.Button(sidebar, text=name, font=("Arial", 11, "bold"),
                      fg="#1da9fe", bg="white", relief="flat", cursor="hand2",
                      command=lambda n=name: show_in_main(n, [f"{n} 1", f"{n} 2"])
                      ).pack(fill="x", padx=15, pady=5)
        return sidebar

try:
    from sidebar_right import create_sidebar_right
except ImportError:
    def create_sidebar_right(root):
        sidebar = tk.Frame(root, bg="#fafafa", width=220)
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="📖 THÔNG TIN", bg="#fafafa",
                 font=("Arial", 12, "bold"), pady=10).pack()
        tk.Label(sidebar, text="Chọn một bài học để bắt đầu.",
                 bg="#fafafa", wraplength=180).pack(padx=10, pady=10)
        return sidebar

try:
    from controller.unit_controller import get_all_units
except ImportError:
    def get_all_units():
        # fallback giả lập dữ liệu
        return [(1, "Unit 1"), (2, "Unit 2"), (3, "Unit 3")]

try:
    from reading_content import show_reading_practice
except ImportError:
    def show_reading_practice(root, main_frame, sidebar_right_ref,
                              recreate_sidebar_right, show_in_main, in_reading_mode):
        in_reading_mode[0] = True
        for w in main_frame.winfo_children():
            w.destroy()
        tk.Label(main_frame, text="📘 Reading Practice",
                 font=("Arial", 16, "bold"), bg="white").pack(pady=30)
        tk.Button(main_frame, text="← Quay lại",
                  command=lambda: show_in_main("__BACK__", [])).pack()

# =================== MAIN APP ===================
root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

main_frame = create_main_frame(root)
sidebar_right_ref = [None]

def recreate_sidebar_right():
    sidebar = create_sidebar_right(root)
    sidebar_right_ref[0] = sidebar
    return sidebar

recreate_sidebar_right()
in_reading_mode = [False]

def reset_sidebar():
    """Khôi phục sidebar phải khi quay lại"""
    if in_reading_mode[0]:
        if sidebar_right_ref[0] is not None:
            try:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
            except Exception:
                pass
            sidebar_right_ref[0] = None
        root.update_idletasks()
        recreate_sidebar_right()
        in_reading_mode[0] = False

# =================== HEADER ===================
def create_header(root, part_text="Phần 9", title_text="Bài mới mỗi ngày",
                  color="#1da9fe", back_callback=None):
    wrapper = tk.Frame(root, bg="#f9f9f9")
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

# =================== LESSON LIST ===================
def show_lesson_list():
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

    # ✅ Hiển thị Units đúng định dạng
    for unit in units:
        # Nếu là tuple: (id, name, ...)
        if isinstance(unit, (tuple, list)):
            unit_name = unit[1]
        else:
            unit_name = getattr(unit, "unit_name", str(unit))

        outer = tk.Frame(scrollable_frame, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
        outer.pack(pady=10, fill="x")

        inner = tk.Frame(outer, bg="white")
        inner.pack(fill="x", padx=20, pady=15)

        left = tk.Frame(inner, bg="white")
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=unit_name, font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
        tk.Label(left, text="✅ HOÀN THÀNH", font=("Arial", 11, "bold"), bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))

        def open_unit_lessons(u):
            lessons = [f"Lesson {i}" for i in range(1, 6)]
            show_in_main(u, lessons)

        tk.Button(inner, text="ÔN TẬP", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", bd=1, relief="solid",
                  activebackground="#ecf5ff", cursor="hand2",
                  width=10, height=1,
                  command=lambda u=unit_name: open_unit_lessons(u)).pack(side="right")

# =================== SHOW IN MAIN ===================
def show_in_main(title, contents):
    reset_sidebar()
    # Nếu là trở về trang chính (avatar hoặc back)
    if title == "__BACK__":
        show_lesson_list()
        return

    # --- Xóa nội dung cũ ---
    for w in main_frame.winfo_children():
        w.destroy()

    # --- Tạo header mới ---
    create_header(
        main_frame,
        part_text="Units",
        title_text=f"Nội dung {title}",
        back_callback=show_lesson_list
    )

    lessons = []
    for item in contents:
        lesson = {"title": str(item), "status": "Chưa học"}

        def lesson_callback(x=item):
            # --- Tạm thời ẩn sidebar phải ---
            if sidebar_right_ref[0] is not None:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
                sidebar_right_ref[0] = None
            # --- Mở Reading ---
            show_reading_practice(root, main_frame, sidebar_right_ref,
                                  recreate_sidebar_right, show_in_main, in_reading_mode)

        lesson["button_cmd"] = lesson_callback
        lessons.append(lesson)

    container = tk.Frame(main_frame, bg="#f9f9f9")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    for lesson in lessons:
        outer = tk.Frame(container, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
        outer.pack(pady=10, fill="x")
        inner = tk.Frame(outer, bg="white")
        inner.pack(fill="x", padx=20, pady=15)
        left = tk.Frame(inner, bg="white")
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=lesson["title"], font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
        tk.Label(left, text=f"✅ {lesson['status']}", font=("Arial", 11, "bold"), bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))
        tk.Button(inner, text="HỌC", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", bd=1, relief="solid",
                  activebackground="#ecf5ff", cursor="hand2",
                  width=10, height=1,
                  command=lesson["button_cmd"]).pack(side="right")

# =================== START ===================
create_sidebar_left(root, show_in_main)
main_frame.pack(side="left", fill="both", expand=True)
show_lesson_list()

root.mainloop()
