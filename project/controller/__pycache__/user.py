import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ===============================
# ⚙️ KẾT NỐI DATABASE
# ===============================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bleu"
        )
    except Error as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database:\n{e}")
        return None

# ===============================
# 🎨 GIAO DIỆN CHÍNH
# ===============================
class BLEUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 BLEU – Language Learning Platform")
        self.root.geometry("1400x800")
        self.root.configure(bg="#F8FAFC")

        # --------- SIDEBAR ---------
        self.sidebar = tk.Frame(root, bg="#0F172A", width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo & Brand with gradient effect
        logo_frame = tk.Frame(self.sidebar, bg="#0F172A")
        logo_frame.pack(pady=50)
        
        tk.Label(logo_frame, text="🌊", bg="#0F172A", font=("Segoe UI", 48)).pack()
        tk.Label(logo_frame, text="BLEU", fg="#38BDF8", bg="#0F172A",
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(logo_frame, text="Language Platform", fg="#94A3B8", bg="#0F172A",
                 font=("Segoe UI", 10)).pack(pady=(5, 0))

        # Separator line
        tk.Frame(self.sidebar, bg="#1E293B", height=1).pack(fill="x", padx=20, pady=30)

        # Menu Buttons
        self.current_btn = None
        self.btn_profile = self.make_sidebar_button("👤  Hồ sơ", self.show_profile)
        self.btn_vocab = self.make_sidebar_button("📚  Từ vựng", self.show_vocab)
        self.btn_lessons = self.make_sidebar_button("📖  Bài học", lambda: None)
        self.btn_progress = self.make_sidebar_button("📊  Tiến độ", lambda: None)
        
        self.btn_profile.pack(fill="x", padx=20, pady=6)
        self.btn_vocab.pack(fill="x", padx=20, pady=6)
        self.btn_lessons.pack(fill="x", padx=20, pady=6)
        self.btn_progress.pack(fill="x", padx=20, pady=6)
        
        # Spacer
        tk.Frame(self.sidebar, bg="#0F172A").pack(fill="both", expand=True)
        
        self.btn_exit = self.make_sidebar_button("🚪  Thoát", self.exit_app, is_exit=True)
        self.btn_exit.pack(side="bottom", fill="x", padx=20, pady=30)

        # Main Frame
        self.main_frame = tk.Frame(root, bg="#F8FAFC")
        self.main_frame.pack(fill="both", expand=True)

        # Set default active button
        self.show_profile()

    def make_sidebar_button(self, text, command, is_exit=False):
        bg_color = "#DC2626" if is_exit else "#0F172A"
        hover_color = "#EF4444" if is_exit else "#1E293B"
        active_color = "#38BDF8" if not is_exit else "#DC2626"
        
        btn = tk.Button(
            self.sidebar, text=text, font=("Segoe UI", 12),
            bg=bg_color, fg="#CBD5E1", activebackground=hover_color,
            activeforeground="white", relief="flat", bd=0,
            cursor="hand2", height=2, anchor="w", padx=25,
            command=lambda: self.on_menu_click(btn, command, is_exit)
        )
        
        def on_enter(e):
            if btn != self.current_btn or is_exit:
                btn.config(bg=hover_color, fg="white")
        
        def on_leave(e):
            if btn == self.current_btn and not is_exit:
                btn.config(bg="#1E293B", fg="white")
            elif not is_exit:
                btn.config(bg=bg_color, fg="#CBD5E1")
            else:
                btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def on_menu_click(self, btn, command, is_exit):
        if not is_exit:
            if self.current_btn:
                self.current_btn.config(bg="#0F172A", fg="#CBD5E1")
            self.current_btn = btn
            btn.config(bg="#1E293B", fg="white")
        command()

    def exit_app(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.root.quit()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ===========================
    # 👤 TRANG HỒ SƠ NGƯỜI DÙNG - REDESIGNED
    # ===========================
    def show_profile(self):
        self.clear_main()
        
        # Load data
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, email, level, progress, createDate, account FROM USER LIMIT 1")
                data = cursor.fetchone()
                conn.close()
            else:
                data = None
        except:
            data = None

        if not data:
            data = ("User 1", "user1@gmail.com", 4, "Đang học Unit 8", "2025-10-27", "🧑‍🎓")

        name, email, level, progress, join_date, avatar = data if len(data) == 6 else (*data, "🧑‍🎓")
        self.current_avatar = avatar if avatar else "🧑‍🎓"

        # Scrollable container
        canvas = tk.Canvas(self.main_frame, bg="#F8FAFC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8FAFC")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Main container - Full width
        container = tk.Frame(scrollable_frame, bg="#F8FAFC")
        container.pack(fill="both", expand=True, padx=45, pady=35)

        # ============ HERO SECTION ============
        hero = tk.Frame(container, bg="#F8FAFC")
        hero.pack(fill="x", pady=(0, 30))

        # Greeting
        greeting_frame = tk.Frame(hero, bg="#F8FAFC")
        greeting_frame.pack(anchor="w", pady=(0, 28))
        
        tk.Label(greeting_frame, text="Xin chào! 👋", font=("Segoe UI", 20),
                 fg="#64748B", bg="#F8FAFC").pack(anchor="w")
        tk.Label(greeting_frame, text=name, font=("Segoe UI", 42, "bold"),
                 fg="#0F172A", bg="#F8FAFC").pack(anchor="w")

        # ============ STATS ROW - 4 MODERN CARDS ============
        stats_row = tk.Frame(container, bg="#F8FAFC")
        stats_row.pack(fill="x", pady=(0, 28))

        # Configure grid
        for i in range(4):
            stats_row.columnconfigure(i, weight=1, uniform="stat")

        # Stat 1 - Streak
        self.create_gradient_stat_card(
            stats_row, "🔥", "7", "Ngày liên tiếp",
            "#FF6B6B", "#EE5A6F", 0
        ).grid(row=0, column=0, padx=(0, 12), sticky="nsew")

        # Stat 2 - XP
        self.create_gradient_stat_card(
            stats_row, "⭐", "2,450", "Tổng điểm XP",
            "#FFA94D", "#FFD43B", 1
        ).grid(row=0, column=1, padx=(6, 12), sticky="nsew")

        # Stat 3 - Vocabulary
        self.create_gradient_stat_card(
            stats_row, "📚", "156", "Từ đã học",
            "#4ECDC4", "#44BCBB", 2
        ).grid(row=0, column=2, padx=(6, 12), sticky="nsew")

        # Stat 4 - Level
        self.create_gradient_stat_card(
            stats_row, "🎯", f"Level {level}", "Cấp độ hiện tại",
            "#A78BFA", "#8B5CF6", 3
        ).grid(row=0, column=3, padx=(6, 0), sticky="nsew")

        # ============ TWO COLUMN LAYOUT ============
        content_row = tk.Frame(container, bg="#F8FAFC")
        content_row.pack(fill="both", expand=True)

        # Left Column (60%)
        left_col = tk.Frame(content_row, bg="#F8FAFC")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 18))

        # Profile Info Card
        self.create_modern_profile_card(left_col, name, email, join_date, level, progress)

        # Learning Progress Card
        self.create_progress_card(left_col)

        # Right Column (40%)
        right_col = tk.Frame(content_row, bg="#F8FAFC")
        right_col.pack(side="right", fill="both", expand=True, padx=(18, 0))

        # Achievements Card
        self.create_modern_achievements_card(right_col)

        # Quick Actions Card
        self.create_quick_actions_card(right_col, name, email)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_gradient_stat_card(self, parent, icon, value, label, color1, color2, index):
        """Modern gradient stat card with animation feel"""
        # Outer frame for shadow effect
        outer = tk.Frame(parent, bg="#E2E8F0", bd=0)
        
        card = tk.Frame(outer, bg="white", bd=0)
        card.pack(padx=1, pady=1, fill="both", expand=True)
        
        # Gradient header
        header = tk.Frame(card, bg=color1, height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Icon
        icon_label = tk.Label(header, text=icon, font=("Segoe UI", 48),
                             bg=color1, fg="white")
        icon_label.pack(pady=(18, 6))
        
        # Content
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, pady=18)
        
        tk.Label(content, text=value, font=("Segoe UI", 33, "bold"),
                fg="#0F172A", bg="white").pack()
        tk.Label(content, text=label, font=("Segoe UI", 13),
                fg="#64748B", bg="white").pack(pady=(2, 0))
        
        # Hover effect
        def on_enter(e):
            card.config(bg=color2)
            header.config(bg=color2)
            icon_label.config(bg=color2)
        
        def on_leave(e):
            card.config(bg="white")
            header.config(bg=color1)
            icon_label.config(bg=color1)
        
        outer.bind("<Enter>", on_enter)
        outer.bind("<Leave>", on_leave)
        
        return outer

    def create_modern_profile_card(self, parent, name, email, join_date, level, progress):
        """Modern profile info card"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x", pady=(0, 22))
        
        # Card shadow
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=36, pady=30)
        
        # Header
        tk.Label(content, text="📋 Thông tin cá nhân", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Avatar & Basic Info
        profile_row = tk.Frame(content, bg="white")
        profile_row.pack(fill="x", pady=(0, 28))
        
        # Large circular avatar
        avatar_container = tk.Frame(profile_row, bg="white")
        avatar_container.pack(side="left", padx=(0, 30))
        
        avatar_outer = tk.Canvas(avatar_container, width=135, height=135, 
                                bg="white", highlightthickness=0)
        avatar_outer.pack()
        
        # Draw circular gradient background
        avatar_outer.create_oval(6, 6, 129, 129, fill="#38BDF8", outline="#0EA5E9", width=3)
        
        self.avatar_label = tk.Label(avatar_container, text=self.current_avatar, 
                                    font=("Segoe UI", 58), bg="#38BDF8")
        self.avatar_label.place(x=67, y=67, anchor="center")
        
        # Info section
        info_section = tk.Frame(profile_row, bg="white")
        info_section.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_section, text=name, font=("Segoe UI", 26, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w")
        tk.Label(info_section, text=email, font=("Segoe UI", 14),
                fg="#64748B", bg="white").pack(anchor="w", pady=(4, 14))
        
        # Status badge
        status_badge = tk.Frame(info_section, bg="#DBEAFE", bd=0)
        status_badge.pack(anchor="w")
        tk.Label(status_badge, text="✓ Tài khoản đã xác thực", font=("Segoe UI", 11, "bold"),
                fg="#0284C7", bg="#DBEAFE").pack(padx=14, pady=8)
        
        # Divider
        tk.Frame(content, bg="#E2E8F0", height=1).pack(fill="x", pady=(0, 22))
        
        # Details grid
        details = tk.Frame(content, bg="white")
        details.pack(fill="x")
        
        self.create_info_row(details, "📅", "Ngày tham gia", str(join_date), 0)
        self.create_info_row(details, "📊", "Cấp độ", f"Level {level}", 1)
        self.create_info_row(details, "📖", "Tiến độ", progress, 2)

    def create_info_row(self, parent, icon, label, value, row):
        """Info row with icon"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=9)
        
        icon_frame = tk.Frame(frame, bg="#F1F5F9", width=54, height=54)
        icon_frame.pack(side="left", padx=(0, 18))
        icon_frame.pack_propagate(False)
        
        tk.Label(icon_frame, text=icon, font=("Segoe UI", 24),
                bg="#F1F5F9").place(relx=0.5, rely=0.5, anchor="center")
        
        text_frame = tk.Frame(frame, bg="white")
        text_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(text_frame, text=label, font=("Segoe UI", 12),
                fg="#94A3B8", bg="white").pack(anchor="w")
        tk.Label(text_frame, text=value, font=("Segoe UI", 15, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(2, 0))

    def create_progress_card(self, parent):
        """Learning progress visualization"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x")
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=36, pady=30)
        
        tk.Label(content, text="📈 Tiến độ học tập", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Weekly progress bars
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        values = [85, 60, 90, 45, 100, 70, 55]
        
        progress_grid = tk.Frame(content, bg="white")
        progress_grid.pack(fill="x")
        
        for i, (day, val) in enumerate(zip(days, values)):
            col = tk.Frame(progress_grid, bg="white")
            col.pack(side="left", fill="both", expand=True, padx=6)
            
            # Progress bar
            bar_container = tk.Frame(col, bg="#F1F5F9", height=145, width=48)
            bar_container.pack()
            bar_container.pack_propagate(False)
            
            bar_height = int(125 * val / 100)
            bar_color = "#10B981" if val > 70 else "#F59E0B" if val > 40 else "#94A3B8"
            
            bar = tk.Frame(bar_container, bg=bar_color, width=44)
            bar.place(x=2, y=125-bar_height+2, height=bar_height-4)
            
            # Day label
            tk.Label(col, text=day, font=("Segoe UI", 11, "bold"),
                    fg="#64748B", bg="white").pack(pady=(9, 0))

    def create_modern_achievements_card(self, parent):
        """Modern achievements display"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x", pady=(0, 22))
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content, text="🏆 Thành tích", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Achievement badges in 2x2 grid
        badges = [
            ("🥇", "Siêu sao", "#FFD700", "#FFF8DC"),
            ("🔥", "Đam mê", "#FF6B6B", "#FFE5E5"),
            ("⚡", "Tốc độ", "#FFA94D", "#FFE8CC"),
            ("🎯", "Chính xác", "#4ECDC4", "#E0F7F6")
        ]
        
        for i in range(0, 4, 2):
            row = tk.Frame(content, bg="white")
            row.pack(fill="x", pady=6)
            
            for j in range(2):
                if i + j < len(badges):
                    icon, label, color, bg = badges[i + j]
                    self.create_achievement_badge_modern(row, icon, label, color, bg).pack(
                        side="left", fill="both", expand=True, padx=6)

    def create_achievement_badge_modern(self, parent, icon, label, color, bg_color):
        """Modern achievement badge"""
        badge = tk.Frame(parent, bg=bg_color, bd=0, height=95)
        badge.pack_propagate(False)
        
        content = tk.Frame(badge, bg=bg_color)
        content.pack(expand=True)
        
        tk.Label(content, text=icon, font=("Segoe UI", 38),
                bg=bg_color).pack(pady=(14, 6))
        tk.Label(content, text=label, font=("Segoe UI", 12, "bold"),
                fg=color, bg=bg_color).pack(pady=(0, 14))
        
        return badge

    def create_quick_actions_card(self, parent, name, email):
        """Quick actions panel"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content, text="⚡ Thao tác nhanh", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Action buttons
        self.create_modern_action_btn(content, "✏️", "Chỉnh sửa hồ sơ", "#3B82F6",
                                     lambda: self.edit_profile(name, email)).pack(fill="x", pady=(0, 14))
        self.create_modern_action_btn(content, "🔒", "Đổi mật khẩu", "#8B5CF6",
                                     self.change_password).pack(fill="x", pady=(0, 14))
        self.create_modern_action_btn(content, "⚙️", "Cài đặt", "#64748B",
                                     self.open_settings).pack(fill="x")

    def create_modern_action_btn(self, parent, icon, text, color, command):
        """Modern action button with icon"""
        btn_frame = tk.Frame(parent, bg=color, bd=0, cursor="hand2")
        
        content = tk.Frame(btn_frame, bg=color)
        content.pack(fill="both", expand=True, pady=16)
        
        tk.Label(content, text=icon, font=("Segoe UI", 21),
                bg=color, fg="white").pack(side="left", padx=(22, 12))
        tk.Label(content, text=text, font=("Segoe UI", 14, "bold"),
                bg=color, fg="white", anchor="w").pack(side="left", fill="x", expand=True)
        
        def on_enter(e):
            darker = self.darken_hex_color(color)
            btn_frame.config(bg=darker)
            content.config(bg=darker)
            for child in content.winfo_children():
                child.config(bg=darker)
        
        def on_leave(e):
            btn_frame.config(bg=color)
            content.config(bg=color)
            for child in content.winfo_children():
                child.config(bg=color)
        
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        btn_frame.bind("<Button-1>", lambda e: command())
        content.bind("<Button-1>", lambda e: command())
        for child in content.winfo_children():
            child.bind("<Button-1>", lambda e: command())
        
        return btn_frame

    def darken_hex_color(self, hex_color):
        """Darken a hex color"""
        colors = {
            "#3B82F6": "#2563EB",
            "#8B5CF6": "#7C3AED",
            "#64748B": "#475569",
            "#10B981": "#059669"
        }
        return colors.get(hex_color, hex_color)

    # ===========================
    # CHỨC NĂNG EDIT PROFILE (ĐẦY ĐỦ TỪ CODE GỐC)
    # ===========================
    def edit_profile(self, current_name, current_email):
        win = tk.Toplevel(self.root)
        win.title("✏️ Chỉnh sửa hồ sơ")
        win.geometry("550x700")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="✏️ Chỉnh sửa thông tin cá nhân",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        # Canvas với scrollbar
        canvas = tk.Canvas(win, bg="#E8F4F8", highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        form = tk.Frame(canvas, bg="white")

        form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form, anchor="nw", width=490)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=30, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)

        # Avatar selection
        tk.Label(form, text="Chọn Avatar:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 10))
        
        selected_avatar = tk.StringVar(value=self.current_avatar)
        
        preview_frame = tk.Frame(form, bg="#F1F5F9", relief="flat", bd=1)
        preview_frame.pack(fill="x", pady=(0, 15), ipady=10)
        
        preview_label = tk.Label(preview_frame, textvariable=selected_avatar, 
                                font=("Segoe UI", 50), bg="#F1F5F9")
        preview_label.pack()

        avatars = [
            "👨", "👩", "🧑", "😊", "😎", "🤓", "🧑‍🎓", "👨‍💻",
            "👩‍💻", "🧑‍🏫", "🧙‍♂️", "🧙‍♀️", "🦸‍♂️", "🦸‍♀️", "🧑‍🚀", "🧑‍🎨"
        ]

        avatar_grid = tk.Frame(form, bg="white")
        avatar_grid.pack(pady=(0, 15))

        row_idx = 0
        col_idx = 0
        for avatar in avatars:
            btn = tk.Button(avatar_grid, text=avatar, font=("Segoe UI", 28),
                           bg="#F1F5F9", fg="black", cursor="hand2",
                           relief="flat", bd=0, width=2, height=1)
            btn.grid(row=row_idx, column=col_idx, padx=3, pady=3)
            
            if avatar == self.current_avatar:
                btn.config(bg="#DBEAFE", relief="solid", bd=2)
            
            def on_click(av=avatar, b=btn):
                for widget in avatar_grid.winfo_children():
                    widget.config(bg="#F1F5F9", relief="flat", bd=0)
                b.config(bg="#DBEAFE", relief="solid", bd=2)
                selected_avatar.set(av)
            
            btn.config(command=on_click)
            
            col_idx += 1
            if col_idx >= 8:
                col_idx = 0
                row_idx += 1

        separator = tk.Frame(form, bg="#E2E8F0", height=1)
        separator.pack(fill="x", pady=15)

        tk.Label(form, text="Họ và tên:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        name_e = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        name_e.insert(0, current_name)
        name_e.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Email:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        email_e = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        email_e.insert(0, current_email)
        email_e.pack(pady=(0, 20), ipady=8, fill="x")

        def save_profile():
            new_name = name_e.get().strip()
            new_email = email_e.get().strip()
            new_avatar = selected_avatar.get()
            
            if not new_name or not new_email:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if not messagebox.askyesno("Xác nhận lưu", 
                                      f"Bạn có chắc muốn cập nhật thông tin?\n\n" +
                                      f"Tên: {new_name}\n" +
                                      f"Email: {new_email}\n" +
                                      f"Avatar: {new_avatar}"):
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE USER SET name=%s, email=%s, account=%s WHERE user_ID=1", 
                                 (new_name, new_email, new_avatar))
                    conn.commit()
                    conn.close()
                    self.current_avatar = new_avatar
                    messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
                    win.destroy()
                    self.show_profile()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Lưu thay đổi", command=save_profile,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def change_password(self):
        win = tk.Toplevel(self.root)
        win.title("🔒 Đổi mật khẩu")
        win.geometry("500x450")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#6366F1", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔒 Đổi mật khẩu",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#6366F1").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Mật khẩu hiện tại:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        old_pass = ttk.Entry(form, width=50, font=("Segoe UI", 11), show="●")
        old_pass.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Mật khẩu mới:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        new_pass = ttk.Entry(form, width=50, font=("Segoe UI", 11), show="●")
        new_pass.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Xác nhận mật khẩu mới:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        confirm_pass = ttk.Entry(form, width=50, font=("Segoe UI", 11), show="●")
        confirm_pass.pack(pady=(0, 20), ipady=8, fill="x")

        def save_password():
            old_p = old_pass.get().strip()
            new_p = new_pass.get().strip()
            conf_p = confirm_pass.get().strip()
            
            if not old_p or not new_p or not conf_p:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if new_p != conf_p:
                messagebox.showerror("Lỗi", "Mật khẩu mới không khớp!")
                return
            
            if len(new_p) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự!")
                return
            
            if not messagebox.askyesno("Xác nhận đổi mật khẩu", 
                                      "Bạn có chắc muốn đổi mật khẩu?\n\n" +
                                      "Bạn sẽ cần sử dụng mật khẩu mới để đăng nhập lần sau."):
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT password FROM USER WHERE user_ID=1")
                    result = cursor.fetchone()
                    
                    if result and result[0] == old_p:
                        cursor.execute("UPDATE USER SET password=%s WHERE user_ID=1", (new_p,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Thành công", "Đã đổi mật khẩu thành công!")
                        win.destroy()
                    else:
                        conn.close()
                        messagebox.showerror("Lỗi", "Mật khẩu hiện tại không đúng!")
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="🔒 Đổi mật khẩu", command=save_password,
                       font=("Segoe UI", 12, "bold"), bg="#6366F1", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#4F46E5"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#6366F1"))

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("⚙️ Cài đặt")
        win.geometry("600x500")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#8B5CF6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="⚙️ Cài đặt ứng dụng",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#8B5CF6").pack(pady=25)

        content = tk.Frame(win, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        notif_frame = tk.LabelFrame(content, text="🔔 Thông báo", bg="white", fg="#1E3A8A",
                                    font=("Segoe UI", 12, "bold"), padx=20, pady=15)
        notif_frame.pack(fill="x", pady=(10, 15))

        self.notif_var = tk.BooleanVar(value=True)
        tk.Checkbutton(notif_frame, text="Nhận thông báo học tập hàng ngày", 
                      variable=self.notif_var, bg="white", font=("Segoe UI", 10),
                      activebackground="white").pack(anchor="w", pady=5)
        
        self.reminder_var = tk.BooleanVar(value=True)
        tk.Checkbutton(notif_frame, text="Nhắc nhở khi chưa học trong ngày", 
                      variable=self.reminder_var, bg="white", font=("Segoe UI", 10),
                      activebackground="white").pack(anchor="w", pady=5)

        lang_frame = tk.LabelFrame(content, text="🌐 Ngôn ngữ", bg="white", fg="#1E3A8A",
                                   font=("Segoe UI", 12, "bold"), padx=20, pady=15)
        lang_frame.pack(fill="x", pady=(0, 15))

        tk.Label(lang_frame, text="Ngôn ngữ giao diện:", bg="white", 
                font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 5))
        
        lang_combo = ttk.Combobox(lang_frame, values=["Tiếng Việt", "English", "日本語", "中文"],
                                 state="readonly", width=30, font=("Segoe UI", 10))
        lang_combo.set("Tiếng Việt")
        lang_combo.pack(anchor="w", pady=(0, 10), ipady=5)

        data_frame = tk.LabelFrame(content, text="💾 Dữ liệu", bg="white", fg="#1E3A8A",
                                   font=("Segoe UI", 12, "bold"), padx=20, pady=15)
        data_frame.pack(fill="x", pady=(0, 15))

        btn_backup = tk.Button(data_frame, text="📥 Sao lưu dữ liệu",
                              font=("Segoe UI", 10, "bold"), bg="#3B82F6", fg="white",
                              cursor="hand2", bd=0, relief="flat", padx=15, pady=8,
                              command=lambda: messagebox.showinfo("Sao lưu", "Đã sao lưu dữ liệu thành công!"))
        btn_backup.pack(side="left", padx=(0, 10))

        btn_reset = tk.Button(data_frame, text="🔄 Đặt lại tiến độ",
                             font=("Segoe UI", 10, "bold"), bg="#EF4444", fg="white",
                             cursor="hand2", bd=0, relief="flat", padx=15, pady=8,
                             command=lambda: self.reset_progress())
        btn_reset.pack(side="left")

        def save_settings():
            if messagebox.askyesno("Xác nhận lưu", "Bạn có muốn lưu các thay đổi cài đặt?"):
                messagebox.showinfo("Thành công", "Đã lưu cài đặt!")
                win.destroy()

        btn_save = tk.Button(content, text="💾 Lưu cài đặt", command=save_settings,
                            font=("Segoe UI", 12, "bold"), bg="#8B5CF6", fg="white",
                            cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn_save.pack(pady=(20, 0))
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg="#7C3AED"))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg="#8B5CF6"))

    def reset_progress(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đặt lại toàn bộ tiến độ học tập?\nHành động này không thể hoàn tác!"):
            messagebox.showinfo("Thành công", "Đã đặt lại tiến độ học tập!")

    # ===========================
    # 📘 TRANG TỪ VỰNG (GIỮ NGUYÊN TỪ CODE GỐC)
    # ===========================
    def show_vocab(self):
        self.clear_main()
        BLEUVocab(self.main_frame)

# ===============================
# 📖 MODULE QUẢN LÝ TỪ VỰNG
# ===============================
class BLEUVocab:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()
        self.search_type_var = tk.StringVar(value="all")

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="📚 Quản lý từ vựng", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Search Panel
        search_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        search_panel.pack(fill="x", pady=(0, 20))
        search_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        search_container = tk.Frame(search_panel, bg="white")
        search_container.pack(fill="x", padx=20, pady=15)

        type_frame = tk.Frame(search_container, bg="white")
        type_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(type_frame, text="Tìm theo:", bg="white", font=("Segoe UI", 10, "bold"),
                 fg="#1E3A8A").pack(side=tk.LEFT, padx=(0, 10))
        
        type_combo = ttk.Combobox(type_frame, textvariable=self.search_type_var,
                                 state="readonly", width=15, font=("Segoe UI", 10))
        type_combo['values'] = ["Tất cả", "ID", "Từ tiếng Anh", "Nghĩa tiếng Việt"]
        type_combo.set("Tất cả")
        type_combo.pack(side=tk.LEFT, ipady=5)

        search_frame = tk.Frame(search_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=45, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_word())

        button_frame = tk.Frame(search_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_word, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "English", "Vietnamese", "Difficulty")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        for col, text, w in zip(columns,
                                ["ID", "Từ tiếng Anh", "Nghĩa tiếng Việt", "Độ khó"],
                                [80, 300, 400, 150]):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["ID", "Difficulty"] else "w")

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.load_data()

    def make_button(self, parent, text, command, color):
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 10, "bold"),
            bg=color, fg="white", cursor="hand2",
            bd=0, relief="flat", padx=20, pady=10
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.darken_color(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def darken_color(self, color):
        colors = {
            "#3B82F6": "#2563EB",
            "#6366F1": "#4F46E5",
            "#10B981": "#059669"
        }
        return colors.get(color, color)

    def load_data(self):
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("SELECT word_ID, word, meaning, difficulty FROM Vocab ORDER BY word_ID ASC")
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    def search_word(self):
        key = self.search_var.get().strip()
        search_type = self.search_type_var.get()
        
        type_mapping = {
            "Tất cả": "all",
            "ID": "id",
            "Từ tiếng Anh": "word",
            "Nghĩa tiếng Việt": "meaning"
        }
        search_type = type_mapping.get(search_type, "all")
        
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            
            if search_type == "id":
                if not key.isdigit():
                    messagebox.showwarning("Lỗi tìm kiếm", "ID phải là số nguyên!")
                    return
                cursor.execute("SELECT word_ID, word, meaning, difficulty FROM Vocab WHERE word_ID = %s", (int(key),))
            elif search_type == "word":
                cursor.execute("SELECT word_ID, word, meaning, difficulty FROM Vocab WHERE word LIKE %s", (f"%{key}%",))
            elif search_type == "meaning":
                cursor.execute("SELECT word_ID, word, meaning, difficulty FROM Vocab WHERE meaning LIKE %s", (f"%{key}%",))
            else:
                cursor.execute("SELECT word_ID, word, meaning, difficulty FROM Vocab WHERE word_ID LIKE %s OR word LIKE %s OR meaning LIKE %s",
                             (f"%{key}%", f"%{key}%", f"%{key}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy từ vựng nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

# ===============================
# 🚀 CHẠY APP
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = BLEUApp(root)
    root.mainloop()