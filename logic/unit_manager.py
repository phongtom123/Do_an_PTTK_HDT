# # controller/unit_controller.py
# import mysql.connector

# def connect_db():
#     """Kết nối tới MySQL — chỉnh thông tin nếu cần."""
#     return mysql.connector.connect(
#         host="localhost",
#         port=3306,
#         user="root",
#         password="",   # nếu bạn có mật khẩu thì thêm vào đây
#         database="bleu"
#     )

# def get_all_units():
#     """
#     Lấy danh sách tất cả Units trong database 'bleu'.
#     Trả về danh sách tuple (unit_id, unit_name)
#     """
#     try:
#         conn = connect_db()
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT unit_id, unit_name
#             FROM Units
#             ORDER BY unit_id;
#         """)
#         rows = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         return rows

#     except mysql.connector.Error as e:
#         print("❌ Lỗi lấy Units:", e)
#         return []
#     except Exception as e:
#         print("❌ Lỗi không xác định khi lấy Units:", e)
#         return []

from db.db import db
import pandas as pd
from .unit_model import Unit

class UnitManager():
    def __init__(self):
        self.__my_db = db()
        self.df = None
        self.get_unit_list()
        self.unit_list = []
        self.append_unit()

    def get_unit_list(self):
        '''Cập nhật thông tin unit từ db'''
        query = 'SELECT unit_id, unit_name FROM `units`'
        self.df = self.__my_db.query(query)
    
    def update_unit_list(self):
        '''Cập lại danh sách unit'''
        self.get_unit_list()
        self.unit_list.clear()
        self.append_unit()

    def append_unit(self):
        '''Lưu unit vào list'''
        for _,row in self.df.iterrows():
            my_unit = Unit(row["unit_id"], row["unit_name"])
            self.unit_list.append(my_unit)

if __name__ == "__main__":
    unit_manager = UnitManager()
    for unit in unit_manager.unit_list:
        print(unit)