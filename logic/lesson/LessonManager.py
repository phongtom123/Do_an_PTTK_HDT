from db.db import db
from logic.lesson.Lesson import Lesson


class LessonManager:
    def __init__(self):
        self.__my_db = db()
        self.lesson_list = []
        self.fetch_db()

    def fetch_db(self):
        """Lấy tất cả lesson trong DB"""
        query = "SELECT * FROM lessons"

        try:
            df = self.__my_db.query(query)
        except Exception as e:
            print("Lỗi load Lesson:", e)
            return

        self.lesson_list.clear()

        for _, row in df.iterrows():
            lesson = Lesson(
                lesson_id=row["lesson_id"],
                lesson_unit_id=row["lesson_unit_id"],
                lesson_name=row["lesson_name"],
                test_id=row["test_id"]     # LẤY TỪ DB
            )
            self.lesson_list.append(lesson)

    def get_all(self):
        return self.lesson_list

    def get_by_unit_id(self, unit_id):
        return [ls for ls in self.lesson_list if ls.get_unit_id() == unit_id]

    def get_by_id(self, lesson_id):
        for ls in self.lesson_list:
            if ls.get_lesson_id() == lesson_id:
                return ls
        return None
