import mysql.connector
from model.question import Question

# ===============================
# KẾT NỐI CƠ SỞ DỮ LIỆU
# ===============================
def connect_db():
    """Kết nối tới MySQL — chỉnh thông tin nếu cần."""
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",   # điền nếu có mật khẩu
        database="bleu"
    )

# ===============================
# LẤY DANH SÁCH QUESTIONS
# ===============================
def get_all_questions():
    """
    Lấy toàn bộ câu hỏi trong bảng Questions.
    Trả về danh sách các đối tượng Question.
    """
    questions = []
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT question_id, question_lesson_id, question_unit_id,
                   question_content, question_answer, question_type
            FROM Questions
            ORDER BY question_id;
        """)
        rows = cursor.fetchall()

        for row in rows:
            q = Question(
                question_id=row[0],
                question_lesson_id=row[1],
                question_unit_id=row[2],
                question_content=row[3],
                question_answer=row[4],
                question_type=row[5]
            )
            questions.append(q)

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print("❌ Lỗi lấy Questions:", e)
    except Exception as e:
        print("❌ Lỗi không xác định khi lấy Questions:", e)

    return questions
