# listening_content.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading, time
from pygame import mixer
from sidebar_learning import create_sidebar_learning

def show_listening_practice(root, main_frame, sidebar_right_ref,
                            recreate_sidebar_right, show_in_main, in_learning_mode):
    """Phiên bản đầy đủ của Listening: giữ nguyên giao diện & chức năng nghe nhạc."""
    in_learning_mode[0] = True

    # --- Chuẩn bị khung ---
    for w in main_frame.winfo_children():
        w.destroy()

    # --- Hủy sidebar_right và thay bằng sidebar_learning ---
    if sidebar_right_ref[0] is not None:
        try:
            sidebar_right_ref[0].pack_forget()
            sidebar_right_ref[0].destroy()
        except Exception:
            pass
        sidebar_right_ref[0] = None
    root.update_idletasks()

    sidebar_learning = create_sidebar_learning(root, mode="Listening")
    sidebar_right_ref[0] = sidebar_learning

    # --- Giao diện chính ---
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content_frame, text="🎧 Listening Practice", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    try:
        img = Image.open("./photos/Tiger.png").resize((400, 350), Image.LANCZOS)
    except Exception:
        from PIL import Image
        img = Image.new("RGB", (400, 350), "#4CAF50")
    photo = ImageTk.PhotoImage(img)
    tk.Label(content_frame, image=photo, bg="white").pack()
    content_frame.image = photo  # tránh bị GC

    # --- Khởi tạo mixer ---
    try:
        mixer.init()
    except Exception as e:
        tk.Label(content_frame, text=f"Lỗi âm thanh: {e}", fg="red", bg="white").pack()
        return

    # --- Biến trạng thái ---
    audio_path = "./audio/Damidami.mp3"
    total = 0
    current = 0
    is_playing = False
    start_time = 0
    update_thread = None

    # --- Thanh tiến trình ---
    progress = ttk.Progressbar(content_frame, orient="horizontal", mode="determinate")
    progress.pack(fill="x", padx=100, pady=(10, 0))
    time_label = tk.Label(content_frame, text="00:00 / 00:00", bg="white", font=("Arial", 12))
    time_label.pack(pady=5)

    # --- Định dạng thời gian ---
    def fmt(sec):
        sec = int(sec)
        return f"{sec//60:02d}:{sec%60:02d}"

    try:
        total = mixer.Sound(audio_path).get_length()
        time_label.config(text=f"00:00 / {fmt(total)}")
    except Exception:
        total = 0
        time_label.config(text="00:00 / 00:00")

    # --- Cập nhật tiến độ ---
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

    # --- Điều khiển ---
    def play_pause():
        nonlocal is_playing, start_time, current, update_thread
        if not is_playing:
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
        else:
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
        nonlocal current, start_time
        width = event.widget.winfo_width()
        pct = event.x / width
        current = pct * total
        progress["value"] = pct * 100
        if is_playing:
            mixer.music.stop()
            mixer.music.play(start=current)
            start_time = time.time()
        time_label.config(text=f"{fmt(current)} / {fmt(total)}")

    # --- Nút điều khiển ---
    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=10)

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

    # --- Thoát Unit ---
    def exit_unit():
        stop(True)
        for w in main_frame.winfo_children():
            w.destroy()
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
        from controller.unit_controller import get_all_units
        if callable(show_in_main):
            show_in_main("Listening", get_all_units())
