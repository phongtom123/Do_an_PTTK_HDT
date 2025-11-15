class Word:
    def __init__(self, word_id, word, word_meaning, word_status, word_difficulty, word_unit_id):
        self._word_id = word_id
        self._word = word
        self._word_meaning = word_meaning
        self._word_status = word_status
        self._word_difficulty = word_difficulty
        self._word_unit_id = word_unit_id

    # ===== GETTERS =====
    def get_word_id(self):
        return self._word_id

    def get_word(self):
        return self._word

    def get_word_meaning(self):
        return self._word_meaning

    def get_word_status(self):
        return self._word_status

    def get_word_difficulty(self):
        return self._word_difficulty

    def get_unit_id(self):
        return self._word_unit_id

    # ===== SETTERS =====
    def set_word(self, word):
        self._word = word

    def set_word_meaning(self, meaning):
        self._word_meaning = meaning

    def set_word_status(self, status):
        self._word_status = status

    def set_word_difficulty(self, diff):
        self._word_difficulty = diff

    # DEBUG
    def __repr__(self):
        return (f"Word(id={self._word_id}, word='{self._word}', meaning='{self._word_meaning}', "
                f"status='{self._word_status}', diff='{self._word_difficulty}', unit={self._word_unit_id})")
