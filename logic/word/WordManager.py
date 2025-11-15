from db.db import db
from logic.word.Word import Word


class WordManager:
    def __init__(self):
        self.db = db()
        self.word_list = []
        self.fetch_db()

    # ==============================
    # LOAD ALL WORDS FROM DB
    # ==============================
    def fetch_db(self):
        df = self.db.query("SELECT * FROM words")
        self.word_list.clear()

        for _, row in df.iterrows():
            w = Word(
                word_id=row["word_id"],
                word=row["word"],
                word_meaning=row["word_meaning"],
                word_status=row["word_status"],
                word_difficulty=row["word_difficulty"],
                word_unit_id=row["word_unit_id"]
            )
            self.word_list.append(w)

    # ==============================
    # GET WORDS BY UNIT
    # ==============================
    def get_by_unit_id(self, unit_id):
        return [w for w in self.word_list if w.get_unit_id() == unit_id]

    # ==============================
    # FIND WORD BY ID
    # ==============================
    def find_word(self, word_id):
        for w in self.word_list:
            if w.get_word_id() == word_id:
                return w
        return None

    # ==============================
    # ADD NEW WORD
    # ==============================
    def add_word(self, word: Word):
        query = """
            INSERT INTO words (word, word_meaning, word_status, word_difficulty, word_unit_id)
            VALUES (%s, %s, %s, %s, %s)
        """

        return self.db.dml_ddl_operator(query, (
            word.get_word(),
            word.get_word_meaning(),
            word.get_word_status(),
            word.get_word_difficulty(),
            word.get_unit_id()
        ))

    # ==============================
    # DEBUG
    # ==============================
    def __repr__(self):
        return f"WordManager(total_words={len(self.word_list)})"
