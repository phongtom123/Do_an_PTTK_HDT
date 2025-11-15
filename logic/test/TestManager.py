from db.db import db

class TestManager:
    def __init__(self):
        self.db = db()

    def get_test_id_by_lesson(self, lesson_id):
        df = self.db.query(
            "SELECT test_id FROM tests WHERE test_lesson_id = %s",
            (int(lesson_id),)
        )

        if df.empty:
            return None

        return int(df.iloc[0]["test_id"])

