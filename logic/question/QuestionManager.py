import json
from db.db import db
from logic.question.Question import Question

class QuestionManager:
    def __init__(self):
        self.db = db()
        self.question_list = []
        self.fetch_db()

    # =============================
    # LOAD TẤT CẢ QUESTION TỪ DB
    # =============================
    def fetch_db(self):
        df = self.db.query("SELECT * FROM questions")
        self.question_list.clear()

        for _, row in df.iterrows():

            # Load JSON options
            options = []
            if row["question_options"] not in (None, "", "NULL"):
                try:
                    options = json.loads(row["question_options"])
                except:
                    options = []

            q = Question(
                question_id=row["question_id"],
                question_content=row["question_content"],
                question_answer=row["question_answer"],
                question_test_id=row["question_test_id"],
                question_options=options
            )
            self.question_list.append(q)

    # =============================
    # LẤY QUESTION THEO test_id
    # =============================
    def get_by_test_id(self, test_id):

        if test_id is None:
            return []

        df = self.db.query(
            "SELECT * FROM questions WHERE question_test_id = %s",
            (int(test_id),)
        )

        result = []
        for _, row in df.iterrows():

            # Load JSON options
            options = []
            if row["question_options"] not in (None, "", "NULL"):
                try:
                    options = json.loads(row["question_options"])
                except:
                    options = []

            q = Question(
                question_id=row["question_id"],
                question_content=row["question_content"],
                question_answer=row["question_answer"],
                question_test_id=row["question_test_id"],
                question_options=options
            )

            result.append(q)

        return result

    # =============================
    # THÊM QUESTION MỚI
    # =============================
    def add_question(self, question):
        query = """
            INSERT INTO questions
            (question_content, question_answer, question_test_id, question_options)
            VALUES (%s, %s, %s, %s)
        """

        # Convert list(dict) → JSON string
        options_json = json.dumps(question.get_question_opt())

        return self.db.dml_ddl_operator(query, (
            question.get_question_content(),
            question.get_question_answer(),
            question.get_test_id(),
            options_json
        ))
    
        # =============================
    # TRẢ VỀ ĐÁP ÁN ĐÚNG CỦA QUESTION
    # =============================
    def get_correct_answer(self, question_id):
        for q in self.question_list:
            if q.get_question_id() == question_id:
                return q.get_question_answer()
        return None

    # =============================
    # KIỂM TRA ĐÚNG / SAI
    # =============================
    def check_answer(self, question_id, user_choice):
        correct = self.get_correct_answer(question_id)
        return user_choice == correct

    # =============================
    # TÍNH ĐIỂM BÀI TRẮC NGHIỆM
    # user_answers = {question_id: "A", ...}
    # =============================
    def score(self, test_id, user_answers):
        questions = self.get_by_test_id(test_id)
        total = len(questions)
        correct = 0

        for q in questions:
            qid = q.get_question_id()
            if qid in user_answers:
                if user_answers[qid] == q.get_question_answer():
                    correct += 1

        return correct, total

