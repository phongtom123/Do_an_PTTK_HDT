# controller/lesson_controller.py

import mysql.connector
from model.lesson import Lesson

def get_lessons_by_unit_id(unit_id):
    """Lấy danh sách Lesson thuộc Unit cụ thể từ MySQL."""
    lessons = []
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="bleu"
        )
        cursor = conn.cursor()
        query = "SELECT lesson_id, lesson_name FROM Lessons WHERE lesson_unit_id = %s"
        cursor.execute(query, (unit_id,))
        for (lesson_id, lesson_name) in cursor.fetchall():
            lessons.append(Lesson(lesson_id, lesson_name, unit_id))
    except Exception as e:
        print(f"❌ Lỗi khi lấy Lessons cho Unit {unit_id}: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return lessons
