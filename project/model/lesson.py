# model/lesson.py

class Lesson:
    """Lớp mô tả một Lesson (bài học nhỏ) trong hệ thống BLEU."""

    def __init__(self, lesson_id=None, lesson_name=None, lesson_unit_id=None):
        self._lesson_id = lesson_id
        self._lesson_name = lesson_name
        self._lesson_unit_id = lesson_unit_id

    def get_lesson_id(self):
        return self._lesson_id

    def set_lesson_id(self, lesson_id):
        self._lesson_id = lesson_id

    def get_lesson_name(self):
        return self._lesson_name

    def set_lesson_name(self, name):
        self._lesson_name = name

    def get_lesson_unit_id(self):
        return self._lesson_unit_id

    def set_lesson_unit_id(self, unit_id):
        self._lesson_unit_id = unit_id

    def __repr__(self):
        return f"Lesson(ID={self._lesson_id}, Name='{self._lesson_name}', UnitID={self._lesson_unit_id})"
