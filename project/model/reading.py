# model/reading.py
from model.question import Question

class Reading(Question):
    """Lớp mô tả câu hỏi Reading kế thừa từ Question."""

    def __init__(self, reading_question_id=None, reading_content=None, **kwargs):
        # Kế thừa toàn bộ thuộc tính của Question
        super().__init__(**kwargs)
        self._reading_question_id = reading_question_id
        self._reading_content = reading_content

    # --- Getter / Setter ---
    def get_reading_question_id(self): return self._reading_question_id
    def set_reading_question_id(self, qid): self._reading_question_id = qid

    def get_reading_content(self): return self._reading_content
    def set_reading_content(self, content): self._reading_content = content

    def __repr__(self):
        return (f"Reading(ID={self._reading_question_id}, Content='{self._reading_content}', "
                f"Base={super().__repr__()})")
