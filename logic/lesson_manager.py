class FakeLesson:
    def __init__(self, id, name):
        self.lesson_id = id
        self.lesson_name = name


class LessonManager:
    def get_by_unit_id(self, unit_id):
        # Tạo dữ liệu giả
        return [
            FakeLesson(1, "Reading Practice"),
            FakeLesson(2, "Listening Practice")
        ]
