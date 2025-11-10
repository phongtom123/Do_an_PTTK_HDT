import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# ===============================
#  KẾT NỐI DATABASE
# ===============================
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="bleu"
        )
        print("Kết nối MySQL thành công!")
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {err}")
        return None

# ===============================
#  HIỂN THỊ USERS
# ===============================
def show_users():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                u.user_id,
                u.user_name,
                r.role_name,
                u.user_rank,
                u.user_level,
                u.user_status
            FROM Users u
            LEFT JOIN Roles r ON u.user_role_id = r.role_id
            ORDER BY u.user_id;
        """)
        rows = cursor.fetchall()

        for row in tree_user.get_children():
            tree_user.delete(row)

        for r in rows:
            status = "Hoạt động" if r[5] == 1 else "Bị khóa"
            tree_user.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], status))
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu Users: {err}")
    finally:
        conn.close()

# ===============================
#  HIỂN THỊ UNITS
# ===============================
def show_units():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT unit_id, unit_name FROM Units ORDER BY unit_id;")
        rows = cursor.fetchall()

        for row in tree_unit.get_children():
            tree_unit.delete(row)

        for r in rows:
            tree_unit.insert("", "end", values=r)
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu Units: {err}")
    finally:
        conn.close()

def show_lessons():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT DISTINCT
                l.lesson_id,
                l.lesson_name,
                u.unit_name,
                CASE
                    WHEN r.reading_question_id IS NOT NULL THEN 'Reading'
                    WHEN li.listening_question_id IS NOT NULL THEN 'Listening'
                    ELSE 'Bài học thường'
                END AS lesson_type,
                COALESCE(r.reading_content, li.listening_content, '') AS content
            FROM Lessons l
            JOIN Units u ON l.lesson_unit_id = u.unit_id
            LEFT JOIN Questions q ON q.question_lesson_id = l.lesson_id
            LEFT JOIN Readings r ON r.reading_question_id = q.question_id
            LEFT JOIN Listenings li ON li.listening_question_id = q.question_id
            ORDER BY l.lesson_id;
        """)
        rows = cursor.fetchall()

        for row in tree_lesson.get_children():
            tree_lesson.delete(row)

        for r in rows:
            tree_lesson.insert("", "end", values=r)
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi truy vấn", f"Không thể lấy dữ liệu Lessons: {err}")
    finally:
        conn.close()


# ===============================
#  GIAO DIỆN CHÍNH
# ===============================
root = Tk()
root.title("Quản lý CSDL BLEU")
root.geometry("1000x550")
root.configure(bg="#f5f5f5")

Label(root, text="Quản lý dữ liệu BLEU", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

# --- Tab 1: USERS ---
frame_user = Frame(notebook, bg="#f5f5f5")
columns_user = ("ID", "Tên người dùng", "Vai trò", "Xếp hạng", "Cấp độ", "Trạng thái")
tree_user = ttk.Treeview(frame_user, columns=columns_user, show="headings")

for col in columns_user:
    tree_user.heading(col, text=col)
    tree_user.column(col, width=140, anchor="center")

tree_user.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_user, text="Tải danh sách Users", command=show_users, bg="#4CAF50", fg="white").pack(pady=5)
notebook.add(frame_user, text="👤 Người dùng")

# --- Tab 2: UNITS ---
frame_unit = Frame(notebook, bg="#f5f5f5")
columns_unit = ("ID Unit", "Tên Unit")
tree_unit = ttk.Treeview(frame_unit, columns=columns_unit, show="headings")

for col in columns_unit:
    tree_unit.heading(col, text=col)
    tree_unit.column(col, width=200, anchor="center")

tree_unit.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_unit, text="Tải danh sách Units", command=show_units, bg="#2196F3", fg="white").pack(pady=5)
notebook.add(frame_unit, text="📘 Units")

# --- Tab 3: LESSONS ---
frame_lesson = Frame(notebook, bg="#f5f5f5")
columns_lesson = ("ID", "Tên bài học", "Thuộc Unit", "Loại bài", "Nội dung / Link")
tree_lesson = ttk.Treeview(frame_lesson, columns=columns_lesson, show="headings")

for col in columns_lesson:
    tree_lesson.heading(col, text=col)
    if col in ("ID", "Loại bài"):
        tree_lesson.column(col, width=100, anchor="center")
    elif col == "Nội dung / Link":
        tree_lesson.column(col, width=300)
    else:
        tree_lesson.column(col, width=180, anchor="center")

tree_lesson.pack(fill=BOTH, expand=True, padx=10, pady=10)
Button(frame_lesson, text="Tải danh sách Lessons", command=show_lessons, bg="#FF9800", fg="white").pack(pady=5)
notebook.add(frame_lesson, text="📖 Lessons")

root.mainloop()
