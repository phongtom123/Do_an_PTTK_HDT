import tkinter as tk
from tkinter import ttk

def create_game_screen(parent):
    
    # Xóa mọi thứ đang có trên frame 'parent' trước khi vẽ
    for widget in parent.winfo_children():
        widget.destroy()

    # --- Style cho các widget ---
    style = ttk.Style()
    style.configure("timer.Horizontal.TProgressbar", 
                    thickness=15, 
                    background='#0078d4',
                    troughcolor='#E0E0E0')
    
    # --- Đặt màu nền cho frame cha (nếu nó chưa phải màu trắng) ---
    parent.config(bg="white")

    # --- Frame chính cho nội dung game ---
    game_frame = tk.Frame(parent, bg="white", width=600)
    # Dùng .place() để căn giữa hoàn hảo trong frame cha
    game_frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- Vòng đếm ngược thời gian ---
    timer_frame = tk.Frame(game_frame, bg="white")
    timer_frame.pack(pady=30)
    
    timer_progress = ttk.Progressbar(timer_frame, 
                                     orient="horizontal", 
                                     length=200, 
                                     mode="determinate", 
                                     style="timer.Horizontal.TProgressbar")
    timer_progress.grid(row=0, column=0)

    timer_label = tk.Label(timer_frame, text="01:00", # Bắt đầu ở 01:00
                           font=("Arial", 36, "bold"), 
                           bg="white", fg="#333333")
    timer_label.grid(row=0, column=0)

    # --- Từ Tiếng Việt ---
    word_frame = tk.Frame(game_frame, bg="white")
    word_frame.pack(pady=20)
    
    word_label = tk.Label(word_frame, text="Con mèo", 
                          font=("Arial", 44, "bold"), 
                          bg="white")
    word_label.pack(side="left", padx=10)
    
    speaker_label = tk.Label(word_frame, text="🔊", 
                             font=("Arial", 20), 
                             bg="white", fg="#555555")
    speaker_label.pack(side="left")

    # --- Ô nhập liệu ---
    entry_answer = ttk.Entry(game_frame, 
                             font=("Arial", 16), 
                             width=40)
    entry_answer.pack(pady=10, ipady=8)
    entry_answer.insert(0, "Nhập từ tiếng Anh...")

    # --- Các nút bấm ---
    button_frame = tk.Frame(game_frame, bg="white")
    button_frame.pack(pady=20)

    hint_button = tk.Button(button_frame, text="💡 GỢI Ý", 
                             font=("Arial", 12, "bold"), 
                             bg="#0078d4", fg="white", 
                             bd=0, padx=20, pady=10, 
                             activebackground="#005a9e", 
                             activeforeground="white")
    hint_button.pack(side="left", padx=10)

    check_button = tk.Button(button_frame, text="✔ KIỂM TRA", 
                              font=("Arial", 12, "bold"), 
                              bg="#f0f0f0", fg="#a0a0a0", 
                              bd=0, padx=20, pady=10,
                              state="disabled")
    check_button.pack(side="left", padx=10)

    # --- Thông tin Điểm & Chuỗi ---
    info_frame = tk.Frame(game_frame, bg="white")
    info_frame.pack(pady=10)

    score_label = tk.Label(info_frame, text="Điểm: 15", 
                           font=("Arial", 14), bg="white")
    score_label.pack(side="left", padx=20)

    streak_label = tk.Label(info_frame, text="Chuỗi đúng liên tiếp: 3", 
                            font=("Arial", 14), bg="white")
    streak_label.pack(side="left", padx=20)

    # --- Nút Dừng game ---
    stop_button = tk.Button(game_frame, text="⏹ Dừng game", 
                            font=("Arial", 11), 
                            fg="#777777", bg="white", bd=0,
                            activebackground="#f0f0f0")
    stop_button.pack(pady=20)

    # ==========================================================
    # ===            LOGIC ĐẾM NGƯỢC (ĐÃ THÊM)              ===
    # ==========================================================

    # Dùng list để có thể thay đổi giá trị trong hàm con
    remaining_time = [60] 

    def update_timer():
        # Lấy giá trị thời gian còn lại
        
        # === SỬA LỖI: Thêm khối try...except ===
        try:
            current_time = remaining_time[0]

            if current_time > 0:
                # Giảm thời gian đi 1 giây
                current_time -= 1
                remaining_time[0] = current_time

                # Cập nhật Giao diện
                mins, secs = divmod(current_time, 60)
                timer_label.config(text=f"{mins:02d}:{secs:02d}")
                
                # Cập nhật vòng tròn tiến trình
                progress_value = (current_time / 60) * 100
                timer_progress.config(value=progress_value)

                # Lên lịch để hàm này tự gọi lại sau 1000ms (1 giây)
                parent.after(1000, update_timer)
                
            else:
                # HẾT GIỜ
                timer_label.config(text="00:00")
                timer_progress.config(value=0)
                
                # Thông báo hết giờ và vô hiệu hóa các nút
                word_label.config(text="Hết giờ!")
                entry_answer.config(state="disabled")
                check_button.config(state="disabled")
                hint_button.config(state="disabled")
        
        except tk.TclError:
            # Lỗi "invalid command name" (widget đã bị hủy) sẽ được bắt ở đây.
            # Chúng ta không cần làm gì cả (pass), vòng lặp sẽ tự dừng lại.
            pass

    # --- KÍCH HOẠT ĐẾM NGƯỢC ---
    # Cập nhật giao diện lần đầu (để hiển thị 01:00 và vòng tròn đầy)
    timer_label.config(text="01:00")
    timer_progress.config(value=100)
    
    # Bắt đầu vòng lặp đếm ngược sau 1 giây
    parent.after(1000, update_timer)