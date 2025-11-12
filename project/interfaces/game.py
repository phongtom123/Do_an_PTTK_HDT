import tkinter as tk
from tkinter import ttk
import random
import time

# ==========================================================
# ===                 NGÂN HÀNG TỪ VỰNG                  ===
# ==========================================================
WORD_BANK = {
    "Cat": "Con mèo", "Dog": "Con chó", "Sun": "Mặt trời", "Moon": "Mặt trăng",
    "House": "Ngôi nhà", "Tree": "Cái cây", "Water": "Nước", "Book": "Quyển sách",
    "Teacher": "Giáo viên", "Student": "Học sinh", "Hello": "Xin chào", "Goodbye": "Tạm biệt"
}

# --- Biến toàn cục cho logic game ---
selected_english_button = None
selected_vietnamese_button = None
matches_found = 0
game_running = True
total_score = 0  # <-- THÊM MỚI: Biến lưu tổng điểm

# ==========================================================
# ===       HÀM 0: MÀN HÌNH KẾT QUẢ (MỚI)                ===
# ==========================================================
def show_results_screen(parent, final_score):
    """
    Vẽ màn hình kết quả (Game Over) khi hết giờ.
    Hiển thị điểm cuối cùng và các nút điều hướng.
    """
    
    # 1. Dọn dẹp màn hình chơi game
    for widget in parent.winfo_children():
        widget.destroy()
    parent.config(bg="white")

    # 2. Khung chứa ở giữa
    results_frame = tk.Frame(parent, bg="white")
    results_frame.place(relx=0.5, rely=0.5, anchor="center")

    # 3. Hiển thị thông báo "Hết giờ!"
    tk.Label(results_frame, text="Hết giờ!", 
             font=("Arial", 28, "bold"), bg="white", fg="#e74c3c").pack(pady=10)
    
    # 4. Hiển thị "Tổng điểm của bạn:"
    tk.Label(results_frame, text="Tổng điểm của bạn:", 
             font=("Arial", 16), bg="white").pack()
             
    # 5. Hiển thị điểm số cuối cùng
    tk.Label(results_frame, text=f"{final_score}", 
             font=("Arial", 40, "bold"), bg="white", fg="#0078d4").pack(pady=20)

    # 6. Nút "Chơi lại"
    play_again_button = tk.Button(results_frame, text="🎮 CHƠI LẠI", 
                                 font=("Arial", 14, "bold"), 
                                 bg="#0078d4", fg="white", 
                                 bd=0, padx=20, pady=10,
                                 activebackground="#005a9e",
                                 activeforeground="white",
                                 # Khi bấm, quay lại trang Bắt đầu
                                 command=lambda: create_game_screen(parent))
    play_again_button.pack(pady=10)
    
    # 7. Nút "Xem Lịch sử" (Tạm thời vô hiệu hóa)
    # (Để kích hoạt nút này, chúng ta sẽ cần sửa file main.py ở bước sau)
    history_button = tk.Button(results_frame, text="📜 Xem Lịch sử", 
                               font=("Arial", 14), 
                               fg="#999", bg="white", bd=0,
                               state="disabled") # Bị mờ đi
    history_button.pack(pady=5)


# ==========================================================
# ===        HÀM 1: TRANG BẮT ĐẦU (MÀN HÌNH MỚI)         ===
# ==========================================================
def create_game_screen(parent):
    """
    Hàm này vẽ MÀN HÌNH CHỜ (Start Page).
    (Giữ nguyên, không thay đổi)
    """
    
    # 1. Dọn dẹp màn hình
    for widget in parent.winfo_children():
        widget.destroy()
    parent.config(bg="white")

    # 2. Tạo một khung chứa ở giữa
    start_frame = tk.Frame(parent, bg="white")
    start_frame.place(relx=0.5, rely=0.5, anchor="center")

    # 3. Tiêu đề game
    tk.Label(start_frame, text="Trò chơi Nối Từ", 
             font=("Arial", 28, "bold"), bg="white").pack(pady=20)

    # 4. Hướng dẫn
    tk.Label(start_frame, text="Nối 4 cặp từ Tiếng Anh - Tiếng Việt chính xác.\nBạn có 60 giây để ghi điểm!", 
             font=("Arial", 14), bg="white", justify="center").pack(pady=10)

    # 5. Nút Bắt Đầu
    start_button = tk.Button(start_frame, text="🚀 BẮT ĐẦU", 
                             font=("Arial", 16, "bold"), 
                             bg="#0078d4", fg="white", 
                             bd=0, padx=30, pady=10,
                             activebackground="#005a9e",
                             activeforeground="white",
                             # Khi bấm, gọi hàm logic game
                             command=lambda: start_actual_game(parent))
    start_button.pack(pady=30)

# ==========================================================
# ===          HÀM 2: LOGIC CHƠI GAME THỰC SỰ            ===
# ==========================================================
def start_actual_game(parent):
    """
    Hàm này chứa toàn bộ logic game (đếm ngược, 8 ô, v.v.)
    """
    # SỬA: Thêm 'total_score' vào danh sách global
    global selected_english_button, selected_vietnamese_button, matches_found, game_running, total_score
    
    # --- Reset biến game mỗi khi bắt đầu ---
    selected_english_button = None
    selected_vietnamese_button = None
    matches_found = 0
    game_running = True
    total_score = 0  # <-- SỬA: Reset điểm về 0 khi bắt đầu game mới
    
    # --- 1. DỌN DẸP MÀN HÌNH (Xóa trang "Bắt đầu") ---
    for widget in parent.winfo_children():
        widget.destroy()

    parent.config(bg="white")

    # --- 2. TÙY CHỈNH STYLE (Giữ nguyên) ---
    style = ttk.Style()
    # ... (toàn bộ code style giữ nguyên) ...
    style.configure("Word.TButton", font=("Arial", 14), padding=10)
    style.map("Word.TButton",
        background=[('active', '#e0e0e0'), ('disabled', '#f5f5f5')],
        foreground=[('disabled', '#b0b0b0')]
    )
    style.configure("Selected.TButton", font=("Arial", 14), padding=10, background="#0078d4")

    # --- 3. VẼ GIAO DIỆN ---
    
    # --- Vòng đếm ngược (Giữ nguyên) ---
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

    # --- THÊM MỚI: LABEL HIỂN THỊ ĐIỂM ---
    score_label = tk.Label(parent, text=f"Điểm: {total_score}", 
                           font=("Arial", 20, "bold"), 
                           bg="white", fg="#0078d4")
    # Đặt label điểm ngay dưới vòng tròn
    score_label.pack(pady=(0, 10)) 

    # --- Khu vực chơi game (Giữ nguyên) ---
    game_area = tk.Frame(parent, bg="white")
    # Bỏ bớt lề trên để gần label điểm hơn
    game_area.pack(fill="x", expand=True, pady=0, padx=50) 

    left_column = tk.Frame(game_area, bg="white")
    left_column.pack(side="left", fill="x", expand=True, padx=(0, 20))
    
    right_column = tk.Frame(game_area, bg="white")
    right_column.pack(side="right", fill="x", expand=True, padx=(20, 0))

    # ... (code tạo 8 nút giữ nguyên) ...
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

    # --- 4. LOGIC GAME ---

    def reset_selection():
        # ... (code giữ nguyên) ...
        global selected_english_button, selected_vietnamese_button
        if selected_english_button:
            selected_english_button.configure(style="Word.TButton")
        if selected_vietnamese_button:
            selected_vietnamese_button.configure(style="Word.TButton")
        selected_english_button = None
        selected_vietnamese_button = None

    def check_for_match():
        # SỬA: Thêm 'total_score' vào global
        global matches_found, total_score
        
        if not selected_english_button or not selected_vietnamese_button:
            return

        eng_word = selected_english_button.cget("text")
        vie_word = selected_vietnamese_button.cget("text")

        if WORD_BANK.get(eng_word) == vie_word:
            # --- NỐI ĐÚNG ---
            selected_english_button.config(text=f"✓ {eng_word}", state="disabled")
            selected_vietnamese_button.config(text=f"✓ {vie_word}", state="disabled")
            matches_found += 1
            
            # --- SỬA: CỘNG ĐIỂM VÀ CẬP NHẬT LABEL ---
            total_score += 1
            score_label.config(text=f"Điểm: {total_score}")
            # --- HẾT SỬA ---
            
        else:
            # --- NỐI SAI (Không làm gì, chỉ reset) ---
            pass 
        
        reset_selection()
        
        if matches_found == 4:
            matches_found = 0
            # Tải vòng mới sau 0.5s
            parent.after(500, load_new_round) 

    # ... (code on_english_select, on_vietnamese_select, load_new_round giữ nguyên) ...
    def on_english_select(button):
        global selected_english_button
        if not game_running: return 
        if selected_english_button: 
            selected_english_button.configure(style="Word.TButton")
        selected_english_button = button 
        selected_english_button.configure(style="Selected.TButton")
        check_for_match()

    def on_vietnamese_select(button):
        global selected_vietnamese_button
        if not game_running: return 
        if selected_vietnamese_button: 
            selected_vietnamese_button.configure(style="Word.TButton")
        selected_vietnamese_button = button 
        selected_vietnamese_button.configure(style="Selected.TButton")
        check_for_match()
        
    def load_new_round():
        if len(WORD_BANK) < 4:
            print("Lỗi: Cần ít nhất 4 từ trong WORD_BANK")
            return
        sample_keys = random.sample(list(WORD_BANK.keys()), 4)
        vietnamese_words = [WORD_BANK[key] for key in sample_keys]
        random.shuffle(sample_keys)
        random.shuffle(vietnamese_words)
        for i in range(4):
            english_buttons[i].config(text=sample_keys[i], state="normal",
                                    command=lambda b=english_buttons[i]: on_english_select(b))
            vietnamese_buttons[i].config(text=vietnamese_words[i], state="normal",
                                       command=lambda b=vietnamese_buttons[i]: on_vietnamese_select(b))


    def game_over():
        global game_running
        game_running = False
        
        # Vô hiệu hóa các nút game
        for i in range(4):
            english_buttons[i].config(state="disabled")
            vietnamese_buttons[i].config(state="disabled")
        
        # --- SỬA: GỌI MÀN HÌNH KẾT QUẢ ---
        # Chờ 1 giây (1000ms) rồi mới chuyển màn hình
        # để người chơi kịp thấy 00:00 và điểm số cuối cùng
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
                # Sửa: Chỉ cập nhật UI, hàm game_over sẽ xử lý logic
                timer_label.config(text="00:00")
                timer_canvas.itemconfig(progress_arc, extent=0)
                game_over() 
        
        except tk.TclError:
            pass 

    # --- 5. KÍCH HOẠT GAME ---
    load_new_round() # Tải vòng đầu tiên
    parent.after(1000, update_timer) # Bắt đầu đếm ngược