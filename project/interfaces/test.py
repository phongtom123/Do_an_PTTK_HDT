import tkinter as tk

root = tk.Tk()
root.geometry("500x200")
root.configure(bg="white")

# Canvas để vẽ thanh
canvas = tk.Canvas(root, width=400, height=30, bg="#FFFFFF", highlightthickness=0)
canvas.pack(pady=50)

# Hàm tiện ích: vẽ hình chữ nhật bo tròn
def create_round_rect(canvas, x1, y1, x2, y2, r=15, **kwargs):
    # Giới hạn bo góc không vượt quá nửa chiều cao/thấp
    r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    return [
        canvas.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, style=tk.PIESLICE, **kwargs),
        canvas.create_arc(x2-r*2, y1, x2, y1+r*2, start=0, extent=90, style=tk.PIESLICE, **kwargs),
        canvas.create_arc(x2-r*2, y2-r*2, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs),
        canvas.create_arc(x1, y2-r*2, x1+r*2, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs),
        canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs),
        canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)
    ]

# Nền bo tròn
create_round_rect(canvas, 0, 0, 400, 30, r=15, fill="#E0E0E0", outline="")

progress = 0

def draw_progress_bar(value):
    """Vẽ lại thanh tiến độ bo tròn mượt"""
    canvas.delete("bar")
    width = 4 * value  # 100% = 400px
    r = 15

    if value <= 0:
        return
    elif value >= 100:
        # Thanh đầy => bo tròn cả 2 đầu
        create_round_rect(canvas, 0, 0, 400, 30, r=r, fill="#4CAF50", outline="", tags="bar")
    else:
        # Thanh giữa chừng => bo tròn đầu trái, đầu phải vuông
        canvas.create_arc(0, 0, r*2, r*2, start=90, extent=90, style=tk.PIESLICE, fill="#4CAF50", outline="", tags="bar")
        canvas.create_arc(0, 30-r*2, r*2, 30, start=180, extent=90, style=tk.PIESLICE, fill="#4CAF50", outline="", tags="bar")
        canvas.create_rectangle(r, 0, width, 30, fill="#4CAF50", outline="", tags="bar")

# Hàm cập nhật tiến độ
def update_progress(delta):
    global progress
    progress = max(0, min(100, progress + delta))
    draw_progress_bar(progress)

# Vẽ lần đầu
draw_progress_bar(progress)

# Nút điều khiển
tk.Button(root, text="Tăng 10%", command=lambda: update_progress(10)).pack(side="left", padx=20)
tk.Button(root, text="Giảm 10%", command=lambda: update_progress(-10)).pack(side="right", padx=20)

root.mainloop()
