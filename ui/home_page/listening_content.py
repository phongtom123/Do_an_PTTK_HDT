import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
import threading, time
from ui.home_page.sidebar_learning import SidebarLearning


class ListeningPracticeFrame(tk.Frame):
    """Khung luyện nghe (Listening Practice) — hiển thị âm thanh, transcript và giữ sidebar thật."""

    def __init__(self, root, main_frame, sidebar_right_ref,
                 recreate_sidebar_right, show_in_main, in_learning_mode,
                 listenings=None):
        super().__init__(main_frame, bg="white")

        self.root = root
        self.main_frame = main_frame
        self.sidebar_right_ref = sidebar_right_ref
        self.recreate_sidebar_right = recreate_sidebar_right
        self.show_in_main = show_in_main
        self.in_learning_mode = in_learning_mode
        self.in_learning_mode[0] = True

        # ---------------- DỮ LIỆU NGHE ----------------
        self.listenings = listenings or [{
            "title": "Listening Sample 1",
            "audio_path": "./audio/sample.mp3",
            "transcript": "This is a static listening passage for testing."
        }]

        self.audio_path = self.listenings[0].get("audio_path", "")
        self.transcript = self.listenings[0].get("transcript", "")
        self.is_playing = False
        self.start_time = 0

        try:
            mixer.init()
        except Exception:
            pass

        # ---------------- GIAO DIỆN ----------------
        self._setup_sidebar()
        self._create_widgets()

    # ============================================================
    def _setup_sidebar(self):
        """
        Giữ nguyên SidebarLearning được truyền từ main_content nếu có câu hỏi thật.
        Nếu không có hoặc đã bị destroy, tạo mới SidebarLearning mặc định.
        """
        if self.sidebar_right_ref and isinstance(self.sidebar_right_ref, (list, tuple)) and len(self.sidebar_right_ref) > 0:
            sidebar = self.sidebar_right_ref[0]

            # ✅ Nếu sidebar tồn tại và còn hoạt động → dùng lại
            if sidebar is not None:
                try:
                    if hasattr(sidebar, "winfo_exists") and sidebar.winfo_exists():
                        try:
                            sidebar.pack(side="right", fill="y", padx=(10, 20), pady=10)
                        except Exception:
                            pass
                        return  # Không tạo mới
                except Exception:
                    pass

        # ❌ Nếu không tồn tại sidebar hợp lệ → tạo mới (fallback)
        try:
            self.sidebar_right_ref[0] = SidebarLearning(self.root, mode="Listening")
        except Exception:
            self.sidebar_right_ref[0] = None

    # ============================================================
    def _create_widgets(self):
        """Tạo bố cục giao diện chính"""
        # Tiêu đề
        tk.Label(self, text="🎧 Listening Practice",
                 font=("Arial", 16, "bold"), bg="white", fg="#1da9fe").pack(pady=10)

        # Hình minh họa
        try:
            img = Image.open("./photos/Tiger.png").resize((400, 300), Image.LANCZOS)
        except Exception:
            img = Image.new("RGB", (400, 300), "#cce5ff")
        self.photo = ImageTk.PhotoImage(img)
        tk.Label(self, image=self.photo, bg="white").pack(pady=(5, 15))

        # Thanh tiến trình + thời gian
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=100, pady=(10, 0))
        self.time_label = tk.Label(self, text="00:00 / 00:00", bg="white", font=("Arial", 12))
        self.time_label.pack(pady=5)

        # Nút điều khiển âm thanh
        controls = tk.Frame(self, bg="white")
        controls.pack(pady=10)

        self.play_btn = tk.Button(controls, text="▶ Play", bg="#2ecc71", fg="white",
                                  font=("Arial", 12, "bold"), width=10,
                                  command=self._toggle_play)
        self.play_btn.pack(side="left", padx=10)

        tk.Button(controls, text="■ Stop", bg="#e74c3c", fg="white",
                  font=("Arial", 12, "bold"), width=10,
                  command=self._stop_audio).pack(side="left", padx=10)

        # Transcript
        tk.Label(self, text="📜 Transcript", font=("Arial", 13, "bold"),
                 bg="white", fg="#333").pack(pady=(10, 0))

        text_box = tk.Text(self, wrap="word", font=("Arial", 12),
                           bg="#F8F9FA", height=8, padx=15, pady=10)
        text_box.insert("1.0", self.transcript)
        text_box.configure(state="disabled")
        text_box.pack(fill="x", padx=50, pady=(0, 20))

    # ============================================================
    def _toggle_play(self):
        """Chạy hoặc tạm dừng audio"""
        if not self.is_playing:
            try:
                mixer.music.load(self.audio_path)
                mixer.music.play()
                self.start_time = time.time()
                self.is_playing = True
                self.play_btn.config(text="⏸ Pause", bg="#e67e22")
                threading.Thread(target=self._update_progress, daemon=True).start()
            except Exception as e:
                self.time_label.config(text=f"Lỗi: {e}")
        else:
            mixer.music.pause()
            self.is_playing = False
            self.play_btn.config(text="▶ Play", bg="#2ecc71")

    def _stop_audio(self):
        """Dừng audio và reset thanh tiến trình"""
        try:
            mixer.music.stop()
        except Exception:
            pass
        self.is_playing = False
        self.progress["value"] = 0
        self.time_label.config(text="00:00 / 00:00")
        self.play_btn.config(text="▶ Play", bg="#2ecc71")

    def _update_progress(self):
        """Cập nhật thanh tiến trình (giả lập 50 giây nghe)"""
        total_time = 50
        while self.is_playing:
            elapsed = time.time() - self.start_time
            percent = min(elapsed / total_time * 100, 100)
            self.progress["value"] = percent
            self.time_label.config(text=f"{int(elapsed):02d}s / {total_time}s")

            if percent >= 100:
                self._stop_audio()
                break
            time.sleep(0.25)
