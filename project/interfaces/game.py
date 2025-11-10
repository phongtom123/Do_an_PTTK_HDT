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
    timer_progress['value'] = 95  # 95% (tương đương 58 giây)

    timer_label = tk.Label(timer_frame, text="00:58", 
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