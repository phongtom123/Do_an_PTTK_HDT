class Lesson:
    def __init__(self, lesson_id, lesson_unit_id, lesson_name, test_id):
        self._lesson_id = lesson_id
        self._lesson_unit_id = lesson_unit_id
        self._lesson_name = lesson_name
        self._test_id = test_id

    def get_test_id(self):
        return self._test_id

    def get_lesson_id(self):
        return self._lesson_id

    def get_unit_id(self):
        return self._lesson_unit_id

    def get_lesson_name(self):
        return self._lesson_name

    def set_lesson_name(self, name):
        self._lesson_name = name

    def __repr__(self):
        return f"Lesson(id={self._lesson_id}, unit_id={self._lesson_unit_id}, name='{self._lesson_name}')"
