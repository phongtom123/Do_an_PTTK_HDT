import mysql.connector

def clear_database():
    conn = None
    cursor = None
    try:
        # 🔗 Kết nối tới MySQL
        conn = mysql.connector.connect(
            host="localhost",        # Nếu dùng Docker: "127.0.0.1"
            user="root",             # Tài khoản MySQL
            password="",             # Không mật khẩu (container mysql-nopass)
            database="bleu"          # Tên cơ sở dữ liệu
        )
        cursor = conn.cursor()

        print("✅ Đã kết nối đến cơ sở dữ liệu 'bleu'.")
        print("🔧 Đang chuẩn bị làm sạch dữ liệu...\n")

        # 🚫 Tạm thời tắt kiểm tra khóa ngoại
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # ⚙️ Cố gắng xóa khóa chính trong bảng Learn (nếu có)
        try:
            cursor.execute("ALTER TABLE Learn DROP PRIMARY KEY;")
            print("🗝️ Đã xóa khóa chính trong bảng Learn.")
        except mysql.connector.Error as e:
            if "needed in a foreign key constraint" in str(e):
                print("⚠️ Không thể xóa khóa chính trong bảng Learn vì đang bị ràng buộc khóa ngoại.")
            elif "Can't DROP" in str(e):
                print("⚠️ Bảng Learn không có khóa chính để xóa.")
            else:
                print(f"⚠️ Lỗi khi xóa khóa chính trong bảng Learn: {e}")

        # 📋 Lấy toàn bộ bảng trong CSDL
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]

        if not tables:
            print("⚠️ Không có bảng nào trong cơ sở dữ liệu 'bleu'.")
        else:
            for table in tables:
                try:
                    cursor.execute(f"TRUNCATE TABLE `{table}`;")
                    print(f"✅ Đã xóa dữ liệu trong bảng: {table}")
                except mysql.connector.Error as e:
                    print(f"❌ Không thể xóa dữ liệu trong bảng {table}: {e}")

        print("\n🎉 Tất cả dữ liệu trong cơ sở dữ liệu 'bleu' đã được xóa sạch thành công!")

    except mysql.connector.Error as err:
        print(f"❌ Lỗi MySQL: {err}")

    finally:
        # ✅ Bật lại kiểm tra khóa ngoại dù có lỗi
        if conn and conn.is_connected():
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                conn.commit()
            except:
                pass
            cursor.close()
            conn.close()
            print("\n🔒 Đã bật lại kiểm tra khóa ngoại và đóng kết nối MySQL.")

if __name__ == "__main__":
    clear_database()
