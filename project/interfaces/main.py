import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_right import create_sidebar_right
from controller.unit_controller import get_all_units
from reading_content import show_reading_practice
from listening_content import show_listening_practice
from controller.lesson_controller import get_lessons_by_unit_id
from ranking import Ranking  


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
in_learning_mode = [False]

# giữ biến cục bộ nhưng cũng đồng bộ với root.current_mode
current_mode = [None]

def reset_sidebar():
    if in_learning_mode[0]:
        if sidebar_right_ref[0] is not None:
            try:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
            except Exception:
                pass
            sidebar_right_ref[0] = None
        root.update_idletasks()
        recreate_sidebar_right()
        in_learning_mode[0] = False

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

def show_lesson_list():
    # Khi trở về danh sách unit => reset trạng thái mode
    current_mode[0] = None
    root.current_mode = None
    # cũng bỏ active_button nếu có
    if hasattr(root, "active_button") and root.active_button is not None:
        try:
            root.active_button.config(bg="#FFFFFF", fg="#000000")
        except Exception:
            pass
        root.active_button = None

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
            # lấy unit_id từ đối tượng unit (nếu là tuple hoặc object)
            if isinstance(u, (tuple, list)):
                unit_id = u[0]
                unit_name = u[1]
            elif hasattr(u, "get_unit_id"):
                unit_id = u.get_unit_id()
                unit_name = u.get_unit_name()
            else:
                # fallback nếu chỉ có tên
                unit_id = None
                unit_name = str(u)

            lessons = get_lessons_by_unit_id(unit_id)
            if not lessons:
                lessons = [f"(Chưa có bài học trong {unit_name})"]

            # Gửi qua giao diện chính
            show_in_main(unit_name, lessons, root.current_mode if hasattr(root, "current_mode") else None)

        tk.Button(inner, text="ÔN TẬP", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", bd=1, relief="solid",
                  activebackground="#ecf5ff", cursor="hand2",
                  width=10, height=1,
                  command=lambda u=unit_name: open_unit_lessons(u)).pack(side="right")

def show_in_main(title, contents, mode=None):
    reset_sidebar()

    # Khi người dùng click 1 menu chính, cập nhật cả hai nơi
    if title in ("Reading", "Listening", "Từ vựng", "Xếp hạng", "Xem thêm", "Hồ sơ"):
        current_mode[0] = title
        root.current_mode = title

    if title == "__BACK__":
        show_lesson_list()
        return

    for w in main_frame.winfo_children():
        w.destroy()

    # ✅ THÊM MỚI: khi chọn "Xếp hạng", hiển thị giao diện ranking.py
    if title == "Xếp hạng":
        from ranking import Ranking
        create_header(
            main_frame,
            part_text="Bảng xếp hạng",
            title_text="Top người học BLEU",
            back_callback=show_lesson_list
        )
        ranking_view = Ranking(main_frame)
        ranking_view.pack(fill="both", expand=True, padx=20, pady=10)
        return

    create_header(main_frame, part_text="Units",
                  title_text=f"Nội dung {title}", back_callback=show_lesson_list)

    lessons = []
    for item in contents:
        lesson = {"title": str(item), "status": "Chưa học"}

        def lesson_callback(x=item):
            if sidebar_right_ref[0] is not None:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
                sidebar_right_ref[0] = None

            mode_now = getattr(root, "current_mode", None)
            if not mode_now:
                mode_now = current_mode[0]

            if mode_now == "Listening":
                show_listening_practice(root, main_frame, sidebar_right_ref,
                                        recreate_sidebar_right, show_in_main, in_learning_mode)
            elif mode_now == "Reading":
                show_reading_practice(root, main_frame, sidebar_right_ref,
                                      recreate_sidebar_right, show_in_main, in_learning_mode)
            else:
                from lesson_content import show_lesson_content
                show_lesson_content(root, main_frame, show_in_main, in_learning_mode)

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
        tk.Label(left, text=lesson["title"], font=("Arial", 13, "bold"),
                 bg="white", fg="#333").pack(anchor="w")
        tk.Label(left, text=f"✅ {lesson['status']}",
                 font=("Arial", 11, "bold"), bg="white", fg="#00AA00").pack(anchor="w", pady=(5, 0))
        tk.Button(inner, text="HỌC", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", bd=1, relief="solid",
                  activebackground="#ecf5ff", cursor="hand2",
                  width=10, height=1,
                  command=lesson["button_cmd"]).pack(side="right")

create_sidebar_left(root, show_in_main)
main_frame.pack(side="left", fill="both", expand=True)
show_lesson_list()

root.mainloop()
