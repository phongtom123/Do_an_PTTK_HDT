# model/listening.py
from model.question import Question

class Listening(Question):
    """Lớp mô tả câu hỏi Listening kế thừa từ Question."""

    def __init__(self, listening_question_id=None, listening_content=None,
                 listening_audio=None, **kwargs):
        super().__init__(**kwargs)
        self._listening_question_id = listening_question_id
        self._listening_content = listening_content
        self._listening_audio = listening_audio

    # --- Getter / Setter ---
    def get_listening_question_id(self): return self._listening_question_id
    def set_listening_question_id(self, qid): self._listening_question_id = qid

    def get_listening_content(self): return self._listening_content
    def set_listening_content(self, content): self._listening_content = content

    def get_listening_audio(self): return self._listening_audio
    def set_listening_audio(self, audio): self._listening_audio = audio

    def __repr__(self):
        return (f"Listening(ID={self._listening_question_id}, Content='{self._listening_content}', "
                f"Audio='{self._listening_audio}', Base={super().__repr__()})")
