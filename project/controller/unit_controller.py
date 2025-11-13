# controller/unit_controller.py
import mysql.connector

# ===============================
# KẾT NỐI CƠ SỞ DỮ LIỆU
# ===============================
def connect_db():
    """Kết nối tới MySQL — chỉnh thông tin nếu cần."""
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",   # nếu bạn có mật khẩu thì thêm vào đây
        database="bleu1"
    )

# ===============================
# LẤY DANH SÁCH UNIT
# ===============================
def get_all_units():
    """
    Lấy danh sách tất cả Units trong database 'bleu1'.
    Trả về danh sách tuple (unit_id, unit_name)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT unit_id, unit_name
            FROM Units
            ORDER BY unit_id;
        """)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except mysql.connector.Error as e:
        print("❌ Lỗi lấy Units:", e)
        return []
    except Exception as e:
        print("❌ Lỗi không xác định khi lấy Units:", e)
        return []
