import tkinter as tk
from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_right import create_sidebar_right
from controller.unit_controller import get_all_units
from reading_content import show_reading_practice  # ✅ import Reading UI
from listening_content import show_listening_practice

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

#main frame 
main_frame = create_main_frame(root)

# sidebar phải (có thể bị thay thế) 
sidebar_right_ref = [None]

def recreate_sidebar_right():
    sidebar = create_sidebar_right(root)
    sidebar_right_ref[0] = sidebar
    return sidebar

# Tạo sidebar_right mặc định
recreate_sidebar_right()

# trạng thái toàn cục 
in_reading_mode = [False]  # True khi đang trong bài học

def reset_sidebar():
    """Hàm dùng chung để phục hồi sidebar_right nếu đang ở chế độ học."""
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

#  hàm hiển thị nội dung chính 
def show_in_main(title, contents):
    reset_sidebar()  #  luôn reset nếu đang ở trong bài học

    for w in main_frame.winfo_children():
        w.destroy()

    tk.Label(main_frame, text=title, font=("Arial",16,"bold"), bg="white").pack(pady=10)

    for item in contents:
        if title == "Reading":
            tk.Button(
            main_frame, text=item, font=("Arial",14),
            bg="#3498db", fg="white", width=30, height=2, bd=3,
            command=lambda: show_reading_practice(
                root, main_frame, sidebar_right_ref,
                recreate_sidebar_right, show_in_main, in_reading_mode
            )
        ).pack(pady=8)

        elif title == "Listening":  
            tk.Button(
            main_frame, text=item, font=("Arial",14),
            bg="#1abc9c", fg="white", width=30, height=2, bd=3,
            command=lambda: show_listening_practice(
                root, main_frame, sidebar_right_ref,
                recreate_sidebar_right, show_in_main, in_reading_mode
            )
        ).pack(pady=8)

    else:
        tk.Button(
            main_frame, text=       item, font=("Arial",14),
            bg="#3498db", fg="white", width=30, height=2, bd=3,
            command=lambda x=item: show_message(f"{title} - {x}")
        ).pack(pady=8)


# --- sidebar trái ---
create_sidebar_left(root, show_in_main)

# --- hiển thị main ---
main_frame.pack(side="left", fill="both", expand=True)

# --- hiển thị trang Home ---
show_in_main("Home", ["Welcome to Home"])

root.mainloop()
