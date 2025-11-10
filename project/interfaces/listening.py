import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading, time
from pygame import mixer

from main_content import create_main_frame
from sidebar_left import create_sidebar_left
from sidebar_learning import create_sidebar_learning

root = tk.Tk()
root.title("BulaBuluuuu")
root.geometry("1100x700")
root.configure(bg="#FFFFFF")

main_frame = create_main_frame(root)
mixer.init()


def show_in_main(title, contents):
    for w in main_frame.winfo_children():
        w.destroy()

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Ảnh minh họa
    try:
        img = Image.open("./photos/Tiger.png").resize((400, 350), Image.LANCZOS)
    except:
        img = Image.new("RGB", (400, 350), "#4CAF50")
    photo = ImageTk.PhotoImage(img)
    tk.Label(content_frame, image=photo, bg="white").pack()
    content_frame.image = photo  # tránh bị GC

    # Khung tiến trình
    progress = ttk.Progressbar(content_frame, orient="horizontal", mode="determinate")
    progress.pack(fill="x", padx=100, pady=(10, 0))
    time_label = tk.Label(content_frame, text="00:00 / 00:00", bg="white", font=("Arial", 12))
    time_label.pack(pady=5)

    # Điều khiển
    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=10)

    # --- Biến trạng thái ---
    audio_path = "./audio/Damidami.mp3"
    total = 0
    current = 0
    is_playing = False
    start_time = 0
    update_thread = None

    # --- Hàm tiện ích ---
    def fmt(sec):  # định dạng thời gian mm:ss
        sec = int(sec)
        return f"{sec//60:02d}:{sec%60:02d}"

    try:
        total = mixer.Sound(audio_path).get_length()
        time_label.config(text=f"00:00 / {fmt(total)}")
    except:
        time_label.config(text="00:00 / 00:00")

    # --- Luồng cập nhật ---
    def updater():
        nonlocal current, start_time, is_playing
        while is_playing:
            elapsed = time.time() - start_time
            now = min(current + elapsed, total)
            progress["value"] = (now / total) * 100 if total else 0
            time_label.config(text=f"{fmt(now)} / {fmt(total)}")
            if now >= total:
                is_playing = False
                play_btn.config(text="▶ Play", bg="#2ecc71")
                current = total
                break
            time.sleep(0.2)

    # --- Các nút chức năng ---
    def play_pause():
        nonlocal is_playing, start_time, current, update_thread
        if not is_playing:  # ▶ phát hoặc tiếp tục
            try:
                mixer.music.load(audio_path)
                mixer.music.play(start=current)
            except Exception as e:
                time_label.config(text=f"Lỗi: {e}")
                return
            start_time = time.time()
            is_playing = True
            play_btn.config(text="⏸ Pause", bg="#e67e22")
            update_thread = threading.Thread(target=updater, daemon=True)
            update_thread.start()
        else:  # ⏸ tạm dừng
            elapsed = time.time() - start_time
            current += elapsed
            mixer.music.pause()
            is_playing = False
            play_btn.config(text="▶ Play", bg="#2ecc71")

    def stop(reset=False):
        nonlocal current, is_playing, start_time
        if is_playing:
            elapsed = time.time() - start_time
            current += elapsed
        mixer.music.stop()
        is_playing = False
        play_btn.config(text="▶ Play", bg="#2ecc71")
        if reset:
            current = 0
            progress["value"] = 0
            time_label.config(text=f"00:00 / {fmt(total)}")

    def seek(event):
        nonlocal current
        width = event.widget.winfo_width()
        pct = event.x / width
        current = pct * total
        progress["value"] = pct * 100
        if is_playing:
            mixer.music.stop()
            mixer.music.play(start=current)
            start_time = time.time()
        time_label.config(text=f"{fmt(current)} / {fmt(total)}")

    # --- Giao diện nút ---
    play_btn = tk.Button(
        btn_frame, text="▶ Play", command=play_pause,
        bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
        relief="flat", bd=2, highlightbackground="black", padx=10, pady=6
    )
    play_btn.pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="■ Stop", command=lambda: stop(False),
        bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
        relief="flat", bd=2, highlightbackground="black", padx=10, pady=6
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="↺ Reset", command=lambda: stop(True),
        bg="#bdc3c7", fg="black", font=("Arial", 11),
        relief="flat", padx=10, pady=6
    ).pack(side="left", padx=10)

    progress.bind("<Button-1>", seek)


create_sidebar_left(root, show_in_main)
create_sidebar_learning(root)
main_frame.pack(side="left", fill="both", expand=True)
show_in_main("", [])
root.mainloop()
