import mysql.connector
from tkinter import *
from tkinter import messagebox

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",       
            port=3306,               # cổng map trong Docker
            user="root",
            password="matkhau",
            database="belu"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Lỗi kết nối MySQL: {err}")
        return None
