from tkinter import *
from tkinter import ttk, messagebox
from db_connector import connect_db
from models import Lesson, Reading, Listening


# --- LẤY DỮ LIỆU TỪ DATABASE ---
def load_lessons():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Lesson")
    lesson_rows = cursor.fetchall()
    lessons = []

    for lesson in lesson_rows:
        cursor.execute("SELECT * FROM Reading WHERE lesson_ID = %s", (lesson["lesson_ID"],))
        reading = cursor.fetchone()

        cursor.execute("SELECT * FROM Listening WHERE lesson_ID = %s", (lesson["lesson_ID"],))
        listening = cursor.fetchone()

        if reading:
            lessons.append(Reading(
                lesson["lesson_ID"],
                lesson["unit_ID"],
                lesson["lessonName"],
                reading["readContent"]
            ))
        elif listening:
            lessons.append(Listening(
                lesson["lesson_ID"],
                lesson["unit_ID"],
                lesson["lessonName"],
                listening["linkAudio"]
            ))
        else:
            lessons.append(Lesson(
                lesson["lesson_ID"],
                lesson["unit_ID"],
                lesson["lessonName"]
            ))

    conn.close()
    return lessons


# --- HIỂN THỊ TRÊN GIAO DIỆN ---
def show_lessons():
    for row in tree.get_children():
        tree.delete(row)

    lessons = load_lessons()
    for l in lessons:
        if isinstance(l, Reading):
            type_ = "Reading"
            content = l.readContent
        elif isinstance(l, Listening):
            type_ = "Listening"
            content = l.linkAudio
        else:
            type_ = "Lesson"
            content = ""
        tree.insert("", "end", values=(l.lesson_ID, l.unit_ID, l.lessonName, type_, content))


# --- GIAO DIỆN TKINTER ---
root = Tk()
root.title("Quản lý Lesson")
root.geometry("850x400")

Label(root, text="Danh sách Lesson", font=("Arial", 16, "bold")).pack(pady=10)

columns = ("ID", "Unit", "Tên bài học", "Loại", "Nội dung / Link")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

Button(root, text="Tải dữ liệu Lesson", command=show_lessons, bg="#4CAF50", fg="white").pack(pady=5)

root.mainloop()
