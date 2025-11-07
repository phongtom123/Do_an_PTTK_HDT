import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# --- Kết nối database ---
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="bleu"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {err}")
        return None

# --- Hiển thị USER ---
def show_users():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT user_ID, createDate, name, email, account, level, progress
            FROM USER
        """)
        rows = cursor.fetchall()

        for row in tree_user.get_children():
            tree_user.delete(row)

        for r in rows:
            tree_user.insert("", "end", values=r)
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu USER: {err}")
    finally:
        conn.close()

# --- Hiển thị Unit ---
def show_units():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT unit_ID, unitName FROM Unit")
        rows = cursor.fetchall()

        for row in tree_unit.get_children():
            tree_unit.delete(row)

        for r in rows:
            tree_unit.insert("", "end", values=r)
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu Unit: {err}")
    finally:
        conn.close()

# --- Hiển thị Lesson (Reading + Listening) ---
def show_lessons():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                l.lesson_ID,
                l.lessonName,
                u.unitName,
                CASE
                    WHEN r.read_ID IS NOT NULL THEN 'Reading'
                    WHEN li.listen_ID IS NOT NULL THEN 'Listening'
                    ELSE 'Lesson'
                END AS lessonType,
                COALESCE(r.readContent, li.linkAudio, '') AS content
            FROM Lesson l
            JOIN Unit u ON l.unit_ID = u.unit_ID
            LEFT JOIN Reading r ON l.lesson_ID = r.lesson_ID
            LEFT JOIN Listening li ON l.lesson_ID = li.lesson_ID
            ORDER BY l.lesson_ID;
        """)
        
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong treeview
        for row in tree_lesson.get_children():
            tree_lesson.delete(row)

        # Thêm dữ liệu mới
        for r in rows:
            tree_lesson.insert("", "end", values=r)

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu Lesson: {err}")
    finally:
        conn.close()


# --- Giao diện chính ---
root = Tk()
root.title("Quản lý BLEU Database")
root.geometry("950x500")
root.configure(bg="#f5f5f5")

Label(root, text="Quản lý dữ liệu BLEU", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

# Tạo tab
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

# --- Tab 1: USER ---
frame_user = Frame(notebook, bg="#f5f5f5")
columns_user = ("ID", "Ngày tạo", "Tên", "Email", "Tài khoản", "Level", "Tiến độ")
tree_user = ttk.Treeview(frame_user, columns=columns_user, show="headings")

for col in columns_user:
    tree_user.heading(col, text=col)
    tree_user.column(col, width=120, anchor="center")
tree_user.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_user, text="Tải danh sách USER", command=show_users, bg="#4CAF50", fg="white").pack(pady=5)
notebook.add(frame_user, text="👤 Người dùng")

# --- Tab 2: Unit ---
frame_unit = Frame(notebook, bg="#f5f5f5")
columns_unit = ("ID Unit", "Tên Unit")
tree_unit = ttk.Treeview(frame_unit, columns=columns_unit, show="headings")

for col in columns_unit:
    tree_unit.heading(col, text=col)
    tree_unit.column(col, width=200, anchor="center")
tree_unit.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_unit, text="Tải danh sách Unit", command=show_units, bg="#2196F3", fg="white").pack(pady=5)
notebook.add(frame_unit, text="📘 Unit")

# --- Tab 3: Lesson ---
frame_lesson = Frame(notebook, bg="#f5f5f5")
columns_lesson = ("ID", "Tên bài học", "Thuộc Unit", "Loại bài", "Nội dung / Link")
tree_lesson = ttk.Treeview(frame_lesson, columns=columns_lesson, show="headings")

for col in columns_lesson:
    tree_lesson.heading(col, text=col)
    if col in ("ID", "Loại bài"):
        tree_lesson.column(col, width=100, anchor="center")
    elif col == "Nội dung / Link":
        tree_lesson.column(col, width=250)
    else:
        tree_lesson.column(col, width=180, anchor="center")

tree_lesson.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_lesson, text="Tải danh sách Lesson", command=show_lessons, bg="#FF9800", fg="white").pack(pady=5)
notebook.add(frame_lesson, text="📖 Lesson")

root.mainloop()
