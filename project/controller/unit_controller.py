# controller/unit_controller.py
import mysql.connector

def connect_db():
    """Kết nối tới MySQL — chỉnh thông tin nếu cần."""
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="bleu"
    )

def _try_queries(conn, queries):
    """Thử các query trong danh sách, trả về rows của query thành công đầu tiên."""
    cursor = conn.cursor()
    last_exc = None
    for q in queries:
        try:
            cursor.execute(q)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except mysql.connector.Error as e:
            # lưu exception rồi thử query tiếp
            last_exc = e
    cursor.close()
    # nếu tới đây thì tất cả queries đều thất bại
    raise last_exc

def get_all_units():
    """
    Lấy danh sách Unit từ DB. Hàm cố gắng thử nhiều tên bảng / cột phổ biến để tránh lỗi case/ten cot.
    Trả về danh sách các tên unit (strings).
    """
    try:
        conn = connect_db()

        # Các truy vấn dự phòng (thứ tự ưu tiên)
        queries = [
            # bảng Unit, cột unitName (theo câu bạn mô tả ban đầu)
            "SELECT unitName FROM `Unit`",
            "SELECT unitName FROM Unit",
        ]

        rows = _try_queries(conn, queries)
        conn.close()

        # rows có thể là list các tuple: [(u1,), (u2,), ...]
        return [r[0] for r in rows]

    except mysql.connector.Error as e:
        print("❌ Lỗi lấy Unit:", e)
        return []
    except Exception as e:
        print("❌ Lỗi không xác định khi lấy Unit:", e)
        return []
