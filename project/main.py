# main.py
import tkinter as tk
from main_content import create_main_frame, show_message
from sidebar_left import create_sidebar_left
from sidebar_right import create_sidebar_right

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

# 1) Tạo main_frame TRƯỚC nhưng KHÔNG pack
main_frame = create_main_frame(root)   # create_main_frame chỉ return Frame, không pack

# 2) Định nghĩa show_in_main để sidebar gọi vào (dùng main_frame)
def show_in_main(title, contents):
    for w in main_frame.winfo_children():
        w.destroy()
    tk.Label(main_frame, text=title, font=("Arial",16,"bold"), bg="white").pack(pady=10)
    for item in contents:
        tk.Button(main_frame, text=item, font=("Arial",14),
                  command=lambda x=item: show_message(f"{title} - {x}"),
                  bg="#3498db", fg="white", width=30, height=2, bd=3).pack(pady=8)

# 3) Tạo sidebar trái (pack left) — truyền callback
create_sidebar_left(root, show_in_main)

# 4) Tạo sidebar phải (pack right)
create_sidebar_right(root)

# 5) Bây giờ pack main_frame giữa
main_frame.pack(side="left", fill="both", expand=True)

# 6) Hiển thị Home mặc định
show_in_main("Home", ["Welcome to Home"])

root.mainloop()
