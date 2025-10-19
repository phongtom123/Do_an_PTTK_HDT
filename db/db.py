import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="bleu"
    )

def show_users():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT user_ID, name, email, level, progress FROM USER")
    rows = cursor.fetchall()
    
    for row in tree.get_children():
        tree.delete(row)

    for r in rows:
        tree.insert("", "end", values=r)
    
    conn.close()

root = Tk()
root.title("Quản lý người dùng - BELU")
root.geometry("700x400")

Label(root, text="Danh sách người dùng", font=("Arial", 16, "bold")).pack(pady=10)

columns = ("ID", "Tên", "Email", "Level", "Tiến độ")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor="center")

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

Button(root, text="Tải danh sách", command=show_users, bg="#4CAF50", fg="white").pack(pady=5)

root.mainloop()
