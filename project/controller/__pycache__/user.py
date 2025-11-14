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
        self.btn_game = self.make_sidebar_button("🎮  Game Matching", self.show_game)
        self.btn_lessons = self.make_sidebar_button("📖  Bài học", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
        self.btn_progress = self.make_sidebar_button("📊  Tiến độ", lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển"))
        
        self.btn_profile.pack(fill="x", padx=20, pady=6)
        self.btn_vocab.pack(fill="x", padx=20, pady=6)
        self.btn_game.pack(fill="x", padx=20, pady=6)
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
    # 👤 TRANG HỒ SƠ NGƯỜI DÙNG
    # ===========================
    def show_profile(self):
        self.clear_main()
        
        # Load data từ bảng Users
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_name, user_level, user_rank, user_status
                    FROM Users 
                    LIMIT 1
                """)
                data = cursor.fetchone()
                conn.close()
            else:
                data = None
        except:
            data = None

        if not data:
            data = ("User 1", 4, 0, 1)

        name = data[0] if data else "User 1"
        level = data[1] if data and len(data) > 1 else 4
        rank = data[2] if data and len(data) > 2 else 0
        email = "user@bleu.com"
        join_date = "2025-01-01"
        progress = f"Level {level}"
        self.current_avatar = "🧑‍🎓"

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
            stats_row, "⭐", str(rank), "Xếp hạng",
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
        self.create_modern_action_btn(content, "🎮", "Chơi game Matching", "#10B981",
                                     self.show_game).pack(fill="x", pady=(0, 14))
        self.create_modern_action_btn(content, "📚", "Xem từ vựng", "#3B82F6",
                                     self.show_vocab).pack(fill="x", pady=(0, 14))
        self.create_modern_action_btn(content, "⚙️", "Cài đặt", "#64748B",
                                     lambda: messagebox.showinfo("Cài đặt", "Chức năng đang phát triển")).pack(fill="x")

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
    # 📘 TRANG TỪ VỰNG
    # ===========================
    def show_vocab(self):
        self.clear_main()
        BLEUVocab(self.main_frame)

    # ===========================
    # 🎮 TRANG GAME MATCHING
    # ===========================
    def show_game(self):
        self.clear_main()
        MatchingGame(self.main_frame)


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
        
        tk.Label(header, text="📚 Từ vựng của tôi", font=("Segoe UI", 28, "bold"),
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
        type_combo['values'] = ["Tất cả", "ID", "Từ tiếng Anh", "Nghĩa tiếng Việt", "Trạng thái", "Độ khó"]
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

        columns = ("ID", "English", "Vietnamese", "Status", "Difficulty")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        for col, text, w in zip(columns,
                                ["ID", "Từ tiếng Anh", "Nghĩa tiếng Việt", "Trạng thái", "Độ khó"],
                                [80, 280, 350, 140, 140]):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["ID", "Status", "Difficulty"] else "w")

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
            cursor.execute("""
                SELECT word_id, word, word_meaning, word_status, word_difficulty 
                FROM Words 
                ORDER BY word_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3] or "N/A", r[4] or "N/A"))

    def search_word(self):
        key = self.search_var.get().strip()
        search_type = self.search_type_var.get()
        
        type_mapping = {
            "Tất cả": "all",
            "ID": "id",
            "Từ tiếng Anh": "word",
            "Nghĩa tiếng Việt": "meaning",
            "Trạng thái": "status",
            "Độ khó": "difficulty"
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
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word_id = %s
                """, (int(key),))
            elif search_type == "word":
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word LIKE %s
                """, (f"%{key}%",))
            elif search_type == "meaning":
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word_meaning LIKE %s
                """, (f"%{key}%",))
            elif search_type == "status":
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word_status LIKE %s
                """, (f"%{key}%",))
            elif search_type == "difficulty":
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word_difficulty LIKE %s
                """, (f"%{key}%",))
            else:
                cursor.execute("""
                    SELECT word_id, word, word_meaning, word_status, word_difficulty 
                    FROM Words 
                    WHERE word_id LIKE %s OR word LIKE %s OR word_meaning LIKE %s 
                       OR word_status LIKE %s OR word_difficulty LIKE %s
                """, (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy từ vựng nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")


# ===============================
# 🎮 MODULE GAME MATCHING
# ===============================
class MatchingGame:
    def __init__(self, parent):
        self.parent = parent
        self.words_data = []
        self.selected_english = None
        self.selected_vietnamese = None
        self.matched_pairs = []
        self.score = 0
        self.total_pairs = 4
        self.english_buttons = []
        self.vietnamese_buttons = []
        
        # Main container
        container = tk.Frame(parent, bg="#F0F4F8")
        container.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(container, bg="#6366F1", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg="#6366F1")
        header_content.pack(expand=True)
        
        tk.Label(header_content, text="🎮 GAME MATCHING", 
                font=("Segoe UI", 32, "bold"), fg="white", bg="#6366F1").pack(pady=(10, 5))
        tk.Label(header_content, text="Ghép từ tiếng Anh với nghĩa tiếng Việt tương ứng", 
                font=("Segoe UI", 13), fg="#E0E7FF", bg="#6366F1").pack()
        
        # Score panel
        score_panel = tk.Frame(container, bg="white", height=80)
        score_panel.pack(fill="x", padx=40, pady=(20, 10))
        score_panel.pack_propagate(False)
        
        score_content = tk.Frame(score_panel, bg="white")
        score_content.pack(expand=True)
        
        self.score_label = tk.Label(score_content, text=f"🏆 Điểm: {self.score}/{self.total_pairs}", 
                                    font=("Segoe UI", 22, "bold"), fg="#6366F1", bg="white")
        self.score_label.pack(side="left", padx=30)
        
        self.status_label = tk.Label(score_content, text="Hãy chọn một từ tiếng Anh và một nghĩa tiếng Việt!", 
                                     font=("Segoe UI", 14), fg="#64748B", bg="white")
        self.status_label.pack(side="left", padx=20)
        
        # Game area
        game_area = tk.Frame(container, bg="#F0F4F8")
        game_area.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Left column - English words
        left_frame = tk.Frame(game_area, bg="#F0F4F8")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        tk.Label(left_frame, text="📘 Từ tiếng Anh", font=("Segoe UI", 18, "bold"),
                fg="#1E3A8A", bg="#F0F4F8").pack(pady=(0, 20))
        
        self.english_frame = tk.Frame(left_frame, bg="#F0F4F8")
        self.english_frame.pack(fill="both", expand=True)
        
        # Right column - Vietnamese meanings
        right_frame = tk.Frame(game_area, bg="#F0F4F8")
        right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        tk.Label(right_frame, text="📗 Nghĩa tiếng Việt", font=("Segoe UI", 18, "bold"),
                fg="#1E3A8A", bg="#F0F4F8").pack(pady=(0, 20))
        
        self.vietnamese_frame = tk.Frame(right_frame, bg="#F0F4F8")
        self.vietnamese_frame.pack(fill="both", expand=True)
        
        # Control buttons
        control_panel = tk.Frame(container, bg="#F0F4F8", height=80)
        control_panel.pack(fill="x", padx=40, pady=(0, 30))
        control_panel.pack_propagate(False)
        
        btn_frame = tk.Frame(control_panel, bg="#F0F4F8")
        btn_frame.pack(expand=True)
        
        self.btn_new_game = tk.Button(btn_frame, text="🔄 Chơi lại", 
                                      font=("Segoe UI", 14, "bold"),
                                      bg="#10B981", fg="white", cursor="hand2",
                                      bd=0, relief="flat", padx=40, pady=15,
                                      command=self.new_game)
        self.btn_new_game.pack(side="left", padx=10)
        
        self.btn_new_game.bind("<Enter>", lambda e: self.btn_new_game.config(bg="#059669"))
        self.btn_new_game.bind("<Leave>", lambda e: self.btn_new_game.config(bg="#10B981"))
        
        # Load game
        self.load_game()
    
    def load_game(self):
        """Load 4 random words from database"""
        try:
            conn = connect_db()
            if not conn:
                messagebox.showerror("Lỗi", "Không thể kết nối database!")
                return
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT word, word_meaning 
                FROM Words 
                WHERE word IS NOT NULL AND word_meaning IS NOT NULL
                ORDER BY RAND() 
                LIMIT 4
            """)
            self.words_data = cursor.fetchall()
            conn.close()
            
            if len(self.words_data) < 4:
                messagebox.showwarning("Cảnh báo", "Cần có ít nhất 4 từ vựng trong database để chơi game!")
                return
            
            self.setup_game()
            
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")
    
    def setup_game(self):
        """Setup game board with words"""
        import random
        
        # Clear previous game
        for widget in self.english_frame.winfo_children():
            widget.destroy()
        for widget in self.vietnamese_frame.winfo_children():
            widget.destroy()
        
        self.english_buttons = []
        self.vietnamese_buttons = []
        self.matched_pairs = []
        self.selected_english = None
        self.selected_vietnamese = None
        self.score = 0
        
        # Extract words and meanings
        english_words = [w[0] for w in self.words_data]
        vietnamese_meanings = [w[1] for w in self.words_data]
        
        # Shuffle Vietnamese meanings
        random.shuffle(vietnamese_meanings)
        
        # Create English buttons
        for i, word in enumerate(english_words):
            btn = tk.Button(
                self.english_frame, text=word,
                font=("Segoe UI", 16, "bold"),
                bg="#3B82F6", fg="white",
                cursor="hand2", relief="flat", bd=0,
                wraplength=300, justify="center",
                padx=20, pady=20
            )
            btn.pack(fill="x", pady=10)
            btn.config(command=lambda b=btn, w=word: self.select_english(b, w))
            self.english_buttons.append((btn, word))
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2563EB") if b.cget("state") != "disabled" else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3B82F6") if b.cget("state") != "disabled" else None)
        
        # Create Vietnamese buttons
        for i, meaning in enumerate(vietnamese_meanings):
            btn = tk.Button(
                self.vietnamese_frame, text=meaning,
                font=("Segoe UI", 16, "bold"),
                bg="#10B981", fg="white",
                cursor="hand2", relief="flat", bd=0,
                wraplength=300, justify="center",
                padx=20, pady=20
            )
            btn.pack(fill="x", pady=10)
            btn.config(command=lambda b=btn, m=meaning: self.select_vietnamese(b, m))
            self.vietnamese_buttons.append((btn, meaning))
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#059669") if b.cget("state") != "disabled" else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#10B981") if b.cget("state") != "disabled" else None)
        
        self.update_status("Hãy chọn một từ tiếng Anh và một nghĩa tiếng Việt!")
        self.update_score()
    
    def select_english(self, button, word):
        """Handle English word selection"""
        # Deselect previous English selection
        if self.selected_english and self.selected_english[0] != button:
            self.selected_english[0].config(bg="#3B82F6", relief="flat")
        
        # Select current button
        self.selected_english = (button, word)
        button.config(bg="#F59E0B", relief="solid")
        
        self.update_status(f"Đã chọn: '{word}' - Hãy chọn nghĩa tiếng Việt!")
        
        # Check if both selected
        if self.selected_vietnamese:
            self.check_match()
    
    def select_vietnamese(self, button, meaning):
        """Handle Vietnamese meaning selection"""
        # Deselect previous Vietnamese selection
        if self.selected_vietnamese and self.selected_vietnamese[0] != button:
            self.selected_vietnamese[0].config(bg="#10B981", relief="flat")
        
        # Select current button
        self.selected_vietnamese = (button, meaning)
        button.config(bg="#F59E0B", relief="solid")
        
        self.update_status(f"Đã chọn nghĩa: '{meaning}' - Hãy chọn từ tiếng Anh!")
        
        # Check if both selected
        if self.selected_english:
            self.check_match()
    
    def check_match(self):
        """Check if selected pair is correct"""
        english_word = self.selected_english[1]
        vietnamese_meaning = self.selected_vietnamese[1]
        
        # Find correct meaning for the English word
        correct_meaning = None
        for word, meaning in self.words_data:
            if word == english_word:
                correct_meaning = meaning
                break
        
        if vietnamese_meaning == correct_meaning:
            # Correct match!
            self.score += 1
            self.matched_pairs.append((english_word, vietnamese_meaning))
            
            # Update buttons to show success
            self.selected_english[0].config(
                bg="#10B981", state="disabled", 
                relief="solid", cursor="arrow"
            )
            self.selected_vietnamese[0].config(
                bg="#10B981", state="disabled",
                relief="solid", cursor="arrow"
            )
            
            self.update_status(f"✅ Chính xác! '{english_word}' = '{vietnamese_meaning}'")
            self.update_score()
            
            # Check if game completed
            if self.score >= self.total_pairs:
                self.parent.after(1000, self.game_completed)
        else:
            # Wrong match
            self.update_status(f"❌ Sai rồi! '{english_word}' ≠ '{vietnamese_meaning}'. Thử lại!")
            
            # Flash red and reset
            self.selected_english[0].config(bg="#EF4444")
            self.selected_vietnamese[0].config(bg="#EF4444")
            
            self.parent.after(800, self.reset_selection)
        
        self.selected_english = None
        self.selected_vietnamese = None
    
    def reset_selection(self):
        """Reset button colors after wrong match"""
        for btn, word in self.english_buttons:
            if btn.cget("state") != "disabled":
                btn.config(bg="#3B82F6", relief="flat")
        
        for btn, meaning in self.vietnamese_buttons:
            if btn.cget("state") != "disabled":
                btn.config(bg="#10B981", relief="flat")
        
        self.update_status("Hãy thử lại! Chọn một từ tiếng Anh và nghĩa tiếng Việt!")
    
    def update_score(self):
        """Update score display"""
        self.score_label.config(text=f"🏆 Điểm: {self.score}/{self.total_pairs}")
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
    
    def game_completed(self):
        """Handle game completion"""
        # Update game result to database
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Games (game_user_id, correct_word_quantity) 
                    VALUES (1, %s)
                """, (self.score,))
                conn.commit()
                conn.close()
        except:
            pass
        
        messagebox.showinfo(
            "🎉 Chúc mừng!", 
            f"Bạn đã hoàn thành game!\n\n" +
            f"Điểm số: {self.score}/{self.total_pairs}\n\n" +
            f"Bạn có muốn chơi lại không?"
        )
        self.new_game()
    
    def new_game(self):
        """Start a new game"""
        self.load_game()


# ===============================
# 🚀 CHẠY APP
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = BLEUApp(root)
    root.mainloop()