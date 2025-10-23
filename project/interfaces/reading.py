import tkinter as tk
from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_right import create_sidebar_right
from controller.unit_controller import get_all_units

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

# --------------------------------------
# 1) Tạo main_frame TRƯỚC nhưng KHÔNG pack
# --------------------------------------
main_frame = create_main_frame(root)

# --------------------------------------
# 2) Hàm show_in_main (bo tròn, co giãn tự động)
# --------------------------------------
def show_in_main(title, contents):
    for w in main_frame.winfo_children():
        w.destroy()

    # 🟢 Tiêu đề
    if title:
        tk.Label(
            main_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

    # 🔹 Nút nội dung (nếu có)
    if contents:
        for item in contents:
            tk.Button(
                main_frame,
                text=item,
                font=("Arial", 14),
                command=lambda x=item: show_message(f"{title} - {x}"),
                bg="#3498db",
                fg="white",
                width=30,
                height=2,
                bd=3
            ).pack(pady=8)

    # --------------------------------------
    # 🟢 Thanh tiến độ bo tròn (Canvas)
    # --------------------------------------
    BAR_HEIGHT = 20
    RADIUS = 10
    progress = 0

    # Canvas chiếm gần hết chiều ngang main_frame
    canvas = tk.Canvas(main_frame, height=BAR_HEIGHT, bg="white", highlightthickness=0)
    canvas.place(relx=0.05, rely=0.1, relwidth=0.9)  # ⬅ dùng relwidth để tự co giãn

    def create_round_rect(canvas, x1, y1, x2, y2, r=10, **kwargs):
        r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
        return [
            canvas.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x2-r*2, y1, x2, y1+r*2, start=0, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x2-r*2, y2-r*2, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_arc(x1, y2-r*2, x1+r*2, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs),
            canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs),
            canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)
        ]

    # 🟢 Hàm vẽ lại thanh tiến độ
    def draw_progress_bar(value):
        """Vẽ lại thanh tiến độ bo tròn, dựa theo kích thước hiện tại"""
        canvas.delete("bar", "bg")
        BAR_WIDTH = canvas.winfo_width()

        # Nền
        create_round_rect(canvas, 0, 0, BAR_WIDTH, BAR_HEIGHT, r=RADIUS, fill="#E0E0E0", outline="", tags="bg")

        # Thanh tiến độ
        width = (BAR_WIDTH / 100) * value
        r = RADIUS
        if value <= 0:
            return
        elif value >= 100:
            create_round_rect(canvas, 0, 0, BAR_WIDTH, BAR_HEIGHT, r=r, fill="#4CAF50", outline="", tags="bar")
        else:
            # Bo tròn đầu trái
            canvas.create_arc(0, 0, r*2, r*2, start=90, extent=90, style=tk.PIESLICE,
                              fill="#4CAF50", outline="", tags="bar")
            canvas.create_arc(0, BAR_HEIGHT-r*2, r*2, BAR_HEIGHT, start=180, extent=90, style=tk.PIESLICE,
                              fill="#4CAF50", outline="", tags="bar")
            canvas.create_rectangle(r, 0, width, BAR_HEIGHT, fill="#4CAF50", outline="", tags="bar")

    # Nhãn hiển thị %
    progress_label = tk.Label(main_frame, text="Tiến độ xử lý: 0%", font=("Arial", 12), bg="white")
    progress_label.place(relx=0.43, rely=0.05)

    # 🟢 Hàm tăng tiến độ
    def increase_progress():
        nonlocal progress
        if progress < 100:
            progress += 20
            draw_progress_bar(progress)
            progress_label.config(text=f"Tiến độ xử lý: {progress}%")
            if progress == 100:
                progress_label.config(text="Hoàn thành ✅")

    # 🟢 Hàm giảm tiến độ
    def decrease_progress():
        nonlocal progress
        if progress > 0:
            progress -= 20
            draw_progress_bar(progress)
            progress_label.config(text=f"Tiến độ xử lý: {progress}%")
        else:
            progress_label.config(text="Đã về mức 0% 🔁")

    # 🟢 Sự kiện khi resize cửa sổ
    def on_resize(event):
        draw_progress_bar(progress)

    canvas.bind("<Configure>", on_resize)

    # 🟢 Nút quay về
    tk.Button(
        main_frame,
        text="Quay về",
        command=decrease_progress,
        bg="#f44336",
        fg="white",
        font=("Arial", 12, "bold"),
        width=10
    ).place(relx=0.1, rely=0.9)

    # 🟢 Nút tiếp theo
    tk.Button(
        main_frame,
        text="Tiếp theo",
        command=increase_progress,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        width=10
    ).place(relx=0.8, rely=0.9)

    # Vẽ lần đầu
    draw_progress_bar(progress)

# --------------------------------------
# 3) Sidebar trái & phải
# --------------------------------------
create_sidebar_left(root, show_in_main)
create_sidebar_right(root)

# --------------------------------------
# 4) Hiển thị main_frame
# --------------------------------------
main_frame.pack(side="left", fill="both", expand=True)

# --------------------------------------
# 5) Mặc định hiển thị
# --------------------------------------
show_in_main("", [])

root.mainloop()
