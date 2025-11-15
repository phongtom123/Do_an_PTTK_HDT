class Question:
    def __init__(self, question_id, question_content, question_answer, question_test_id, question_options=None):
        self._question_id = question_id
        self._question_content = question_content
        self._question_answer = question_answer
        self._question_test_id = question_test_id
        self._question_options = question_options or []   # list of dict

    def get_question_id(self):
        return self._question_id

    def get_question_content(self):
        return self._question_content

    def get_question_answer(self):
        return self._question_answer

    def get_question_opt(self):
        return self._question_options

    def get_test_id(self):
        return self._question_test_id
