import tkinter as tk
from tkinter import ttk
import random
import time
# --- IMPORT DB ---
from db.db import db 

# --- (Các biến toàn cục giữ nguyên) ---
selected_english_button = None
selected_vietnamese_button = None
matches_found = 0
game_running = True
total_score = 0

# ==========================================================
# ===       HÀM 0: MÀN HÌNH KẾT QUẢ (Game Over)          ===
# ==========================================================
# (Hàm này không thay đổi)
def show_results_screen(parent, final_score):
    for widget in parent.winfo_children():
        widget.destroy()
    parent.config(bg="white")
    results_frame = tk.Frame(parent, bg="white")
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
                                 command=lambda: create_game_screen(parent))
    play_again_button.pack(pady=(10, 20)) 


# ==========================================================
# ===        HÀM 1: TRANG BẮT ĐẦU (Start Page)           ===
# ==========================================================
# (Hàm này không thay đổi, 4 cặp từ là đúng với DB mới)
def create_game_screen(parent):
    for widget in parent.winfo_children():
        widget.destroy()
    parent.config(bg="white")
    start_frame = tk.Frame(parent, bg="white")
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
                             command=lambda: start_actual_game(parent))
    start_button.pack(pady=30)

# ==========================================================
# ===          HÀM 2: LOGIC CHƠI GAME THỰC SỰ            ===
# ==========================================================
def start_actual_game(parent):
    global selected_english_button, selected_vietnamese_button, matches_found, game_running, total_score
    
    selected_english_button = None
    selected_vietnamese_button = None
    matches_found = 0
    game_running = True
    total_score = 0
    
    # (Phần code UI/Style/Vẽ đồng hồ/Vẽ 8 nút giữ nguyên)
    # (Vì bảng 'words' mới của bạn hỗ trợ 4 cặp từ)
    for widget in parent.winfo_children():
        widget.destroy()
    parent.config(bg="white")
    style = ttk.Style()
    style.configure("Word.TButton", font=("Arial", 14), padding=10)
    style.map("Word.TButton",
        background=[('active', '#e0e0e0'), ('disabled', '#f5f5f5')],
        foreground=[('disabled', '#b0b0b0')]
    )
    style.configure("Selected.TButton", font=("Arial", 14), padding=10, background="#0078d4")
    timer_frame = tk.Frame(parent, bg="white")
    timer_frame.pack(pady=20)
    timer_canvas = tk.Canvas(timer_frame, width=200, height=200, bg="white", highlightthickness=0)
    timer_canvas.grid(row=0, column=0) 
    timer_canvas.create_arc(10, 10, 190, 190, start=90, extent=360, 
                            style=tk.ARC, outline="#E0E0E0", width=15)
    progress_arc = timer_canvas.create_arc(10, 10, 190, 190, start=90, extent=360, 
                                           style=tk.ARC, outline="#0078d4", width=15)
    timer_label = tk.Label(timer_frame, text="01:00",
                           font=("Arial", 36, "bold"), 
                           bg="white", fg="#333333")
    timer_label.grid(row=0, column=0) 
    score_label = tk.Label(parent, text=f"Điểm: {total_score}", 
                           font=("Arial", 20, "bold"), 
                           bg="white", fg="#0078d4")
    score_label.pack(pady=(0, 10)) 
    game_area = tk.Frame(parent, bg="white")
    game_area.pack(fill="x", expand=True, pady=0, padx=50) 
    left_column = tk.Frame(game_area, bg="white")
    left_column.pack(side="left", fill="x", expand=True, padx=(0, 20))
    right_column = tk.Frame(game_area, bg="white")
    right_column.pack(side="right", fill="x", expand=True, padx=(20, 0))
    
    english_buttons = []
    for _ in range(4):
        btn = ttk.Button(left_column, text="...", style="Word.TButton")
        btn.pack(fill="x", pady=10)
        english_buttons.append(btn)
        
    vietnamese_buttons = []
    for _ in range(4):
        btn = ttk.Button(right_column, text="...", style="Word.TButton")
        btn.pack(fill="x", pady=10)
        vietnamese_buttons.append(btn)

    # --- 4. LOGIC GAME (Kết nối Database) ---

    def reset_selection():
        # (Giữ nguyên)
        global selected_english_button, selected_vietnamese_button
        if selected_english_button:
            selected_english_button.configure(style="Word.TButton")
        if selected_vietnamese_button:
            selected_vietnamese_button.configure(style="Word.TButton")
        selected_english_button = None
        selected_vietnamese_button = None

    def check_for_match():
        # (Giữ nguyên - Bảng 'words' mới vẫn hỗ trợ)
        global matches_found, total_score
        if not selected_english_button or not selected_vietnamese_button:
            return
        eng_word = selected_english_button.cget("text")
        vie_word = selected_vietnamese_button.cget("text")
        db_conn = db()
        query = "SELECT COUNT(1) FROM Words WHERE word = %s AND word_meaning = %s"
        params = (eng_word, vie_word)
        df = db_conn.query(query, params)
        db_conn.close()
        is_match = df.iloc[0, 0] > 0
        if is_match:
            selected_english_button.config(text=f"✓ {eng_word}", state="disabled")
            selected_vietnamese_button.config(text=f"✓ {vie_word}", state="disabled")
            matches_found += 1
            total_score += 1
            score_label.config(text=f"Điểm: {total_score}")
        else:
            pass 
        reset_selection()
        
        if matches_found == 4:
            matches_found = 0
            parent.after(500, load_new_round) 

    def on_english_select(button):
        # (Giữ nguyên)
        global selected_english_button
        if not game_running: return 
        if selected_english_button: 
            selected_english_button.configure(style="Word.TButton")
        selected_english_button = button 
        selected_english_button.configure(style="Selected.TButton")
        check_for_match()

    def on_vietnamese_select(button):
        # (Giữ nguyên)
        global selected_vietnamese_button
        if not game_running: return 
        if selected_vietnamese_button: 
            selected_vietnamese_button.configure(style="Word.TButton")
        selected_vietnamese_button = button 
        selected_vietnamese_button.configure(style="Selected.TButton")
        check_for_match()
        
    def load_new_round():
        # (Giữ nguyên - Bảng 'words' mới có 25 từ)
        db_conn = db()
        query = "SELECT word, word_meaning FROM Words ORDER BY RAND() LIMIT 4"
        df = db_conn.query(query)
        db_conn.close()
        
        if df.empty or len(df) < 4:
            print("Lỗi: Không lấy đủ 4 từ từ database, dùng từ dự phòng")
            english_words = ['Error', 'Test', 'Fail', 'Backup']
            vietnamese_words = ['Lỗi', 'Kiểm tra', 'Thất bại', 'Dự phòng']
        else:
            english_words = df['word'].tolist()
            vietnamese_words = df['word_meaning'].tolist()
        
        random.shuffle(english_words)
        random.shuffle(vietnamese_words)
        
        for i in range(4):
            english_buttons[i].config(text=english_words[i], state="normal",
                                    command=lambda b=english_buttons[i]: on_english_select(b))
            
            vietnamese_buttons[i].config(text=vietnamese_words[i], state="normal",
                                       command=lambda b=vietnamese_buttons[i]: on_vietnamese_select(b))

    def game_over():
        global game_running
        game_running = False
        
        for i in range(4):
            try:
                english_buttons[i].config(state="disabled")
                vietnamese_buttons[i].config(state="disabled")
            except tk.TclError:
                pass 
        
        print(f"Lưu điểm: {total_score} cho user 1 (Lựa chọn 2)")
        
        db_conn = db()
        
        # --- THAY ĐỔI 1: SỬA LỆNH INSERT ---
        # Sửa tên bảng: GameHistory -> games
        # Sửa tên cột: user_id -> game_user_id
        query_insert = "INSERT INTO games (game_user_id, score) VALUES (%s, %s)"
        params_insert = (1, total_score) # Tạm dùng user_id = 1 ('admin')
        db_conn.dml_ddl_operator(query_insert, params_insert)
        
        # --- (Lệnh UPDATE Users giữ nguyên) ---
        # (Vì bảng 'users' mới vẫn có 'user_rank')
        query_update = "UPDATE Users SET user_rank = IFNULL(user_rank, 0) + %s WHERE user_id = %s"
        params_update = (total_score, 1) # Tạm dùng user_id = 1
        db_conn.dml_ddl_operator(query_update, params_update)
        
        db_conn.close()
        
        parent.after(1000, lambda: show_results_screen(parent, total_score))

            
    # --- LOGIC ĐẾM NGƯỢC (Giữ nguyên) ---
    remaining_time = [60] 

    def update_timer():
        if not game_running: 
            return
        try:
            current_time = remaining_time[0]
            if current_time > 0:
                current_time -= 1
                remaining_time[0] = current_time
                mins, secs = divmod(current_time, 60)
                timer_label.config(text=f"{mins:02d}:{secs:02d}")
                angle = current_time * 6 
                timer_canvas.itemconfig(progress_arc, extent=angle)
                parent.after(1000, update_timer)
            else:
                timer_label.config(text="00:00")
                timer_canvas.itemconfig(progress_arc, extent=0)
                game_over() 
        except tk.TclError:
            pass 

    # --- 5. KÍCH HOẠT GAME ---
    load_new_round()
    parent.after(1000, update_timer)