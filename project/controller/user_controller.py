# controller/user_controller.py
import mysql.connector
from model.user import User  # ✅ import model User


# ===============================
# KẾT NỐI CƠ SỞ DỮ LIỆU
# ===============================
def connect_db():
    """Kết nối tới MySQL — chỉnh thông tin nếu cần."""
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",   # thêm mật khẩu nếu cần
        database="bleu"
    )


# ===============================
# LẤY DANH SÁCH TOÀN BỘ NGƯỜI DÙNG
# ===============================
def get_all_users():
    """
    Lấy danh sách toàn bộ người dùng từ bảng Users.
    Trả về danh sách đối tượng User.
    """
    users = []
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, user_name, user_password, user_role_id, 
                   user_rank, user_level, user_status
            FROM Users
            ORDER BY user_rank DESC;
        """)

        for row in cursor.fetchall():
            user = User(
                user_id=row[0],
                user_name=row[1],
                user_password=row[2],
                user_role_id=row[3],
                user_rank=row[4],
                user_level=row[5],
                user_status=row[6]
            )
            users.append(user)

        cursor.close()
        conn.close()
        return users

    except mysql.connector.Error as e:
        print("❌ Lỗi khi lấy danh sách Users:", e)
        return []
    except Exception as e:
        print("❌ Lỗi không xác định khi lấy Users:", e)
        return []


# ===============================
# LẤY USER THEO ID
# ===============================
def get_user_by_id(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, user_name, user_password, user_role_id,
                   user_rank, user_level, user_status
            FROM Users
            WHERE user_id = %s;
        """, (user_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return User(*row)
        return None
    except mysql.connector.Error as e:
        print("❌ Lỗi khi lấy thông tin user:", e)
        return None


# ===============================
# THÊM USER
# ===============================
def add_user(user: User):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Users (user_name, user_password, user_role_id, user_rank, user_level, user_status)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            user.get_user_name(),
            user.get_user_password(),
            user.get_user_role_id(),
            user.get_user_rank(),
            user.get_user_level(),
            user.get_user_status()
        ))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print("❌ Lỗi khi thêm user:", e)
        return False


# ===============================
# CẬP NHẬT RANK
# ===============================
def update_user_rank(user_id, new_rank):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Users
            SET user_rank = %s
            WHERE user_id = %s;
        """, (new_rank, user_id))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print("❌ Lỗi khi cập nhật rank user:", e)
        return False
