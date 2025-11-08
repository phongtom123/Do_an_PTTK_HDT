# utils/connector.py
import mysql.connector

def connect_db():
    """Kết nối tới MySQL"""
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="bleu"
    )
