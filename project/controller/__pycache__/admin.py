import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
        logo_frame.pack(pady=40)
        
        tk.Label(logo_frame, text="👑", bg="#0F172A", font=("Segoe UI", 48)).pack()
        tk.Label(logo_frame, text="ADMIN", fg="#F59E0B", bg="#0F172A",
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(logo_frame, text="Control Panel", fg="#94A3B8", bg="#0F172A",
                 font=("Segoe UI", 10)).pack(pady=(5, 0))

        # Separator line
        tk.Frame(self.sidebar, bg="#1E293B", height=1).pack(fill="x", padx=20, pady=25)

        # Menu Buttons
        self.current_btn = None
        self.btn_dashboard = self.make_sidebar_button("📊  Dashboard", self.show_dashboard)
        self.btn_units = self.make_sidebar_button("📦  Quản lý Units", self.show_units)
        self.btn_lessons = self.make_sidebar_button("📖  Quản lý Lessons", self.show_lessons)
        self.btn_vocab = self.make_sidebar_button("📚  Quản lý từ vựng", self.show_vocab)
        self.btn_questions = self.make_sidebar_button("❓  Quản lý Questions", self.show_questions)
        self.btn_reading = self.make_sidebar_button("📰  Quản lý Reading", self.show_reading)
        self.btn_listening = self.make_sidebar_button("🎧  Quản lý Listening", self.show_listening)
        self.btn_users = self.make_sidebar_button("👥  Quản lý người dùng", self.show_users)
        
        self.btn_dashboard.pack(fill="x", padx=20, pady=4)
        self.btn_units.pack(fill="x", padx=20, pady=4)
        self.btn_lessons.pack(fill="x", padx=20, pady=4)
        self.btn_vocab.pack(fill="x", padx=20, pady=4)
        self.btn_questions.pack(fill="x", padx=20, pady=4)
        self.btn_reading.pack(fill="x", padx=20, pady=4)
        self.btn_listening.pack(fill="x", padx=20, pady=4)
        self.btn_users.pack(fill="x", padx=20, pady=4)
        
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
            self.sidebar, text=text, font=("Segoe UI", 11),
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

    def show_dashboard(self):
        self.clear_main()
        tk.Label(self.main_frame, text="📊 Dashboard", font=("Segoe UI", 32, "bold"),
                 fg="#0F172A", bg="#F8FAFC").pack(pady=50)
        tk.Label(self.main_frame, text="Chào mừng đến với hệ thống quản lý BLEU Admin",
                 font=("Segoe UI", 16), fg="#64748B", bg="#F8FAFC").pack()

    def show_units(self):
        self.clear_main()
        AdminUnits(self.main_frame)

    def show_lessons(self):
        self.clear_main()
        AdminLessons(self.main_frame)

    def show_vocab(self):
        self.clear_main()
        AdminVocab(self.main_frame)

    def show_questions(self):
        self.clear_main()
        AdminQuestions(self.main_frame)

    def show_reading(self):
        self.clear_main()
        AdminReading(self.main_frame)

    def show_listening(self):
        self.clear_main()
        AdminListening(self.main_frame)

    def show_users(self):
        self.clear_main()
        AdminUsers(self.main_frame)


# ===============================
# 📦 MODULE QUẢN LÝ UNITS
# ===============================
class AdminUnits:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="📦 Quản lý Units (Bài học lớn)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_unit())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_unit, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm Unit", self.add_unit, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "Name", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên Unit")
        self.tree.heading("Actions", text="Thao tác")
        
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=600, anchor="w")
        self.tree.column("Actions", width=200, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#3":
                values = self.tree.item(item)['values']
                unit_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_unit(unit_id, values[1]))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_unit(unit_id))
                
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
            cursor.execute("SELECT unit_id, unit_name FROM Units ORDER BY unit_id ASC")
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[1], "✏️ Sửa | 🗑️ Xóa"))

    def search_unit(self):
        key = self.search_var.get().strip()
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("SELECT unit_id, unit_name FROM Units WHERE unit_name LIKE %s OR unit_id LIKE %s",
                         (f"%{key}%", f"%{key}%"))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy unit nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_unit(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm Unit mới")
        win.geometry("600x400")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm Unit mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        name_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        name_entry.pack(pady=(0, 15), ipady=8, fill="x")

        def save_unit():
            name = name_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên Unit!")
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Units (unit_name) VALUES (%s)", (name,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm Unit mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm Unit:\n{e}")

        btn = tk.Button(form, text="💾 Thêm Unit", command=save_unit,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_unit(self, unit_id, current_name):
        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa Unit")
        win.geometry("600x400")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa Unit ID: {unit_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        name_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        name_entry.insert(0, current_name)
        name_entry.pack(pady=(0, 15), ipady=8, fill="x")

        def update_unit():
            name = name_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên Unit!")
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Units SET unit_name=%s WHERE unit_id=%s", (name, unit_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật Unit!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_unit,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def delete_unit(self, unit_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa Unit ID {unit_id}?\n\n" +
                                  "Lưu ý: Tất cả Lessons và dữ liệu liên quan sẽ bị xóa!"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Units WHERE unit_id=%s", (unit_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa Unit!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# 📖 MODULE QUẢN LÝ LESSONS
# ===============================
class AdminLessons:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="📖 Quản lý Lessons (Bài học nhỏ)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_lesson())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_lesson, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm Lesson", self.add_lesson, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "Name", "Unit", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên Lesson")
        self.tree.heading("Unit", text="Thuộc Unit")
        self.tree.heading("Actions", text="Thao tác")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=400, anchor="w")
        self.tree.column("Unit", width=300, anchor="w")
        self.tree.column("Actions", width=200, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#4":
                values = self.tree.item(item)['values']
                lesson_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_lesson(lesson_id, values[1], values[2]))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_lesson(lesson_id))
                
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
            cursor.execute("""
                SELECT l.lesson_id, l.lesson_name, u.unit_name
                FROM Lessons l
                LEFT JOIN Units u ON l.lesson_unit_id = u.unit_id
                ORDER BY l.lesson_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            unit_name = r[2] if r[2] else "Chưa gán"
            self.tree.insert("", "end", values=(r[0], r[1], unit_name, "✏️ Sửa | 🗑️ Xóa"))

    def search_lesson(self):
        key = self.search_var.get().strip()
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.lesson_id, l.lesson_name, u.unit_name
                FROM Lessons l
                LEFT JOIN Units u ON l.lesson_unit_id = u.unit_id
                WHERE l.lesson_name LIKE %s OR l.lesson_id LIKE %s OR u.unit_name LIKE %s
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy lesson nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_lesson(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm Lesson mới")
        win.geometry("600x500")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm Lesson mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên Lesson:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        name_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        name_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load units
        try:
            conn = connect_db()
            units = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT unit_id, unit_name FROM Units")
                units = cursor.fetchall()
                conn.close()
        except:
            units = []
        
        unit_dict = {f"{u[1]} (ID: {u[0]})": u[0] for u in units}
        unit_names = list(unit_dict.keys()) if unit_dict else []
        
        unit_combo = ttk.Combobox(form, values=unit_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        if unit_names:
            unit_combo.set(unit_names[0])
        unit_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def save_lesson():
            name = name_entry.get().strip()
            unit_str = unit_combo.get()
            
            if not name or not unit_str:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            unit_id = unit_dict.get(unit_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Lessons (lesson_name, lesson_unit_id) VALUES (%s, %s)", 
                                 (name, unit_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm Lesson mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm Lesson:\n{e}")

        btn = tk.Button(form, text="💾 Thêm Lesson", command=save_lesson,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_lesson(self, lesson_id, current_name, current_unit):
        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa Lesson")
        win.geometry("600x500")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa Lesson ID: {lesson_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên Lesson:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        name_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        name_entry.insert(0, current_name)
        name_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load units
        try:
            conn = connect_db()
            units = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT unit_id, unit_name FROM Units")
                units = cursor.fetchall()
                conn.close()
        except:
            units = []
        
        unit_dict = {f"{u[1]} (ID: {u[0]})": u[0] for u in units}
        unit_names = list(unit_dict.keys()) if unit_dict else []
        
        unit_combo = ttk.Combobox(form, values=unit_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        # Set current unit
        for key in unit_dict.keys():
            if current_unit in key or key.startswith(current_unit):
                unit_combo.set(key)
                break
        unit_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def update_lesson():
            name = name_entry.get().strip()
            unit_str = unit_combo.get()
            
            if not name or not unit_str:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            unit_id = unit_dict.get(unit_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Lessons SET lesson_name=%s, lesson_unit_id=%s WHERE lesson_id=%s", 
                                 (name, unit_id, lesson_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật Lesson!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_lesson,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def delete_lesson(self, lesson_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa Lesson ID {lesson_id}?\n\n" +
                                  "Lưu ý: Tất cả dữ liệu liên quan sẽ bị xóa!"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Lessons WHERE lesson_id=%s", (lesson_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa Lesson!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# 📚 MODULE QUẢN LÝ TỪ VỰNG (WORDS)
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
        
        tk.Label(header, text="📚 Quản lý từ vựng (Words)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
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
                                 state="readonly", width=12, font=("Segoe UI", 10))
        type_combo['values'] = ["Tất cả", "ID", "Từ", "Nghĩa"]
        type_combo.set("Tất cả")
        type_combo.pack(side=tk.LEFT, ipady=5)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_word())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_word, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm từ", self.add_word, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "Word", "Meaning", "Lesson", "Status", "Difficulty", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("ID", "ID", 60),
            ("Word", "Từ", 150),
            ("Meaning", "Nghĩa", 200),
            ("Lesson", "Lesson", 150),
            ("Status", "Trạng thái", 100),
            ("Difficulty", "Độ khó", 90),
            ("Actions", "Thao tác", 150)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["ID", "Status", "Difficulty", "Actions"] else "w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#7":
                values = self.tree.item(item)['values']
                word_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_word(word_id))
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
            cursor.execute("""
                SELECT w.word_id, w.word, w.word_meaning, l.lesson_name, w.word_status, w.word_difficulty
                FROM Words w
                LEFT JOIN Lessons l ON w.word_lesson_id = l.lesson_id
                ORDER BY w.word_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            lesson_name = r[3] if r[3] else "Chưa gán"
            self.tree.insert("", "end", values=(r[0], r[1], r[2], lesson_name, r[4] or "N/A", r[5] or "medium", "✏️ | 🗑️"))

    def search_word(self):
        key = self.search_var.get().strip()
        search_type = self.search_type_var.get()
        
        type_mapping = {
            "Tất cả": "all",
            "ID": "id",
            "Từ": "word",
            "Nghĩa": "meaning"
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
                    SELECT w.word_id, w.word, w.word_meaning, l.lesson_name, w.word_status, w.word_difficulty
                    FROM Words w
                    LEFT JOIN Lessons l ON w.word_lesson_id = l.lesson_id
                    WHERE w.word_id = %s
                """, (int(key),))
            elif search_type == "word":
                cursor.execute("""
                    SELECT w.word_id, w.word, w.word_meaning, l.lesson_name, w.word_status, w.word_difficulty
                    FROM Words w
                    LEFT JOIN Lessons l ON w.word_lesson_id = l.lesson_id
                    WHERE w.word LIKE %s
                """, (f"%{key}%",))
            elif search_type == "meaning":
                cursor.execute("""
                    SELECT w.word_id, w.word, w.word_meaning, l.lesson_name, w.word_status, w.word_difficulty
                    FROM Words w
                    LEFT JOIN Lessons l ON w.word_lesson_id = l.lesson_id
                    WHERE w.word_meaning LIKE %s
                """, (f"%{key}%",))
            else:
                cursor.execute("""
                    SELECT w.word_id, w.word, w.word_meaning, l.lesson_name, w.word_status, w.word_difficulty
                    FROM Words w
                    LEFT JOIN Lessons l ON w.word_lesson_id = l.lesson_id
                    WHERE w.word LIKE %s OR w.word_meaning LIKE %s
                """, (f"%{key}%", f"%{key}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy từ vựng nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_word(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm từ vựng mới")
        win.geometry("600x700")
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

        tk.Label(form, text="Thuộc Lesson (tùy chọn):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load lessons
        try:
            conn = connect_db()
            lessons = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lesson_id, lesson_name FROM Lessons")
                lessons = cursor.fetchall()
                conn.close()
        except:
            lessons = []
        
        lesson_dict = {f"{l[1]} (ID: {l[0]})": l[0] for l in lessons}
        lesson_dict["Không gán"] = None
        lesson_names = list(lesson_dict.keys())
        
        lesson_combo = ttk.Combobox(form, values=lesson_names, 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        lesson_combo.set("Không gán")
        lesson_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Trạng thái:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        status_combo = ttk.Combobox(form, values=["new", "learning", "mastered"], 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        status_combo.set("new")
        status_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Độ khó:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        difficulty_combo = ttk.Combobox(form, values=["easy", "medium", "hard"], 
                                       state="readonly", width=47, font=("Segoe UI", 11))
        difficulty_combo.set("medium")
        difficulty_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def save_word():
            word = word_entry.get().strip()
            meaning = meaning_entry.get().strip()
            lesson_str = lesson_combo.get()
            status = status_combo.get()
            difficulty = difficulty_combo.get()
            
            if not word or not meaning:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            lesson_id = lesson_dict.get(lesson_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO Words (word, word_meaning, word_lesson_id, word_status, word_difficulty) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (word, meaning, lesson_id, status, difficulty))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm từ vựng mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm từ vựng:\n{e}")

        btn = tk.Button(form, text="💾 Thêm từ vựng", command=save_word,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_word(self, word_id):
        # Get current word data
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT word, word_meaning, word_lesson_id, word_status, word_difficulty
                FROM Words WHERE word_id=%s
            """, (word_id,))
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy từ vựng!")
                return
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            return

        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa từ vựng")
        win.geometry("600x700")
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
        word_entry.insert(0, data[0])
        word_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nghĩa tiếng Việt:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        meaning_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        meaning_entry.insert(0, data[1])
        meaning_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Lesson:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load lessons
        try:
            conn = connect_db()
            lessons = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lesson_id, lesson_name FROM Lessons")
                lessons = cursor.fetchall()
                conn.close()
        except:
            lessons = []
        
        lesson_dict = {f"{l[1]} (ID: {l[0]})": l[0] for l in lessons}
        lesson_dict["Không gán"] = None
        lesson_names = list(lesson_dict.keys())
        
        lesson_combo = ttk.Combobox(form, values=lesson_names, 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        # Set current lesson
        if data[2]:
            for key, val in lesson_dict.items():
                if val == data[2]:
                    lesson_combo.set(key)
                    break
        else:
            lesson_combo.set("Không gán")
        lesson_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Trạng thái:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        status_combo = ttk.Combobox(form, values=["new", "learning", "mastered"], 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        status_combo.set(data[3] if data[3] else "new")
        status_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Độ khó:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        difficulty_combo = ttk.Combobox(form, values=["easy", "medium", "hard"], 
                                       state="readonly", width=47, font=("Segoe UI", 11))
        difficulty_combo.set(data[4] if data[4] else "medium")
        difficulty_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def update_word():
            word = word_entry.get().strip()
            meaning = meaning_entry.get().strip()
            lesson_str = lesson_combo.get()
            status = status_combo.get()
            difficulty = difficulty_combo.get()
            
            if not word or not meaning:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            lesson_id = lesson_dict.get(lesson_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Words 
                        SET word=%s, word_meaning=%s, word_lesson_id=%s, word_status=%s, word_difficulty=%s 
                        WHERE word_id=%s
                    """, (word, meaning, lesson_id, status, difficulty, word_id))
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
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa từ vựng ID {word_id}?"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Words WHERE word_id=%s", (word_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa từ vựng!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# ❓ MODULE QUẢN LÝ QUESTIONS
# ===============================
class AdminQuestions:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="❓ Quản lý Questions (Câu hỏi)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_question())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_question, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm Question", self.add_question, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "Content", "Answer", "Type", "Lesson", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("ID", "ID", 60),
            ("Content", "Nội dung", 300),
            ("Answer", "Đáp án", 150),
            ("Type", "Loại", 100),
            ("Lesson", "Lesson", 150),
            ("Actions", "Thao tác", 150)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["ID", "Type", "Actions"] else "w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#6":
                values = self.tree.item(item)['values']
                question_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_question(question_id))
                menu.add_separator()
                menu.add_command(label="⚙️ Quản lý Options", 
                               command=lambda: self.manage_options(question_id))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_question(question_id))
                
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
            cursor.execute("""
                SELECT q.question_id, q.question_content, q.question_answer, q.question_type, l.lesson_name
                FROM Questions q
                LEFT JOIN Lessons l ON q.question_lesson_id = l.lesson_id
                ORDER BY q.question_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            lesson_name = r[4] if r[4] else "Chưa gán"
            content = r[1][:50] + "..." if r[1] and len(r[1]) > 50 else r[1]
            self.tree.insert("", "end", values=(r[0], content, r[2], r[3], lesson_name, "✏️ | ⚙️ | 🗑️"))

    def search_question(self):
        key = self.search_var.get().strip()
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT q.question_id, q.question_content, q.question_answer, q.question_type, l.lesson_name
                FROM Questions q
                LEFT JOIN Lessons l ON q.question_lesson_id = l.lesson_id
                WHERE q.question_content LIKE %s OR q.question_answer LIKE %s OR q.question_id LIKE %s
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy câu hỏi nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_question(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm Question mới")
        win.geometry("700x750")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm Question mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Nội dung câu hỏi:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=5, font=("Segoe UI", 11))
        content_text.pack(pady=(0, 15), fill="x")

        tk.Label(form, text="Đáp án đúng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        answer_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        answer_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Loại câu hỏi:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        type_combo = ttk.Combobox(form, values=["multiple_choice", "fill_blank", "true_false", "matching"], 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        type_combo.set("multiple_choice")
        type_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Lesson:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load lessons
        try:
            conn = connect_db()
            lessons = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lesson_id, lesson_name FROM Lessons")
                lessons = cursor.fetchall()
                conn.close()
        except:
            lessons = []
        
        lesson_dict = {f"{l[1]} (ID: {l[0]})": l[0] for l in lessons}
        lesson_dict["Không gán"] = None
        lesson_names = list(lesson_dict.keys())
        
        lesson_combo = ttk.Combobox(form, values=lesson_names, 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        lesson_combo.set("Không gán")
        lesson_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load units
        try:
            conn = connect_db()
            units = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT unit_id, unit_name FROM Units")
                units = cursor.fetchall()
                conn.close()
        except:
            units = []
        
        unit_dict = {f"{u[1]} (ID: {u[0]})": u[0] for u in units}
        unit_dict["Không gán"] = None
        unit_names = list(unit_dict.keys())
        
        unit_combo = ttk.Combobox(form, values=unit_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        unit_combo.set("Không gán")
        unit_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def save_question():
            content = content_text.get("1.0", "end-1c").strip()
            answer = answer_entry.get().strip()
            q_type = type_combo.get()
            lesson_str = lesson_combo.get()
            unit_str = unit_combo.get()
            
            if not content or not answer:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            lesson_id = lesson_dict.get(lesson_str)
            unit_id = unit_dict.get(unit_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO Questions (question_content, question_answer, question_type, question_lesson_id, question_unit_id) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (content, answer, q_type, lesson_id, unit_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm Question mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm Question:\n{e}")

        btn = tk.Button(form, text="💾 Thêm Question", command=save_question,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_question(self, question_id):
        # Get current question data
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT question_content, question_answer, question_type, question_lesson_id, question_unit_id
                FROM Questions WHERE question_id=%s
            """, (question_id,))
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy câu hỏi!")
                return
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            return

        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa Question")
        win.geometry("700x750")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa Question ID: {question_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Nội dung câu hỏi:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=5, font=("Segoe UI", 11))
        content_text.insert("1.0", data[0] if data[0] else "")
        content_text.pack(pady=(0, 15), fill="x")

        tk.Label(form, text="Đáp án đúng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        answer_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        answer_entry.insert(0, data[1] if data[1] else "")
        answer_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Loại câu hỏi:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        type_combo = ttk.Combobox(form, values=["multiple_choice", "fill_blank", "true_false", "matching"], 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        type_combo.set(data[2] if data[2] else "multiple_choice")
        type_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Lesson:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load lessons
        try:
            conn = connect_db()
            lessons = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lesson_id, lesson_name FROM Lessons")
                lessons = cursor.fetchall()
                conn.close()
        except:
            lessons = []
        
        lesson_dict = {f"{l[1]} (ID: {l[0]})": l[0] for l in lessons}
        lesson_dict["Không gán"] = None
        lesson_names = list(lesson_dict.keys())
        
        lesson_combo = ttk.Combobox(form, values=lesson_names, 
                                   state="readonly", width=47, font=("Segoe UI", 11))
        if data[3]:
            for key, val in lesson_dict.items():
                if val == data[3]:
                    lesson_combo.set(key)
                    break
        else:
            lesson_combo.set("Không gán")
        lesson_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Thuộc Unit:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load units
        try:
            conn = connect_db()
            units = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT unit_id, unit_name FROM Units")
                units = cursor.fetchall()
                conn.close()
        except:
            units = []
        
        unit_dict = {f"{u[1]} (ID: {u[0]})": u[0] for u in units}
        unit_dict["Không gán"] = None
        unit_names = list(unit_dict.keys())
        
        unit_combo = ttk.Combobox(form, values=unit_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        if data[4]:
            for key, val in unit_dict.items():
                if val == data[4]:
                    unit_combo.set(key)
                    break
        else:
            unit_combo.set("Không gán")
        unit_combo.pack(pady=(0, 20), ipady=8, fill="x")

        def update_question():
            content = content_text.get("1.0", "end-1c").strip()
            answer = answer_entry.get().strip()
            q_type = type_combo.get()
            lesson_str = lesson_combo.get()
            unit_str = unit_combo.get()
            
            if not content or not answer:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            lesson_id = lesson_dict.get(lesson_str)
            unit_id = unit_dict.get(unit_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Questions 
                        SET question_content=%s, question_answer=%s, question_type=%s, 
                            question_lesson_id=%s, question_unit_id=%s
                        WHERE question_id=%s
                    """, (content, answer, q_type, lesson_id, unit_id, question_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật Question!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_question,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def manage_options(self, question_id):
        """Manage question options"""
        win = tk.Toplevel(self.parent)
        win.title("⚙️ Quản lý Options")
        win.geometry("700x600")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#8B5CF6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"⚙️ Quản lý Options cho Question ID: {question_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#8B5CF6").pack(pady=25)

        # Load existing options
        try:
            conn = connect_db()
            options_data = None
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT option_1, option_2, option_3, option_4
                    FROM Question_options WHERE question_option_question_id=%s
                """, (question_id,))
                options_data = cursor.fetchone()
                conn.close()
        except:
            options_data = None

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Option 1:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        opt1_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        if options_data and options_data[0]:
            opt1_entry.insert(0, options_data[0])
        opt1_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Option 2:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        opt2_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        if options_data and options_data[1]:
            opt2_entry.insert(0, options_data[1])
        opt2_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Option 3:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        opt3_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        if options_data and options_data[2]:
            opt3_entry.insert(0, options_data[2])
        opt3_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Option 4:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        opt4_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        if options_data and options_data[3]:
            opt4_entry.insert(0, options_data[3])
        opt4_entry.pack(pady=(0, 20), ipady=8, fill="x")

        def save_options():
            opt1 = opt1_entry.get().strip()
            opt2 = opt2_entry.get().strip()
            opt3 = opt3_entry.get().strip()
            opt4 = opt4_entry.get().strip()
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    if options_data:
                        # Update existing
                        cursor.execute("""
                            UPDATE Question_options 
                            SET option_1=%s, option_2=%s, option_3=%s, option_4=%s
                            WHERE question_option_question_id=%s
                        """, (opt1, opt2, opt3, opt4, question_id))
                    else:
                        # Insert new
                        cursor.execute("""
                            INSERT INTO Question_options (question_option_question_id, option_1, option_2, option_3, option_4)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (question_id, opt1, opt2, opt3, opt4))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã lưu Options!")
                    win.destroy()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể lưu Options:\n{e}")

        btn = tk.Button(form, text="💾 Lưu Options", command=save_options,
                       font=("Segoe UI", 12, "bold"), bg="#8B5CF6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#7C3AED"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#8B5CF6"))

    def delete_question(self, question_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa Question ID {question_id}?\n\n" +
                                  "Lưu ý: Tất cả Options liên quan sẽ bị xóa!"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Questions WHERE question_id=%s", (question_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa Question!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# 📰 MODULE QUẢN LÝ READING
# ===============================
class AdminReading:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="📰 Quản lý Reading (Đọc hiểu)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_reading())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_reading, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm Reading", self.add_reading, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("QuestionID", "Content", "ReadingContent", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("QuestionID", "Question ID", 120),
            ("Content", "Câu hỏi", 300),
            ("ReadingContent", "Nội dung đọc", 400),
            ("Actions", "Thao tác", 150)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["QuestionID", "Actions"] else "w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#4":
                values = self.tree.item(item)['values']
                question_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_reading(question_id))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_reading(question_id))
                
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
            cursor.execute("""
                SELECT r.reading_question_id, q.question_content, r.reading_content
                FROM Readings r
                LEFT JOIN Questions q ON r.reading_question_id = q.question_id
                ORDER BY r.reading_question_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            q_content = r[1][:40] + "..." if r[1] and len(r[1]) > 40 else r[1]
            r_content = r[2][:60] + "..." if r[2] and len(r[2]) > 60 else r[2]
            self.tree.insert("", "end", values=(r[0], q_content, r_content, "✏️ | 🗑️"))

    def search_reading(self):
        key = self.search_var.get().strip()
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.reading_question_id, q.question_content, r.reading_content
                FROM Readings r
                LEFT JOIN Questions q ON r.reading_question_id = q.question_id
                WHERE r.reading_content LIKE %s OR q.question_content LIKE %s OR r.reading_question_id LIKE %s
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy reading nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_reading(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm Reading mới")
        win.geometry("700x600")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm Reading mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Question ID (phải tồn tại):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        
        # Load available questions
        try:
            conn = connect_db()
            questions = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT q.question_id, q.question_content 
                    FROM Questions q
                    WHERE q.question_id NOT IN (SELECT reading_question_id FROM Readings)
                    ORDER BY q.question_id
                """)
                questions = cursor.fetchall()
                conn.close()
        except:
            questions = []
        
        question_dict = {f"ID {q[0]}: {q[1][:50]}...": q[0] for q in questions}
        question_names = list(question_dict.keys())
        
        question_combo = ttk.Combobox(form, values=question_names, 
                                     state="readonly", width=57, font=("Segoe UI", 10))
        if question_names:
            question_combo.set(question_names[0])
        question_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nội dung đọc hiểu:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=12, font=("Segoe UI", 11))
        content_text.pack(pady=(0, 20), fill="both", expand=True)

        def save_reading():
            question_str = question_combo.get()
            content = content_text.get("1.0", "end-1c").strip()
            
            if not question_str or not content:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            question_id = question_dict.get(question_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO Readings (reading_question_id, reading_content) 
                        VALUES (%s, %s)
                    """, (question_id, content))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm Reading mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm Reading:\n{e}")

        btn = tk.Button(form, text="💾 Thêm Reading", command=save_reading,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_reading(self, question_id):
        # Get current reading data
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT reading_content FROM Readings WHERE reading_question_id=%s
            """, (question_id,))
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy reading!")
                return
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            return

        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa Reading")
        win.geometry("700x600")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa Reading (Question ID: {question_id})",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Nội dung đọc hiểu:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=15, font=("Segoe UI", 11))
        content_text.insert("1.0", data[0] if data[0] else "")
        content_text.pack(pady=(0, 20), fill="both", expand=True)

        def update_reading():
            content = content_text.get("1.0", "end-1c").strip()
            
            if not content:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập nội dung đọc!")
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Readings SET reading_content=%s WHERE reading_question_id=%s
                    """, (content, question_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật Reading!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_reading,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def delete_reading(self, question_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa Reading (Question ID: {question_id})?"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Readings WHERE listening_question_id=%s", (question_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa Reading!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# 🎧 MODULE QUẢN LÝ LISTENING
# ===============================
class AdminListening:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="🎧 Quản lý Listening (Nghe)", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
        action_panel = tk.Frame(container, bg="white", relief="flat", bd=0)
        action_panel.pack(fill="x", pady=(0, 20))
        action_panel.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        action_container = tk.Frame(action_panel, bg="white")
        action_container.pack(fill="x", padx=20, pady=15)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_listening())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_listening, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm Listening", self.add_listening, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("QuestionID", "Content", "Audio", "ListeningContent", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("QuestionID", "Question ID", 100),
            ("Content", "Câu hỏi", 250),
            ("Audio", "Audio File", 200),
            ("ListeningContent", "Nội dung nghe", 300),
            ("Actions", "Thao tác", 150)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ["QuestionID", "Actions"] else "w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#5":
                values = self.tree.item(item)['values']
                question_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_listening(question_id))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_listening(question_id))
                
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
            cursor.execute("""
                SELECT l.listening_question_id, q.question_content, l.listening_audio, l.listening_content
                FROM Listenings l
                LEFT JOIN Questions q ON l.listening_question_id = q.question_id
                ORDER BY l.listening_question_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            q_content = r[1][:35] + "..." if r[1] and len(r[1]) > 35 else r[1]
            audio = r[2][:30] + "..." if r[2] and len(r[2]) > 30 else r[2]
            l_content = r[3][:45] + "..." if r[3] and len(r[3]) > 45 else r[3]
            self.tree.insert("", "end", values=(r[0], q_content, audio, l_content, "✏️ | 🗑️"))

    def search_listening(self):
        key = self.search_var.get().strip()
        if not key:
            self.load_data()
            return
            
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.listening_question_id, q.question_content, l.listening_audio, l.listening_content
                FROM Listenings l
                LEFT JOIN Questions q ON l.listening_question_id = q.question_id
                WHERE l.listening_content LIKE %s OR l.listening_audio LIKE %s OR q.question_content LIKE %s OR l.listening_question_id LIKE %s
            """, (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy listening nào phù hợp!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khi tìm kiếm:\n{e}")

    def add_listening(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm Listening mới")
        win.geometry("700x650")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm Listening mới vào hệ thống",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Question ID (phải tồn tại):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        
        # Load available questions
        try:
            conn = connect_db()
            questions = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT q.question_id, q.question_content 
                    FROM Questions q
                    WHERE q.question_id NOT IN (SELECT listening_question_id FROM Listenings)
                    ORDER BY q.question_id
                """)
                questions = cursor.fetchall()
                conn.close()
        except:
            questions = []
        
        question_dict = {f"ID {q[0]}: {q[1][:50]}...": q[0] for q in questions}
        question_names = list(question_dict.keys())
        
        question_combo = ttk.Combobox(form, values=question_names, 
                                     state="readonly", width=57, font=("Segoe UI", 10))
        if question_names:
            question_combo.set(question_names[0])
        question_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Audio File Path:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        audio_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        audio_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nội dung nghe (transcript):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=10, font=("Segoe UI", 11))
        content_text.pack(pady=(0, 20), fill="both", expand=True)

        def save_listening():
            question_str = question_combo.get()
            audio = audio_entry.get().strip()
            content = content_text.get("1.0", "end-1c").strip()
            
            if not question_str or not audio or not content:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            question_id = question_dict.get(question_str)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO Listenings (listening_question_id, listening_audio, listening_content) 
                        VALUES (%s, %s, %s)
                    """, (question_id, audio, content))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm Listening mới!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm Listening:\n{e}")

        btn = tk.Button(form, text="💾 Thêm Listening", command=save_listening,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_listening(self, question_id):
        # Get current listening data
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT listening_audio, listening_content FROM Listenings WHERE listening_question_id=%s
            """, (question_id,))
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy listening!")
                return
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            return

        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa Listening")
        win.geometry("700x650")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa Listening (Question ID: {question_id})",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Audio File Path:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        audio_entry = ttk.Entry(form, width=60, font=("Segoe UI", 11))
        audio_entry.insert(0, data[0] if data[0] else "")
        audio_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Nội dung nghe (transcript):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        content_text = scrolledtext.ScrolledText(form, width=60, height=12, font=("Segoe UI", 11))
        content_text.insert("1.0", data[1] if data[1] else "")
        content_text.pack(pady=(0, 20), fill="both", expand=True)

        def update_listening():
            audio = audio_entry.get().strip()
            content = content_text.get("1.0", "end-1c").strip()
            
            if not audio or not content:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Listenings SET listening_audio=%s, listening_content=%s WHERE listening_question_id=%s
                    """, (audio, content, question_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật Listening!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_listening,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def delete_listening(self, question_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa Listening (Question ID: {question_id})?"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Listenings WHERE listening_question_id=%s", (question_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa Listening!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{e}")


# ===============================
# 👥 MODULE QUẢN LÝ NGƯỜI DÙNG
# ===============================
class AdminUsers:
    def __init__(self, parent):
        self.parent = parent
        self.search_var = tk.StringVar()
        self.search_type_var = tk.StringVar(value="all")

        container = tk.Frame(parent, bg="#E8F4F8")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Frame(container, bg="#E8F4F8")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="👥 Quản lý người dùng", font=("Segoe UI", 28, "bold"),
                 fg="#1E3A8A", bg="#E8F4F8").pack(side="left")

        # Action Panel
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
                                 state="readonly", width=12, font=("Segoe UI", 10))
        type_combo['values'] = ["Tất cả", "ID", "Tên", "Cấp độ"]
        type_combo.set("Tất cả")
        type_combo.pack(side=tk.LEFT, ipady=5)

        # Search box
        search_frame = tk.Frame(action_container, bg="#F1F5F9", relief="flat", bd=0)
        search_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 15))
        
        tk.Label(search_frame, text="🔍", bg="#F1F5F9", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(15, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25, font=("Segoe UI", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=8, fill="x", expand=True)
        search_entry.bind("<Return>", lambda e: self.search_user())

        # Action buttons
        button_frame = tk.Frame(action_container, bg="white")
        button_frame.pack(side=tk.RIGHT)

        self.make_button(button_frame, "Tìm kiếm", self.search_user, "#3B82F6").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "Làm mới", self.load_data, "#6366F1").pack(side=tk.LEFT, padx=5)
        self.make_button(button_frame, "➕ Thêm user", self.add_user, "#10B981").pack(side=tk.LEFT, padx=5)

        # Table
        table_container = tk.Frame(container, bg="white", relief="flat", bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#CBD5E1", highlightthickness=1)

        columns = ("ID", "Username", "Role", "Rank", "Level", "Status", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=20)
        
        col_config = [
            ("ID", "ID", 70),
            ("Username", "Tên người dùng", 200),
            ("Role", "Vai trò", 120),
            ("Rank", "Xếp hạng", 100),
            ("Level", "Cấp độ", 100),
            ("Status", "Trạng thái", 120),
            ("Actions", "Thao tác", 180)
        ]
        
        for col, text, w in col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col != "Username" else "w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))

        self.tree.bind("<Double-Button-1>", self.on_row_click)
        self.load_data()

    def on_row_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if item and column == "#7":
                values = self.tree.item(item)['values']
                user_id = values[0]
                
                menu = tk.Menu(self.parent, tearoff=0)
                menu.add_command(label="✏️ Chỉnh sửa", 
                               command=lambda: self.edit_user(user_id))
                menu.add_separator()
                menu.add_command(label="🔒 Khóa/Mở", 
                               command=lambda: self.toggle_status(user_id, values[5]))
                menu.add_separator()
                menu.add_command(label="🗑️ Xóa", 
                               command=lambda: self.delete_user(user_id))
                
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
            cursor.execute("""
                SELECT u.user_id, u.user_name, r.role_name, u.user_rank, u.user_level, u.user_status
                FROM Users u
                LEFT JOIN Roles r ON u.user_role_id = r.role_id
                ORDER BY u.user_id ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu:\n{e}")

    def update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            role_name = r[2] if r[2] else "User"
            status_text = "🟢 Active" if r[5] == 1 else "🔴 Locked"
            self.tree.insert("", "end", values=(r[0], r[1], role_name, r[3], r[4], status_text, "✏️ | 🗑️"))

    def search_user(self):
        key = self.search_var.get().strip()
        search_type = self.search_type_var.get()
        
        type_mapping = {
            "Tất cả": "all",
            "ID": "id",
            "Tên": "username",
            "Cấp độ": "level"
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
                    messagebox.showwarning("Lỗi", "ID phải là số!")
                    return
                cursor.execute("""
                    SELECT u.user_id, u.user_name, r.role_name, u.user_rank, u.user_level, u.user_status
                    FROM Users u LEFT JOIN Roles r ON u.user_role_id = r.role_id
                    WHERE u.user_id = %s
                """, (int(key),))
            elif search_type == "username":
                cursor.execute("""
                    SELECT u.user_id, u.user_name, r.role_name, u.user_rank, u.user_level, u.user_status
                    FROM Users u LEFT JOIN Roles r ON u.user_role_id = r.role_id
                    WHERE u.user_name LIKE %s
                """, (f"%{key}%",))
            elif search_type == "level":
                if not key.isdigit():
                    messagebox.showwarning("Lỗi", "Cấp độ phải là số!")
                    return
                cursor.execute("""
                    SELECT u.user_id, u.user_name, r.role_name, u.user_rank, u.user_level, u.user_status
                    FROM Users u LEFT JOIN Roles r ON u.user_role_id = r.role_id
                    WHERE u.user_level = %s
                """, (int(key),))
            else:
                cursor.execute("""
                    SELECT u.user_id, u.user_name, r.role_name, u.user_rank, u.user_level, u.user_status
                    FROM Users u LEFT JOIN Roles r ON u.user_role_id = r.role_id
                    WHERE u.user_name LIKE %s
                """, (f"%{key}%",))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("Kết quả", "Không tìm thấy!")
            
            self.update_table(rows)
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm:\n{e}")

    def add_user(self):
        win = tk.Toplevel(self.parent)
        win.title("➕ Thêm người dùng")
        win.geometry("600x700")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#10B981", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Thêm người dùng mới",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#10B981").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên người dùng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        username_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        username_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Mật khẩu:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        password_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11), show="*")
        password_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Vai trò:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load roles
        try:
            conn = connect_db()
            roles = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT role_id, role_name FROM Roles")
                roles = cursor.fetchall()
                conn.close()
        except:
            roles = []
        
        role_dict = {role[1]: role[0] for role in roles}
        role_names = list(role_dict.keys()) if role_dict else ["User"]
        
        role_combo = ttk.Combobox(form, values=role_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        role_combo.set(role_names[0] if role_names else "User")
        role_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Cấp độ:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        level_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        level_entry.insert(0, "1")
        level_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Xếp hạng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        rank_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        rank_entry.insert(0, "0")
        rank_entry.pack(pady=(0, 20), ipady=8, fill="x")

        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role_name = role_combo.get()
            level = level_entry.get().strip()
            rank = rank_entry.get().strip()
            
            if not username or not password:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập username và password!")
                return
            
            if not level.isdigit() or not rank.isdigit():
                messagebox.showwarning("Lỗi", "Level và Rank phải là số!")
                return
            
            role_id = role_dict.get(role_name, 1)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO Users (user_name, user_password, user_role_id, user_level, user_rank, user_status) 
                        VALUES (%s, %s, %s, %s, %s, 1)
                    """, (username, password, role_id, int(level), int(rank)))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã thêm người dùng!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể thêm:\n{e}")

        btn = tk.Button(form, text="💾 Thêm", command=save_user,
                       font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#10B981"))

    def edit_user(self, user_id):
        # Get current user data
        try:
            conn = connect_db()
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_name, user_role_id, user_level, user_rank
                FROM Users WHERE user_id=%s
            """, (user_id,))
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                messagebox.showerror("Lỗi", "Không tìm thấy user!")
                return
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            return

        win = tk.Toplevel(self.parent)
        win.title("✏️ Chỉnh sửa người dùng")
        win.geometry("600x700")
        win.configure(bg="#E8F4F8")
        win.resizable(False, False)

        header = tk.Frame(win, bg="#3B82F6", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"✏️ Chỉnh sửa User ID: {user_id}",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#3B82F6").pack(pady=25)

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(form, text="Tên người dùng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(15, 5))
        username_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        username_entry.insert(0, data[0])
        username_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Mật khẩu mới (để trống nếu không đổi):", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        password_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11), show="*")
        password_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Vai trò:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        
        # Load roles
        try:
            conn = connect_db()
            roles = []
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT role_id, role_name FROM Roles")
                roles = cursor.fetchall()
                conn.close()
        except:
            roles = []
        
        role_dict = {role[1]: role[0] for role in roles}
        role_names = list(role_dict.keys()) if role_dict else ["User"]
        
        role_combo = ttk.Combobox(form, values=role_names, 
                                 state="readonly", width=47, font=("Segoe UI", 11))
        # Set current role
        for name, rid in role_dict.items():
            if rid == data[1]:
                role_combo.set(name)
                break
        role_combo.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Cấp độ:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        level_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        level_entry.insert(0, str(data[2]))
        level_entry.pack(pady=(0, 15), ipady=8, fill="x")

        tk.Label(form, text="Xếp hạng:", bg="white", font=("Segoe UI", 11, "bold"),
                 fg="#1E3A8A").pack(anchor="w", pady=(0, 5))
        rank_entry = ttk.Entry(form, width=50, font=("Segoe UI", 11))
        rank_entry.insert(0, str(data[3]))
        rank_entry.pack(pady=(0, 20), ipady=8, fill="x")

        def update_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role_name = role_combo.get()
            level = level_entry.get().strip()
            rank = rank_entry.get().strip()
            
            if not username:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập username!")
                return
            
            if not level.isdigit() or not rank.isdigit():
                messagebox.showwarning("Lỗi", "Level và Rank phải là số!")
                return
            
            role_id = role_dict.get(role_name, 1)
            
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    if password:
                        cursor.execute("""
                            UPDATE Users 
                            SET user_name=%s, user_password=%s, user_role_id=%s, user_level=%s, user_rank=%s 
                            WHERE user_id=%s
                        """, (username, password, role_id, int(level), int(rank), user_id))
                    else:
                        cursor.execute("""
                            UPDATE Users 
                            SET user_name=%s, user_role_id=%s, user_level=%s, user_rank=%s 
                            WHERE user_id=%s
                        """, (username, role_id, int(level), int(rank), user_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Đã cập nhật!")
                    win.destroy()
                    self.load_data()
            except Error as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

        btn = tk.Button(form, text="💾 Cập nhật", command=update_user,
                       font=("Segoe UI", 12, "bold"), bg="#3B82F6", fg="white",
                       cursor="hand2", bd=0, relief="flat", padx=40, pady=12)
        btn.pack(pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))

    def toggle_status(self, user_id, current_status):
        is_active = "Active" in current_status
        new_status = 0 if is_active else 1
        action = "khóa" if is_active else "mở khóa"
        
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn {action} user ID {user_id}?"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Users SET user_status=%s WHERE user_id=%s", (new_status, user_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", f"Đã {action} người dùng!")
                self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")

    def delete_user(self, user_id):
        if not messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc muốn xóa user ID {user_id}?\n\n" +
                                  "Hành động này không thể hoàn tác!"):
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Users WHERE user_id=%s", (user_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa người dùng!")
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