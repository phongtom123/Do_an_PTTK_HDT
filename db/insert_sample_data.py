import mysql.connector
import random
from datetime import datetime

def insert_random_data():
    try:
        # 🔗 Kết nối tới MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # nếu có mật khẩu MySQL, điền vào đây
            database="bleu"
        )
        cursor = conn.cursor()
        print("✅ Kết nối thành công tới cơ sở dữ liệu 'bleu'.\n")

        # ======================================================
        # 🧹 XÓA DỮ LIỆU CŨ
        # ======================================================
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        tables = [
            "Answers", "Games", "Learnings", "Words",
            "Listenings", "Readings", "Question_options",
            "Questions", "Lessons", "Units", "Users", "Roles"
        ]
        for t in tables:
            cursor.execute(f"TRUNCATE TABLE {t};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("🧹 Đã xóa toàn bộ dữ liệu cũ.\n")

        # ======================================================
        # NHẬP SỐ LƯỢNG NGẪU NHIÊN
        # ======================================================
        num_users = int(input("👤 Số lượng người dùng cần thêm: "))
        num_units = int(input("📘 Số lượng Unit cần thêm: "))
        num_lessons = int(input("📗 Số lượng Lesson cần thêm: "))
        num_questions = int(input("❓ Số lượng câu hỏi cần thêm: "))
        num_words = int(input("🔤 Số lượng từ vựng cần thêm: "))

        # ======================================================
        # 1️⃣ ROLES
        # ======================================================
        role_names = [("Admin",), ("Teacher",), ("Student",)]
        cursor.executemany("INSERT INTO Roles (role_name) VALUES (%s)", role_names)
        conn.commit()
        cursor.execute("SELECT role_id FROM Roles;")
        role_ids = [r[0] for r in cursor.fetchall()]
        print(f"✅ Đã thêm {len(role_ids)} Roles.")

        # ======================================================
        # 2️⃣ USERS
        # ======================================================
        users = []
        for i in range(num_users):
            users.append((
                f"user{i+1}",
                f"pass{i+1}",
                random.choice(role_ids),
                random.randint(1, 10),
                random.randint(1, 20),
                random.choice([0, 1])
            ))
        cursor.executemany("""
            INSERT INTO Users (user_name, user_password, user_role_id, user_rank, user_level, user_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, users)
        conn.commit()
        cursor.execute("SELECT user_id FROM Users;")
        user_ids = [u[0] for u in cursor.fetchall()]
        print(f"✅ Đã thêm {len(user_ids)} Users.")

        # ======================================================
        # 3️⃣ UNITS
        # ======================================================
        units = [(f"Unit {i+1}",) for i in range(num_units)]
        cursor.executemany("INSERT INTO Units (unit_name) VALUES (%s)", units)
        conn.commit()
        cursor.execute("SELECT unit_id FROM Units;")
        unit_ids = [u[0] for u in cursor.fetchall()]
        print(f"✅ Đã thêm {len(unit_ids)} Units.")

        # ======================================================
        # 4️⃣ LESSONS
        # ======================================================
        lessons = []
        for i in range(num_lessons):
            unit_id = random.choice(unit_ids)
            lessons.append((unit_id, f"Lesson {i+1} của Unit {unit_id}"))
        cursor.executemany("INSERT INTO Lessons (lesson_unit_id, lesson_name) VALUES (%s, %s)", lessons)
        conn.commit()
        cursor.execute("SELECT lesson_id FROM Lessons;")
        lesson_ids = [l[0] for l in cursor.fetchall()]
        print(f"✅ Đã thêm {len(lesson_ids)} Lessons.")

        # ======================================================
        # 5️⃣ QUESTIONS
        # ======================================================
        questions = []
        for i in range(num_questions):
            lesson_id = random.choice(lesson_ids)
            unit_id = random.choice(unit_ids)
            questions.append((
                lesson_id,
                unit_id,
                f"Nội dung câu hỏi {i+1}",
                f"Đáp án đúng {random.choice(['A','B','C','D'])}",
                random.choice(["Trắc nghiệm", "Đọc hiểu", "Nghe"])
            ))
        cursor.executemany("""
            INSERT INTO Questions (question_lesson_id, question_unit_id, question_content, question_answer, question_type)
            VALUES (%s, %s, %s, %s, %s)
        """, questions)
        conn.commit()
        cursor.execute("SELECT question_id FROM Questions;")
        question_ids = [q[0] for q in cursor.fetchall()]
        print(f"✅ Đã thêm {len(question_ids)} Questions.")

        # ======================================================
        # 6️⃣ QUESTION OPTIONS
        # ======================================================
        options = []
        for qid in question_ids:
            options.append((
                qid,
                f"Lựa chọn A cho câu {qid}",
                f"Lựa chọn B cho câu {qid}",
                f"Lựa chọn C cho câu {qid}",
                f"Lựa chọn D cho câu {qid}"
            ))
        cursor.executemany("""
            INSERT INTO Question_options (question_option_question_id, option_1, option_2, option_3, option_4)
            VALUES (%s, %s, %s, %s, %s)
        """, options)
        conn.commit()
        print(f"✅ Đã thêm {len(options)} Question_options.")

        # ======================================================
        # 7️⃣ READINGS & LISTENINGS (một phần mở rộng câu hỏi)
        # ======================================================
        readings = []
        listenings = []
        for qid in question_ids:
            if random.random() < 0.5:
                readings.append((qid, f"Nội dung đọc hiểu cho câu hỏi {qid}"))
            else:
                listenings.append((qid, f"Nội dung nghe cho câu hỏi {qid}", f"https://audio.fake/lesson{qid}.mp3"))

        if readings:
            cursor.executemany("INSERT INTO Readings (reading_question_id, reading_content) VALUES (%s, %s)", readings)
        if listenings:
            cursor.executemany("""
                INSERT INTO Listenings (listening_question_id, listening_content, listening_audio)
                VALUES (%s, %s, %s)
            """, listenings)
        conn.commit()
        print(f"✅ Đã thêm {len(readings)} Readings và {len(listenings)} Listenings.")

        # ======================================================
        # 8️⃣ WORDS (Flashcard)
        # ======================================================
        words = []
        for i in range(num_words):
            lesson_id = random.choice(lesson_ids)
            words.append((
                f"Word_{i+1}",
                f"Nghĩa của từ {i+1}",
                random.choice(["Đã nhớ", "Chưa nhớ"]),
                random.choice(["Easy", "Medium", "Hard"]),
                lesson_id
            ))
        cursor.executemany("""
            INSERT INTO Words (word, word_meaning, word_status, word_difficulty, word_lesson_id)
            VALUES (%s, %s, %s, %s, %s)
        """, words)
        conn.commit()
        print(f"✅ Đã thêm {len(words)} Words.")

        # ======================================================
        # 9️⃣ LEARNINGS (Lưu tiến trình học)
        # ======================================================
        learn_records = []
        for uid in user_ids:
            for _ in range(random.randint(1, 3)):
                unit_id = random.choice(unit_ids)
                learn_records.append((
                    uid,
                    unit_id,
                    datetime.now(),
                    round(random.uniform(0, 10), 2),
                    random.choice([True, False]),
                    f"{random.randint(0,100)}%",
                    datetime.now()
                ))
        cursor.executemany("""
            INSERT INTO Learnings (learning_user_id, learning_unit_id, learning_finished_time, learning_score,
                                   learning_is_pass, learning_user_progress, learning_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, learn_records)
        conn.commit()
        print(f"✅ Đã thêm {len(learn_records)} Learnings.")

        # ======================================================
        # 🔟 GAMES
        # ======================================================
        games = [(uid, random.randint(0, 20)) for uid in user_ids]
        cursor.executemany("INSERT INTO Games (game_user_id, correct_word_quantity) VALUES (%s, %s)", games)
        conn.commit()
        print(f"✅ Đã thêm {len(games)} Games.")

        # ======================================================
        # 1️⃣1️⃣ ANSWERS
        # ======================================================
        answers = []
        for uid in user_ids:
            qid = random.choice(question_ids)
            answers.append((qid, uid, f"Trả lời của user {uid} cho câu hỏi {qid}"))
        cursor.executemany("""
            INSERT INTO Answers (answer_question_id, answer_user_id, answer_user_answer)
            VALUES (%s, %s, %s)
        """, answers)
        conn.commit()
        print(f"✅ Đã thêm {len(answers)} Answers.")

        print("\n🎉 Toàn bộ dữ liệu mẫu đã được thêm thành công vào CSDL 'bleu'!")

    except mysql.connector.Error as err:
        print(f"❌ Lỗi MySQL: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔒 Đã đóng kết nối MySQL.")


if __name__ == "__main__":
    insert_random_data()
