from db.db import db
from logic.unit.Unit import Unit

class UnitManager:
    def __init__(self, user_id=None):
        self.__my_db = db()
        self.unit_list = []
        self.fetch_db()

    def fetch_db(self):
        """Lấy toàn bộ unit từ DB"""
        query = "SELECT * FROM units"

        try:
            df = self.__my_db.query(query)
        except Exception as e:
            print("Lỗi load Unit:", e)
            return

        self.unit_list.clear()
        for _, row in df.iterrows():
            unit = Unit(
                unit_id=row["unit_id"],
                unit_name=row["unit_name"]
            )
            self.unit_list.append(unit)

    def get_all(self):
        return self.unit_list
    
    def get_by_id(self, unit_id):
        for unit in self.unit_list:
            if unit.get_unit_id() == unit_id:
                return unit
        return None
