import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

# --- import các module chính ---
from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_right import create_sidebar_right
from controller.unit_controller import get_all_units
from reading_content import show_reading_practice
from listening_content import show_listening_practice
from game import create_game_screen
from history import create_history_screen
from ranking import Ranking

# --- Khởi tạo ---
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

# --- Biến nhớ chế độ hiện tại ---
current_mode = [None]

# --- Reset sidebar phải ---
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

# --- Header ---
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

# --- Danh sách unit (Trang chủ) ---
def show_lesson_list():
    reset_sidebar()
    current_mode[0] = "Home" # Đặt lại chế độ
    for w in main_frame.winfo_children():
        w.destroy()

    create_header(main_frame, part_text="Unit", title_text="Bài mới mỗi ngày")

    units = get_all_units()

    container_frame = tk.Frame(main_frame, bg="#f9f9f9")
    container_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ... (Code Canvas và Scrollbar của bạn) ...
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
            lessons = [f"Lesson {i}" for i in range(1, 6)]
            # Truyền luôn chế độ hiện tại (lúc này là "Home")
            show_in_main(u, lessons, current_mode[0])

        tk.Button(inner, text="ÔN TẬP", font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white", bd=1, relief="solid",
                  activebackground="#ecf5ff", cursor="hand2",
                  width=10, height=1,
                  command=lambda u=unit_name: open_unit_lessons(u)).pack(side="right")

# --- BỘ ĐIỀU KHIỂN HIỂN THỊ CHÍNH ---
def show_in_main(title, contents, mode=None):
    reset_sidebar()

    # === KHỐI 1: XỬ LÝ CÁC TRANG TRỰC TIẾP ===
    # (Các trang này không phải là danh sách)

    if title == "__BACK__":
        show_lesson_list() # Quay về trang chủ
        return

    if title == "Game":
        current_mode[0] = "Game"
        create_game_screen(main_frame)
        return 

    # SỬA 1: Đảm bảo string khớp với sidebar_left.py (Thường là "History")
    if title == "History": 
        current_mode[0] = "History"
        create_history_screen(main_frame)
        return
    
    # SỬA 2: Đảm bảo string khớp với sidebar_left.py ("Xếp hạng")
    if title == "Xếp hạng":
        current_mode[0] = "Xếp hạng"
        for w in main_frame.winfo_children():
            w.destroy()
        ranking_page = Ranking(main_frame)
        ranking_page.pack(fill="both", expand=True)
        return 

    # === KHỐI 2: XỬ LÝ CÁC TRANG HIỂN THỊ DANH SÁCH ===
    # (Nếu code chạy đến đây, nghĩa là title là "Reading", "Listening", "Trò chơi", v.v.)

    # SỬA 3: Ghi lại chế độ cho TẤT CẢ các loại danh sách
    if title in ("Reading", "Listening", "Trò chơi"):
        current_mode[0] = title
    
    # Xóa frame
    for w in main_frame.winfo_children():
        w.destroy()

    # SỬA 4: Thêm logic màu sắc cho header "Trò chơi"
    if title == "Trò chơi":
        color = "#0078d4" # Màu xanh đậm của Game
        back_part = "Home"
    else: 
        color = "#1da9fe" # Màu xanh nhạt của Reading/Listening
        back_part = "Units"
        
    create_header(main_frame, part_text=back_part,
                  title_text=f"Nội dung {title}", 
                  color=color,
                  back_callback=show_lesson_list) # Luôn quay về trang chủ (list units)

    # Tạo nội dung danh sách
    lessons = []
    for item in contents:
        lesson = {"title": str(item), "status": "Chưa học"}

        def lesson_callback(x=item):
            if sidebar_right_ref[0] is not None:
                sidebar_right_ref[0].pack_forget()
                sidebar_right_ref[0].destroy()
                sidebar_right_ref[0] = None

            # SỬA 5: Thêm logic cho nút "HỌC" của "Trò chơi"
            if current_mode[0] == "Listening":
                show_listening_practice(root, main_frame, sidebar_right_ref,
                                        recreate_sidebar_right, show_in_main, in_learning_mode)
            elif current_mode[0] == "Trò chơi":
                # Khi bấm "HỌC" trong danh sách "Trò chơi" -> Mở game
                create_game_screen(main_frame)
            else:
                # Mặc định là Reading
                show_reading_practice(root, main_frame, sidebar_right_ref,
                                      recreate_sidebar_right, show_in_main, in_learning_mode)

        lesson["button_cmd"] = lesson_callback
        lessons.append(lesson)

    # Vẽ danh sách
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

# --- Giao diện chính ---
create_sidebar_left(root, show_in_main)
main_frame.pack(side="left", fill="both", expand=True)
show_lesson_list() # Bắt đầu ở trang chủ

root.mainloop()