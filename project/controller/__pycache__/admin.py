import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
# 🎨 GIAO DIỆN ADMIN CHÍNH
# ===============================
class BLEUAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("👑 BLEU Admin – Language Learning Platform")
        self.root.geometry("1400x800")
        self.root.configure(bg="#F8FAFC")

        # --------- SIDEBAR ---------
        self.sidebar = tk.Frame(root, bg="#0F172A", width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo & Brand
        logo_frame = tk.Frame(self.sidebar, bg="#0F172A")
        logo_frame.pack(pady=50)
        
        tk.Label(logo_frame, text="👑", bg="#0F172A", font=("Segoe UI", 48)).pack()
        tk.Label(logo_frame, text="ADMIN", fg="#F59E0B", bg="#0F172A",
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(logo_frame, text="Control Panel", fg="#94A3B8", bg="#0F172A",
                 font=("Segoe UI", 10)).pack(pady=(5, 0))

        # Separator line
        tk.Frame(self.sidebar, bg="#1E293B", height=1).pack(fill="x", padx=20, pady=30)

        # Menu Buttons
        self.current_btn = None
        self.btn_dashboard = self.make_sidebar_button("📊  Dashboard", self.show_dashboard)
        self.btn_vocab = self.make_sidebar_button("📚  Quản lý từ vựng", self.show_vocab)
        self.btn_users = self.make_sidebar_button("👥  Quản lý người dùng", lambda: None)
        self.btn_lessons = self.make_sidebar_button("📖  Quản lý bài học", lambda: None)
        
        self.btn_dashboard.pack(fill="x", padx=20, pady=6)
        self.btn_vocab.pack(fill="x", padx=20, pady=6)
        self.btn_users.pack(fill="x", padx=20, pady=6)
        self.btn_lessons.pack(fill="x", padx=20, pady=6)
        
        # Spacer
        tk.Frame(self.sidebar, bg="#0F172A").pack(fill="both", expand=True)
        
        self.btn_exit = self.make_sidebar_button("🚪  Thoát", self.exit_app, is_exit=True)
        self.btn_exit.pack(side="bottom", fill="x", padx=20, pady=30)

        # Main Frame
        self.main_frame = tk.Frame(root, bg="#F8FAFC")
        self.main_frame.pack(fill="both", expand=True)

        # Set default active button
        self.show_dashboard()

    def make_sidebar_button(self, text, command, is_exit=False):
        bg_color = "#DC2626" if is_exit else "#0F172A"
        hover_color = "#EF4444" if is_exit else "#1E293B"
        
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
    # 📊 TRANG DASHBOARD ADMIN
    # ===========================
    def show_dashboard(self):
        self.clear_main()
        
        # Load system stats
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM USER")
                total_users = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM Vocab")
                total_vocab = cursor.fetchone()[0]
                
                cursor.execute("SELECT name, email FROM USER WHERE user_ID=1")
                admin_data = cursor.fetchone()
                conn.close()
            else:
                total_users, total_vocab = 0, 0
                admin_data = ("Admin", "admin@bleu.com")
        except:
            total_users, total_vocab = 0, 0
            admin_data = ("Admin", "admin@bleu.com")

        admin_name, admin_email = admin_data if admin_data else ("Admin", "admin@bleu.com")

        # Scrollable container
        canvas = tk.Canvas(self.main_frame, bg="#F8FAFC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8FAFC")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Main container
        container = tk.Frame(scrollable_frame, bg="#F8FAFC")
        container.pack(fill="both", expand=True, padx=45, pady=35)

        # ============ HERO SECTION ============
        hero = tk.Frame(container, bg="#F8FAFC")
        hero.pack(fill="x", pady=(0, 30))

        greeting_frame = tk.Frame(hero, bg="#F8FAFC")
        greeting_frame.pack(anchor="w", pady=(0, 28))
        
        tk.Label(greeting_frame, text="Xin chào Admin! 👋", font=("Segoe UI", 20),
                 fg="#64748B", bg="#F8FAFC").pack(anchor="w")
        tk.Label(greeting_frame, text=admin_name, font=("Segoe UI", 42, "bold"),
                 fg="#0F172A", bg="#F8FAFC").pack(anchor="w")

        # ============ STATS ROW - 4 ADMIN CARDS ============
        stats_row = tk.Frame(container, bg="#F8FAFC")
        stats_row.pack(fill="x", pady=(0, 28))

        for i in range(4):
            stats_row.columnconfigure(i, weight=1, uniform="stat")

        # Stat 1 - Total Users
        self.create_admin_stat_card(
            stats_row, "👥", str(total_users), "Tổng người dùng",
            "#3B82F6", "#2563EB"
        ).grid(row=0, column=0, padx=(0, 12), sticky="nsew")

        # Stat 2 - Total Vocabulary
        self.create_admin_stat_card(
            stats_row, "📚", str(total_vocab), "Tổng từ vựng",
            "#10B981", "#059669"
        ).grid(row=0, column=1, padx=(6, 12), sticky="nsew")

        # Stat 3 - Lessons
        self.create_admin_stat_card(
            stats_row, "📖", "24", "Bài học",
            "#F59E0B", "#D97706"
        ).grid(row=0, column=2, padx=(6, 12), sticky="nsew")

        # Stat 4 - System Status
        self.create_admin_stat_card(
            stats_row, "✅", "Online", "Trạng thái",
            "#10B981", "#059669"
        ).grid(row=0, column=3, padx=(6, 0), sticky="nsew")

        # ============ TWO COLUMN LAYOUT ============
        content_row = tk.Frame(container, bg="#F8FAFC")
        content_row.pack(fill="both", expand=True)

        # Left Column (60%)
        left_col = tk.Frame(content_row, bg="#F8FAFC")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 18))

        # Admin Info Card
        self.create_admin_info_card(left_col, admin_name, admin_email)

        # System Stats Card
        self.create_system_stats_card(left_col, total_users, total_vocab)

        # Right Column (40%)
        right_col = tk.Frame(content_row, bg="#F8FAFC")
        right_col.pack(side="right", fill="both", expand=True, padx=(18, 0))

        # Quick Actions Card
        self.create_admin_actions_card(right_col)

        # Recent Activity Card
        self.create_recent_activity_card(right_col)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_admin_stat_card(self, parent, icon, value, label, color1, color2):
        """Admin stat card"""
        outer = tk.Frame(parent, bg="#E2E8F0", bd=0)
        
        card = tk.Frame(outer, bg="white", bd=0)
        card.pack(padx=1, pady=1, fill="both", expand=True)
        
        # Gradient header
        header = tk.Frame(card, bg=color1, height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
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

    def create_admin_info_card(self, parent, name, email):
        """Admin info card"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x", pady=(0, 22))
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=36, pady=30)
        
        # Header
        tk.Label(content, text="👤 Thông tin quản trị viên", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Profile row
        profile_row = tk.Frame(content, bg="white")
        profile_row.pack(fill="x", pady=(0, 28))
        
        # Avatar
        avatar_container = tk.Frame(profile_row, bg="white")
        avatar_container.pack(side="left", padx=(0, 30))
        
        avatar_outer = tk.Canvas(avatar_container, width=135, height=135, 
                                bg="white", highlightthickness=0)
        avatar_outer.pack()
        
        avatar_outer.create_oval(6, 6, 129, 129, fill="#F59E0B", outline="#D97706", width=3)
        
        avatar_label = tk.Label(avatar_container, text="👑", 
                               font=("Segoe UI", 58), bg="#F59E0B")
        avatar_label.place(x=67, y=67, anchor="center")
        
        # Info section
        info_section = tk.Frame(profile_row, bg="white")
        info_section.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_section, text=name, font=("Segoe UI", 26, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w")
        tk.Label(info_section, text=email, font=("Segoe UI", 14),
                fg="#64748B", bg="white").pack(anchor="w", pady=(4, 14))
        
        # Admin badge
        status_badge = tk.Frame(info_section, bg="#FEF3C7", bd=0)
        status_badge.pack(anchor="w")
        tk.Label(status_badge, text="⭐ Quản trị viên", font=("Segoe UI", 11, "bold"),
                fg="#D97706", bg="#FEF3C7").pack(padx=14, pady=8)
        
        # Divider
        tk.Frame(content, bg="#E2E8F0", height=1).pack(fill="x", pady=(0, 22))
        
        # Details
        details = tk.Frame(content, bg="white")
        details.pack(fill="x")
        
        self.create_info_row(details, "🔑", "Quyền hạn", "Toàn quyền", 0)
        self.create_info_row(details, "📅", "Ngày tạo", datetime.now().strftime("%Y-%m-%d"), 1)
        self.create_info_row(details, "⚡", "Trạng thái", "Đang hoạt động", 2)

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

    def create_system_stats_card(self, parent, total_users, total_vocab):
        """System statistics card"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x")
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=36, pady=30)
        
        tk.Label(content, text="📊 Thống kê hệ thống", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Stats grid
        stats_data = [
            ("👥", "Người dùng", str(total_users), "#3B82F6"),
            ("📚", "Từ vựng", str(total_vocab), "#10B981"),
            ("📖", "Bài học", "24", "#F59E0B"),
            ("✅", "Hoàn thành", "156", "#8B5CF6")
        ]
        
        for icon, label, value, color in stats_data:
            stat_row = tk.Frame(content, bg="white")
            stat_row.pack(fill="x", pady=8)
            
            icon_frame = tk.Frame(stat_row, bg=color, width=54, height=54)
            icon_frame.pack(side="left", padx=(0, 18))
            icon_frame.pack_propagate(False)
            
            tk.Label(icon_frame, text=icon, font=("Segoe UI", 24),
                    bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")
            
            text_frame = tk.Frame(stat_row, bg="white")
            text_frame.pack(side="left", fill="x", expand=True)
            
            tk.Label(text_frame, text=label, font=("Segoe UI", 12),
                    fg="#94A3B8", bg="white").pack(anchor="w")
            tk.Label(text_frame, text=value, font=("Segoe UI", 18, "bold"),
                    fg="#0F172A", bg="white").pack(anchor="w", pady=(2, 0))

    def create_admin_actions_card(self, parent):
        """Admin quick actions"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="x", pady=(0, 22))
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content, text="⚡ Thao tác nhanh", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        # Action buttons
        self.create_action_btn(content, "📚", "Quản lý từ vựng", "#10B981",
                              self.show_vocab).pack(fill="x", pady=(0, 14))
        self.create_action_btn(content, "👥", "Quản lý người dùng", "#3B82F6",
                              lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")).pack(fill="x", pady=(0, 14))
        self.create_action_btn(content, "⚙️", "Cài đặt hệ thống", "#8B5CF6",
                              lambda: messagebox.showinfo("Thông báo", "Chức năng đang phát triển")).pack(fill="x")

    def create_action_btn(self, parent, icon, text, color, command):
        """Action button"""
        btn_frame = tk.Frame(parent, bg=color, bd=0, cursor="hand2")
        
        content = tk.Frame(btn_frame, bg=color)
        content.pack(fill="both", expand=True, pady=16)
        
        tk.Label(content, text=icon, font=("Segoe UI", 21),
                bg=color, fg="white").pack(side="left", padx=(22, 12))
        tk.Label(content, text=text, font=("Segoe UI", 14, "bold"),
                bg=color, fg="white", anchor="w").pack(side="left", fill="x", expand=True)
        
        def on_enter(e):
            darker = self.darken_color(color)
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

    def darken_color(self, color):
        """Darken hex color"""
        colors = {
            "#3B82F6": "#2563EB",
            "#8B5CF6": "#7C3AED",
            "#10B981": "#059669",
            "#F59E0B": "#D97706"
        }
        return colors.get(color, color)

    def create_recent_activity_card(self, parent):
        """Recent activity card"""
        card = tk.Frame(parent, bg="white", bd=0)
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#E2E8F0", height=2)
        shadow.pack(fill="x", side="bottom")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content, text="📋 Hoạt động gần đây", font=("Segoe UI", 21, "bold"),
                fg="#0F172A", bg="white").pack(anchor="w", pady=(0, 22))
        
        activities = [
            ("✅", "Thêm 5 từ vựng mới", "2 giờ trước", "#10B981"),
            ("✏️", "Cập nhật bài học Unit 3", "5 giờ trước", "#3B82F6"),
            ("👥", "3 người dùng mới đăng ký", "1 ngày trước", "#F59E0B"),
        ]
        
        for icon, text, time, color in activities:
            activity_row = tk.Frame(content, bg="#F8FAFC")
            activity_row.pack(fill="x", pady=8)
            
            icon_frame = tk.Frame(activity_row, bg=color, width=40, height=40)
            icon_frame.pack(side="left", padx=(12, 12), pady=12)
            icon_frame.pack_propagate(False)
            
            tk.Label(icon_frame, text=icon, font=("Segoe UI", 18),
                    bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")
            
            text_frame = tk.Frame(activity_row, bg="#F8FAFC")
            text_frame.pack(side="left", fill="x", expand=True, pady=12)
            
            tk.Label(text_frame, text=text, font=("Segoe UI", 11, "bold"),
                    fg="#0F172A", bg="#F8FAFC").pack(anchor="w")
            tk.Label(text_frame, text=time, font=("Segoe UI", 9),
                    fg="#94A3B8", bg="#F8FAFC").pack(anchor="w")

    # ===========================
    # 📘 TRANG QUẢN LÝ TỪ VỰNG ADMIN
    # ===========================
    def show_vocab(self):
        self.clear_main()
        AdminVocab(self.main_frame)

# ===============================
# 📖 MODULE QUẢN LÝ TỪ VỰNG ADMIN
# ===============================
class AdminVocab:
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

        # Search & Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search type
        type_frame = tk.Frame(action_container, bg="white")
        type_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(type_frame, text="Tìm theo:", bg="white", font=("Segoe UI", 10, "bold"),
                 fg="#1E3A8A").pack(side=tk.LEFT, padx=(0, 10))
        
        type_combo = ttk.Combobox(type_frame, textvariable=self.search_type_var,
                                 state="readonly", width=15, font=("Segoe UI", 10))
        type_combo['values'] = ["Tất cả", "ID", "Từ tiếng Anh", "Nghĩa tiếng Việt"]
        type_combo.set("Tất cả")
        type_combo.pack(side=tk.LEFT, ipady=5)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_word())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_word, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm từ mới", self.add_word, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "English", "Vietnamese", "Difficulty", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("ID", "ID", 70),
            ("English", "Từ tiếng Anh", 250),
            ("Vietnamese", "Nghĩa tiếng Việt", 320),
            ("Difficulty", "Độ khó", 120),
            ("Actions", "Thao tác", 200)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["ID", "Difficulty", "Actions"] else "w")

        # Style for alternating rows
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        # Bind double-click to edit
        self.tree.bind("<Double-Button-1>", self.on_row_click)

        self.load_data()

    def on_row_click(self, event):
        """Handle row click for edit/delete"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#5":  # Actions column
                values = self.tree.item(item)['values']
                word_id = values[0]
                
                # Show action menu
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_word(word_id, values[1], values[2], values[3]))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_word(word_id))
                
                menu.post(event.x_root, event.y_root)

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
            "#10B981": "#059669",
            "#EF4444": "#DC2626"
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
            # Add visual indicators for actions
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], "✏️ Sửa | 🗑️ Xóa"))

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

    def add_word(self):
        """Add new vocabulary"""
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm từ vựng mới")
        win.geometry("600x550")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm từ vựng mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Từ tiếng Anh:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        word_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        word_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nghĩa tiếng Việt:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        meaning_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        meaning_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Độ khó:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        difficulty_combo = ttk.Combobox(form, values=["easy", "medium", "hard"], 
                                       state="readonly", width=47, font=("Segoe UI", 11))
        difficulty_combo.set("medium")
        difficulty_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def save_word():
            word = word_entry.get().strip()
            meaning = meaning_entry.get().strip()
            difficulty = difficulty_combo.get()
            
            if not word or not meaning:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if not messagebox.askyesno("Xác nhận thêm", 
                                      f"Bạn có chắc muốn thêm từ vựng này?\n\n" +
                                      f"Từ: {word}\n" +
                                      f"Nghĩa: {meaning}\n" +
                                      f"Độ khó: {difficulty}"):
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Vocab (word, meaning, difficulty) VALUES (%s, %s, %s)", 
                                 (word, meaning, difficulty))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm từ vựng mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm từ vựng:\n{e}")

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(pady=(10, 0))

        btn = tk.Button(btn_frame, text="💾 Thêm từ vựng", command=save_word,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack()
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_word(self, word_id, current_word, current_meaning, current_difficulty):
        """Edit vocabulary"""
        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa từ vựng")
        win.geometry("600x550")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa từ vựng ID: {word_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Từ tiếng Anh:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        word_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        word_entry.insert(0, current_word)
        word_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nghĩa tiếng Việt:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        meaning_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        meaning_entry.insert(0, current_meaning)
        meaning_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Độ khó:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        difficulty_combo = ttk.Combobox(form, values=["easy", "medium", "hard"], 
                                       state="readonly", width=47, font=("Segoe UI", 11))
        difficulty_combo.set(current_difficulty)
        difficulty_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def update_word():
            word = word_entry.get().strip()
            meaning = meaning_entry.get().strip()
            difficulty = difficulty_combo.get()
            
            if not word or not meaning:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if not messagebox.askyesno("Xác nhận cập nhật", 
                                      f"Bạn có chắc muốn cập nhật từ vựng này?\n\n" +
                                      f"Từ: {word}\n" +
                                      f"Nghĩa: {meaning}\n" +
                                      f"Độ khó: {difficulty}"):
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Vocab SET word=%s, meaning=%s, difficulty=%s WHERE word_ID=%s", 
                                 (word, meaning, difficulty, word_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật từ vựng!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_word,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def delete_word(self, word_id):
        """Delete vocabulary"""
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa từ vựng ID {word_id}?\n\n" +
                                  "Hành động này không thể hoàn tác!"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Vocab WHERE word_ID=%s", (word_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa từ vựng!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")

# ===============================
# 🚀 CHẠY APP
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = BLEUAdminApp(root)
    root.mainloop()