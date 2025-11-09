# Để query cần đảm bao 2 yếu tố query và params tách biệt nhay và được liên kết bởi trình giữ chỗ.
# Ex: query = "insert into tbl(col1, col2) values (%s, %s)"
#     params = ("val1", "val2")
#     => pd.ddl_dml_operator(query, params)


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

    def query(self, query: str, params: tuple = None) -> pd.DataFrame:
         '''Đọc toàn bộ kết quả và trả về 1 dataframe'''
         df = pd.read_sql(query, self.connect, params=params)
         return pd.DataFrame(df)
    
    def dml_ddl_operator(self, query: str, params: tuple = None) -> None:
        '''Dùng để thao tác thêm, sửa, xóa với db, Trả về 1 nếu query thành công và 0 nếu query không thành công'''
        cursor = self.connect.cursor()
        try:
            cursor.execute(query, params)
            self.connect.commit()   
            return True
        except Exception as e:
            print(f"Lỗi: {e}")
            return False
        
    def close(self):
         self.connect.close()
        

if __name__ == "__main__":
    my_db = db()
    my_db.close()
