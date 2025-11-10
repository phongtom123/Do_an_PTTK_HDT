import tkinter as tk
from tkinter import ttk
import random
import time

# ==========================================================
# ===                 NGÂN HÀNG TỪ VỰNG                  ===
# ==========================================================
# (Bạn có thể thêm bao nhiêu từ tùy thích vào đây)
WORD_BANK = {
    "Cat": "Con mèo",
    "Dog": "Con chó",
    "Sun": "Mặt trời",
    "Moon": "Mặt trăng",
    "House": "Ngôi nhà",
    "Tree": "Cái cây",
    "Water": "Nước",
    "Book": "Quyển sách",
    "Teacher": "Giáo viên",
    "Student": "Học sinh",
    "Hello": "Xin chào",
    "Goodbye": "Tạm biệt"
}

# --- Biến toàn cục cho logic game ---
selected_english_button = None
selected_vietnamese_button = None
matches_found = 0
game_running = True # Sẽ chuyển thành False khi hết giờ


def create_game_screen(parent):
    global selected_english_button, selected_vietnamese_button, matches_found, game_running
    
    # --- Reset biến game mỗi khi bắt đầu ---
    selected_english_button = None
    selected_vietnamese_button = None
    matches_found = 0
    game_running = True
    
    # --- 1. DỌN DẸP MÀN HÌNH ---
    for widget in parent.winfo_children():
        widget.destroy()

    parent.config(bg="white")

    # --- 2. TÙY CHỈNH STYLE ---
    style = ttk.Style()
    style.configure("timer.Horizontal.TProgressbar", 
                    thickness=15, 
                    background='#0078d4',
                    troughcolor='#E0E0E0')
    
    # Style cho các nút từ
    style.configure("Word.TButton", font=("Arial", 14), padding=10)
    style.map("Word.TButton",
        background=[('active', '#e0e0e0'), ('disabled', '#f5f5f5')],
        foreground=[('disabled', '#b0b0b0')]
    )
    # Style cho nút đã chọn
    style.configure("Selected.TButton", font=("Arial", 14), padding=10, background="#0078d4")


    # --- 3. VẼ GIAO DIỆN ---
    
    # --- Vòng đếm ngược thời gian (Giữ nguyên) ---
    timer_frame = tk.Frame(parent, bg="white")
    timer_frame.pack(pady=20)
    
    timer_progress = ttk.Progressbar(timer_frame, 
                                     orient="horizontal", 
                                     length=200, 
                                     mode="determinate", 
                                     style="timer.Horizontal.TProgressbar")
    timer_progress.pack(pady=5)

    timer_label = tk.Label(timer_frame, text="01:00",
                           font=("Arial", 36, "bold"), 
                           bg="white", fg="#333333")
    timer_label.pack()

    # --- Khu vực chơi game (Mới) ---
    game_area = tk.Frame(parent, bg="white")
    game_area.pack(fill="x", expand=True, pady=20, padx=50)

    # Chia làm 2 cột
    left_column = tk.Frame(game_area, bg="white")
    left_column.pack(side="left", fill="x", expand=True, padx=(0, 20))
    
    right_column = tk.Frame(game_area, bg="white")
    right_column.pack(side="right", fill="x", expand=True, padx=(20, 0))

    # Tạo 8 nút và lưu vào list
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
        """Reset màu của 2 nút đã chọn (nếu có)"""
        global selected_english_button, selected_vietnamese_button
        if selected_english_button:
            selected_english_button.configure(style="Word.TButton")
        if selected_vietnamese_button:
            selected_vietnamese_button.configure(style="Word.TButton")
        selected_english_button = None
        selected_vietnamese_button = None

    def check_for_match():
        """Kiểm tra xem 2 nút đã chọn có khớp không"""
        global matches_found
        
        # Nếu chưa chọn đủ 2 nút thì không làm gì
        if not selected_english_button or not selected_vietnamese_button:
            return

        eng_word = selected_english_button.cget("text")
        vie_word = selected_vietnamese_button.cget("text")

        # Kiểm tra trong ngân hàng từ
        if WORD_BANK.get(eng_word) == vie_word:
            # === NẾU ĐÚNG ===
            selected_english_button.config(text=f"✓ {eng_word}", state="disabled")
            selected_vietnamese_button.config(text=f"✓ {vie_word}", state="disabled")
            matches_found += 1
        else:
            # === NẾU SAI ===
            # (Bạn có thể thêm hiệu ứng nháy đỏ ở đây nếu muốn)
            pass 
        
        # Dù đúng hay sai, reset lựa chọn để chơi tiếp
        reset_selection()
        
        # Nếu tìm đủ 4 cặp, tải vòng mới
        if matches_found == 4:
            matches_found = 0
            parent.after(500, load_new_round) # Chờ 0.5s rồi tải vòng mới

    def on_english_select(button):
        """Khi bấm vào 1 nút tiếng Anh"""
        global selected_english_button
        if not game_running: return # Ngừng nếu hết giờ

        if selected_english_button: # Bỏ chọn nút cũ
            selected_english_button.configure(style="Word.TButton")
            
        selected_english_button = button # Chọn nút mới
        selected_english_button.configure(style="Selected.TButton")
        check_for_match()

    def on_vietnamese_select(button):
        """Khi bấm vào 1 nút tiếng Việt"""
        global selected_vietnamese_button
        if not game_running: return # Ngừng nếu hết giờ

        if selected_vietnamese_button: # Bỏ chọn nút cũ
            selected_vietnamese_button.configure(style="Word.TButton")
            
        selected_vietnamese_button = button # Chọn nút mới
        selected_vietnamese_button.configure(style="Selected.TButton")
        check_for_match()
        
    def load_new_round():
        """Tải 4 cặp từ mới lên các nút"""
        
        # Lấy 4 từ tiếng Anh ngẫu nhiên
        if len(WORD_BANK) < 4:
            print("Lỗi: Cần ít nhất 4 từ trong WORD_BANK")
            return
            
        sample_keys = random.sample(list(WORD_BANK.keys()), 4)
        
        # Lấy các từ tiếng Việt tương ứng
        vietnamese_words = [WORD_BANK[key] for key in sample_keys]
        
        # Xáo trộn 2 danh sách
        random.shuffle(sample_keys)
        random.shuffle(vietnamese_words)
        
        # Gán từ mới cho 8 nút
        for i in range(4):
            english_buttons[i].config(text=sample_keys[i], state="normal",
                                    command=lambda b=english_buttons[i]: on_english_select(b))
            
            vietnamese_buttons[i].config(text=vietnamese_words[i], state="normal",
                                       command=lambda b=vietnamese_buttons[i]: on_vietnamese_select(b))

    def game_over():
        """Hàm được gọi khi hết giờ"""
        global game_running
        game_running = False
        timer_label.config(text="00:00")
        timer_progress.config(value=0)
        
        # Vô hiệu hóa tất cả các nút
        for i in range(4):
            english_buttons[i].config(state="disabled")
            vietnamese_buttons[i].config(state="disabled")
        
        # (Bạn có thể thêm 1 Label "Hết giờ!" ở đây)


    # ==========================================================
    # ===            LOGIC ĐẾM NGƯỢC (Đã sửa)               ===
    # ==========================================================

    remaining_time = [60] 

    def update_timer():
        if not game_running: # Dừng nếu game đã kết thúc
            return

        try:
            current_time = remaining_time[0]
            if current_time > 0:
                current_time -= 1
                remaining_time[0] = current_time

                mins, secs = divmod(current_time, 60)
                timer_label.config(text=f"{mins:02d}:{secs:02d}")
                
                progress_value = (current_time / 60) * 100
                timer_progress.config(value=progress_value)

                parent.after(1000, update_timer)
            else:
                game_over() # Hết giờ
        
        except tk.TclError:
            pass # Widget đã bị hủy, dừng vòng lặp

    # --- 5. KÍCH HOẠT GAME ---
    load_new_round() # Tải vòng đầu tiên
    parent.after(1000, update_timer) # Bắt đầu đếm ngược