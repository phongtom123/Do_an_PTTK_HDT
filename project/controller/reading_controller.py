import mysql.connector
from model.reading import Reading

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bleu"
    )

def get_readings_by_lesson_id(lesson_id):
    """Lấy danh sách Reading theo lesson_id."""
    readings = []
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.reading_question_id, r.reading_content,
                   q.question_id, q.question_lesson_id, q.question_unit_id,
                   q.question_content, q.question_answer, q.question_type
            FROM Readings r
            JOIN Questions q ON r.reading_question_id = q.question_id
            WHERE q.question_lesson_id = %s;
        """, (lesson_id,))

        for row in cursor.fetchall():
            reading = Reading(
                reading_question_id=row[0],
                reading_content=row[1],
                question_id=row[2],
                question_lesson_id=row[3],
                question_unit_id=row[4],
                question_content=row[5],
                question_answer=row[6],
                question_type=row[7]
            )
            readings.append(reading)

        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Lỗi lấy Reading:", e)

    return readings
