import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

class db:
    def __init__(self):
        load_dotenv()
        self.host = os.environ["MYSQL_HOST"]
        self.user =os.environ["MYSQL_USERNAME"]
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
                print("Kết nối thành công!!!")
        except mysql.connector.Error as err:
                print(f"Có lỗi xảy ra. Thông tin lỗi: {err}")

    def query(self, query: str) -> pd.DataFrame:
         '''Đọc toàn bộ kết quả và trả về 1 dataframe'''
         df = pd.read_sqL(query, self.connect)
         return pd.DataFrame(df)
    
    def dml_ddl_operator(self,query: str):
         '''Dùng để thao tác thêm, sửa, xóa với db'''
         cursor = self.connect.cursor()
         cursor.execute(query)
    
    def close(self):
         self.connect.close()
        

if __name__ == "__main__":
    my_db = db()
    my_db.close()
