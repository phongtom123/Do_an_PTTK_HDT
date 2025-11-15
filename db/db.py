import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

class db:
    def __init__(self):
        load_dotenv()
        self.host = os.environ["MYSQL_HOST"]
        self.user = os.environ["MYSQL_USERNAME"]
        self.password = os.environ["MYSQL_PASSWORD"]
        self.database_name = os.environ["MYSQL_DATABASE_NAME"]
        self.port = os.environ["MYSQL_PORT"]
        
        config = {
            'host': self.host,
            'user': self.user, 
            'password': self.password,
            'database': self.database_name,
            'port': self.port,
        }
        self.connect = None
        try:
            self.connect = mysql.connector.connect(**config)
            if self.connect.is_connected():
                print("✅ Kết nối thành công!!!")
        except mysql.connector.Error as err:
            print(f"❌ Có lỗi xảy ra khi kết nối MySQL: {err}")

    # # =====================================================
    # # DQL (SELECT) — cho code cũ, trả về list tuple
    # # =====================================================
    # def dql_operator(self, query: str, params: tuple = None):
    #     """Dùng cho SELECT — trả về list tuple (phù hợp với các controller cũ)."""
    #     try:
    #         cursor = self.connect.cursor()
    #         cursor.execute(query, params)
    #         rows = cursor.fetchall()
    #         cursor.close()
    #         return rows
    #     except Exception as e:
    #         print(f"❌ Lỗi DQL: {e}")
    #         return []


    def query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Đọc toàn bộ kết quả và trả về 1 DataFrame."""
        try:
            df = pd.read_sql(query, self.connect, params=params)
            return pd.DataFrame(df)
        except Exception as e:
            print(f"Lỗi khi thực hiện query(): {e}")
            return pd.DataFrame()


    def dml_ddl_operator(self, query: str, params: tuple = None) -> bool:
        """Thao tác thêm/sửa/xóa. Trả về True nếu thành công."""
        try:
            cursor = self.connect.cursor()
            cursor.execute(query, params)
            self.connect.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id

        except Exception as e:
            print(f"Loi khi thuc hien dml_ddl: {e}")
            return False
        
    def close(self):
        """Đóng kết nối CSDL."""
        try:
            if self.connect:
                self.connect.close()
                print("🔒 Đã đóng kết nối MySQL.")
        except Exception as e:
            print(f"⚠️ Lỗi khi đóng kết nối: {e}")


if __name__ == "__main__":
    my_db = db()
    print(my_db.query("SELECT * FROM Users"))
    my_db.close()
