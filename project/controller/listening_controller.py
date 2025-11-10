import mysql.connector
from model.listening import Listening


def connect_db():
    """Kết nối tới cơ sở dữ liệu."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # sửa nếu MySQL có password
        database="bleu"
    )


def get_listenings_by_lesson_id(lesson_id):
    """Lấy danh sách Listening theo lesson_id."""
    listenings = []
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.listening_question_id, l.listening_content, l.listening_audio,
                   q.question_id, q.question_lesson_id, q.question_unit_id,
                   q.question_content, q.question_answer, q.question_type
            FROM Listenings l
            JOIN Questions q ON l.listening_question_id = q.question_id
            WHERE q.question_lesson_id = %s;
        """, (lesson_id,))

        for row in cursor.fetchall():
            listen = Listening(
                listening_question_id=row[0],
                listening_content=row[1],
                listening_audio=row[2],
                question_id=row[3],
                question_lesson_id=row[4],
                question_unit_id=row[5],
                question_content=row[6],
                question_answer=row[7],
                question_type=row[8]
            )
            listenings.append(listen)

        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Lỗi lấy Listening:", e)

    return listenings
