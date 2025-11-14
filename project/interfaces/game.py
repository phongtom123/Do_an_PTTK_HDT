import tkinter as tk
from tkinter import ttk
import random
import time
from db.db import db 

# ==========================================================
# ===            CLASS TRANG CHƠI GAME (GAMEPAGE)        ===
# ==========================================================

class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.selected_english_button = None
        self.selected_vietnamese_button = None
        self.matches_found = 0
        self.game_running = True
        self.total_score = 0
        
        self.english_buttons = []
        self.vietnamese_buttons = []

        self._draw_start_screen()

    def refresh(self):
        """Hàm này được controller gọi khi trang được hiển thị."""
        self._draw_start_screen()

    def _clear_frame(self):
        """Xóa tất cả widget con khỏi frame này."""
        for widget in self.winfo_children():
            widget.destroy()

    # --- HÀM VẼ 1: Màn hình "Bắt đầu" ---
    def _draw_start_screen(self):
        self._clear_frame()
        self.config(bg="white")
        
        start_frame = tk.Frame(self, bg="white")
        start_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(start_frame, text="Trò chơi Nối Từ", 
                 font=("Arial", 28, "bold"), bg="white").pack(pady=20)
        tk.Label(start_frame, text="Nối 4 cặp từ Tiếng Anh - Tiếng Việt chính xác.\nBạn có 60 giây để ghi điểm!", 
                 font=("Arial", 14), bg="white", justify="center").pack(pady=10)
        
        start_button = tk.Button(start_frame, text="🚀 BẮT ĐẦU", 
                                 font=("Arial", 16, "bold"), 
                                 bg="#0078d4", fg="white", 
                                 bd=0, padx=30, pady=10,
                                 activebackground="#005a9e",
                                 activeforeground="white",
                                 command=self._draw_game_screen)
        start_button.pack(pady=30)

    # --- HÀM VẼ 2: Màn hình "Chơi game" ---
    def _draw_game_screen(self):
        self._clear_frame()
        
        self.selected_english_button = None
        self.selected_vietnamese_button = None
        self.matches_found = 0
        self.game_running = True
        self.total_score = 0
        self.english_buttons = []
        self.vietnamese_buttons = []

        style = ttk.Style(self)
        style.configure("Word.TButton", font=("Arial", 14), padding=10)
        style.map("Word.TButton",
            background=[('active', '#e0e0e0'), ('disabled', '#f5f5f5')],
            foreground=[('disabled', '#b0b0b0')]
        )
        style.configure("Selected.TButton", font=("Arial", 14), padding=10, background="#0078d4")

        timer_frame = tk.Frame(self, bg="white")
        timer_frame.pack(pady=20)
        self.timer_canvas = tk.Canvas(timer_frame, width=200, height=200, bg="white", highlightthickness=0)
        self.timer_canvas.grid(row=0, column=0) 
        self.timer_canvas.create_arc(10, 10, 190, 190, start=90, extent=360, 
                                style=tk.ARC, outline="#E0E0E0", width=15)
        self.progress_arc = self.timer_canvas.create_arc(10, 10, 190, 190, start=90, extent=360, 
                                               style=tk.ARC, outline="#0078d4", width=15)
        self.timer_label = tk.Label(timer_frame, text="01:00",
                               font=("Arial", 36, "bold"), 
                               bg="white", fg="#333333")
        self.timer_label.grid(row=0, column=0) 

        self.score_label = tk.Label(self, text=f"Điểm: {self.total_score}", 
                               font=("Arial", 20, "bold"), 
                               bg="white", fg="#0078d4")
        self.score_label.pack(pady=(0, 10)) 

        game_area = tk.Frame(self, bg="white")
        game_area.pack(fill="x", expand=True, pady=0, padx=50) 
        left_column = tk.Frame(game_area, bg="white")
        left_column.pack(side="left", fill="x", expand=True, padx=(0, 20))
        right_column = tk.Frame(game_area, bg="white")
        right_column.pack(side="right", fill="x", expand=True, padx=(20, 0))
        
        for _ in range(4):
            btn = ttk.Button(left_column, text="...", style="Word.TButton")
            btn.pack(fill="x", pady=10)
            self.english_buttons.append(btn)
            
        for _ in range(4):
            btn = ttk.Button(right_column, text="...", style="Word.TButton")
            btn.pack(fill="x", pady=10)
            self.vietnamese_buttons.append(btn)
        
        self.remaining_time = [60]
        
        self._load_new_round()
        self._update_timer()

    # --- HÀM VẼ 3: Màn hình "Kết quả" ---
    def _draw_results_screen(self, final_score):
        self._clear_frame()
        
        results_frame = tk.Frame(self, bg="white")
        results_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(results_frame, text="Hết giờ!", 
                 font=("Arial", 28, "bold"), bg="white", fg="#e74c3c").pack(pady=10)
        tk.Label(results_frame, text="Tổng điểm của bạn:", 
                 font=("Arial", 16), bg="white").pack()
        tk.Label(results_frame, text=f"{final_score}", 
                 font=("Arial", 40, "bold"), bg="white", fg="#0078d4").pack(pady=20)
        
        play_again_button = tk.Button(results_frame, text="🎮 CHƠI LẠI", 
                                     font=("Arial", 14, "bold"), 
                                     bg="#0078d4", fg="white", 
                                     bd=0, padx=20, pady=10,
                                     activebackground="#005a9e",
                                     activeforeground="white",
                                     command=self._draw_start_screen)
        play_again_button.pack(pady=(10, 20))

    # --- CÁC HÀM LOGIC (giờ là phương thức của Class) ---

    def _reset_selection(self):
        if self.selected_english_button:
            self.selected_english_button.configure(style="Word.TButton")
        if self.selected_vietnamese_button:
            self.selected_vietnamese_button.configure(style="Word.TButton")
        self.selected_english_button = None
        self.selected_vietnamese_button = None

    def _check_for_match(self):
        if not self.selected_english_button or not self.selected_vietnamese_button:
            return

        eng_word = self.selected_english_button.cget("text")
        vie_word = self.selected_vietnamese_button.cget("text")

        db_conn = self.controller.db_class()
        query = "SELECT COUNT(1) FROM Words WHERE word = %s AND word_meaning = %s"
        params = (eng_word, vie_word)
        df = db_conn.query(query, params)
        db_conn.close()
        is_match = df.iloc[0, 0] > 0
        
        if is_match:
            self.selected_english_button.config(text=f"✓ {eng_word}", state="disabled")
            self.selected_vietnamese_button.config(text=f"✓ {vie_word}", state="disabled")
            self.matches_found += 1
            self.total_score += 1
            self.score_label.config(text=f"Điểm: {self.total_score}")
        
        self._reset_selection()
        
        if self.matches_found == 4:
            self.matches_found = 0
            self.after(500, self._load_new_round) # Dùng self.after

    def _on_english_select(self, button):
        if not self.game_running: return 
        if self.selected_english_button: 
            self.selected_english_button.configure(style="Word.TButton")
        self.selected_english_button = button 
        self.selected_english_button.configure(style="Selected.TButton")
        self._check_for_match()

    def _on_vietnamese_select(self, button):
        if not self.game_running: return 
        if self.selected_vietnamese_button: 
            self.selected_vietnamese_button.configure(style="Word.TButton")
        self.selected_vietnamese_button = button 
        self.selected_vietnamese_button.configure(style="Selected.TButton")
        self._check_for_match()
        
    def _load_new_round(self):
        db_conn = self.controller.db_class()
        query = "SELECT word, word_meaning FROM Words ORDER BY RAND() LIMIT 4"
        df = db_conn.query(query)
        db_conn.close()
        
        if df.empty or len(df) < 4:
            english_words = ['Error', 'Test', 'Fail', 'Backup']
            vietnamese_words = ['Lỗi', 'Kiểm tra', 'Thất bại', 'Dự phòng']
        else:
            english_words = df['word'].tolist()
            vietnamese_words = df['word_meaning'].tolist()
        
        random.shuffle(english_words)
        random.shuffle(vietnamese_words)
        
        for i in range(4):
            self.english_buttons[i].config(text=english_words[i], state="normal",
                                    command=lambda b=self.english_buttons[i]: self._on_english_select(b))
            self.vietnamese_buttons[i].config(text=vietnamese_words[i], state="normal",
                                       command=lambda b=self.vietnamese_buttons[i]: self._on_vietnamese_select(b))

    def _game_over(self):
        self.game_running = False
        
        for i in range(4):
            try:
                self.english_buttons[i].config(state="disabled")
                self.vietnamese_buttons[i].config(state="disabled")
            except tk.TclError:
                pass 
        
        print(f"Lưu điểm: {self.total_score} cho user {self.controller.current_user_id}")
        
        db_conn = self.controller.db_class()
        user_id = self.controller.current_user_id
        
        # Lệnh 1: INSERT vào games
        query_insert = "INSERT INTO games (game_user_id, score) VALUES (%s, %s)"
        params_insert = (user_id, self.total_score)
        db_conn.dml_ddl_operator(query_insert, params_insert)
        
        # Lệnh 2: UPDATE Users
        query_update = "UPDATE Users SET user_rank = IFNULL(user_rank, 0) + %s WHERE user_id = %s"
        params_update = (self.total_score, user_id)
        db_conn.dml_ddl_operator(query_update, params_update)
        db_conn.close()
        
        self.after(1000, lambda: self._draw_results_screen(self.total_score))

    def _update_timer(self):
        if not self.game_running: 
            return
        try:
            current_time = self.remaining_time[0]
            if current_time > 0:
                current_time -= 1
                self.remaining_time[0] = current_time
                mins, secs = divmod(current_time, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                angle = current_time * 6 
                self.timer_canvas.itemconfig(self.progress_arc, extent=angle)
                self.after(1000, self._update_timer) # Dùng self.after
            else:
                self.timer_label.config(text="00:00")
                self.timer_canvas.itemconfig(self.progress_arc, extent=0)
                self._game_over() 
        except tk.TclError:
            pass