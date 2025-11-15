from db.db import db
from logic.reading.reading import Reading

class ReadingManager:
    def __init__(self):
        self.db = db()

    def get_by_test_id(self, test_id):
        """Lấy Reading dựa trên test_id. test_id có thể là numpy.int64 hoặc str; convert an toàn."""
        if test_id is None:
            return []

        try:
            tid = int(test_id)
        except Exception:
            # nếu không convert được, trả về rỗng để tránh crash
            return []

        df = self.db.query(
            "SELECT reading_test_id, reading_content FROM readings WHERE reading_test_id = %s",
            (tid,)
        )

        result = []
        for _, row in df.iterrows():
            result.append(
                Reading(
                    reading_id=row["reading_test_id"],
                    reading_content=row["reading_content"]
                )
            )

        return result
