# model/question.py
class Question:
    """Lớp mô tả câu hỏi trong hệ thống BLEU."""

    def __init__(self, question_id=None, question_lesson_id=None, question_unit_id=None,
                 question_content=None, question_answer=None, question_type=None):
        self._question_id = question_id
        self._question_lesson_id = question_lesson_id
        self._question_unit_id = question_unit_id
        self._question_content = question_content
        self._question_answer = question_answer
        self._question_type = question_type

    # --- Getter / Setter ---
    def get_question_id(self): return self._question_id
    def set_question_id(self, question_id): self._question_id = question_id

    def get_question_lesson_id(self): return self._question_lesson_id
    def set_question_lesson_id(self, lesson_id): self._question_lesson_id = lesson_id

    def get_question_unit_id(self): return self._question_unit_id
    def set_question_unit_id(self, unit_id): self._question_unit_id = unit_id

    def get_question_content(self): return self._question_content
    def set_question_content(self, content): self._question_content = content

    def get_question_answer(self): return self._question_answer
    def set_question_answer(self, answer): self._question_answer = answer

    def get_question_type(self): return self._question_type
    def set_question_type(self, qtype): self._question_type = qtype

    def __repr__(self):
        return (f"Question(ID={self._question_id}, Lesson={self._question_lesson_id}, "
                f"Unit={self._question_unit_id}, Type='{self._question_type}', "
                f"Content='{self._question_content}', Answer='{self._question_answer}')")
