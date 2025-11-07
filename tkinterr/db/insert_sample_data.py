import mysql.connector
import random
from datetime import date

def insert_random_data():
    try:
        # 🔗 Kết nối tới MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # nếu có mật khẩu thì điền vào đây
            database="bleu"
        )
        cursor = conn.cursor()
        print("✅ Kết nối thành công tới cơ sở dữ liệu 'bleu'.\n")

        # ======================================================
        # 🧹 XÓA DỮ LIỆU CŨ (nếu cần chạy lại)
        # ======================================================
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        tables = ["UserAnswer", "FVocab", "FlashCard", "Learn", "Question", "Listening", "Reading", "Lesson", "Vocab", "Unit", "USER"]
        for t in tables:
            cursor.execute(f"TRUNCATE TABLE {t};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("🧹 Đã xóa dữ liệu cũ trong toàn bộ bảng.\n")

        # ==== NHẬP SỐ LƯỢNG NGẪU NHIÊN ====
        num_users = int(input("👤 Số lượng người dùng cần thêm: "))
        num_units = int(input("📘 Số lượng Unit cần thêm: "))
        num_vocab = int(input("🔤 Số lượng từ vựng cần thêm: "))
        num_questions = int(input("❓ Số lượng câu hỏi cần thêm: "))

        # ======================================================
        # 1️⃣ UNIT
        # ======================================================
        units = [(f"Unit {i+1}",) for i in range(num_units)]
        cursor.executemany("INSERT INTO Unit (unitName) VALUES (%s);", units)
        conn.commit()
        cursor.execute("SELECT unit_ID FROM Unit;")
        unit_ids = [u[0] for u in cursor.fetchall()]
        print(f"✅ Đã thêm {num_units} Unit.")

        # ======================================================
        # 2️⃣ USER
        # ======================================================
        users = []
        for i in range(num_users):
            users.append((
                date.today(),
                f"User {i+1}",
                f"user{i+1}@gmail.com",
                f"user{i+1}",
                "123456",
                random.randint(1, 5),
                round(random.uniform(0, 100), 2),
                random.choice([True, False])
            ))
        cursor.executemany("""
            INSERT INTO USER (createDate, name, email, account, password, level, progress, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, users)
        conn.commit()
        cursor.execute("SELECT user_ID FROM USER;")
        user_ids = [u[0] for u in cursor.fetchall()]
        print(f"✅ Đã thêm {num_users} người dùng.")

        # ======================================================
        # 3️⃣ VOCAB
        # ======================================================
        vocab = [(f"word{i+1}", f"nghĩa {i+1}", random.choice(["Easy", "Medium", "Hard"])) for i in range(num_vocab)]
        cursor.executemany("INSERT INTO Vocab (word, meaning, difficulty) VALUES (%s, %s, %s);", vocab)
        conn.commit()
        cursor.execute("SELECT word_ID FROM Vocab;")
        word_ids = [w[0] for w in cursor.fetchall()]
        print(f"✅ Đã thêm {num_vocab} từ vựng.")

        # ======================================================
        # 4️⃣ LESSON (mỗi Unit có ít nhất 1 Lesson)
        # ======================================================
        lessons = [(uid, f"Lesson của Unit {uid}") for uid in unit_ids]
        cursor.executemany("INSERT INTO Lesson (unit_ID, lessonName) VALUES (%s, %s);", lessons)
        conn.commit()
        cursor.execute("SELECT lesson_ID FROM Lesson;")
        lesson_ids = [l[0] for l in cursor.fetchall()]
        print(f"✅ Đã thêm {len(lesson_ids)} Lesson.")

        # ======================================================
        # 5️⃣ READING & LISTENING (mỗi Lesson chỉ 1 loại)
        # ======================================================
        readings = []
        listenings = []

        for lid in lesson_ids:
            if random.random() < 0.6:  # 60% là Reading
                readings.append((lid, f"Nội dung đọc cho Lesson {lid}"))
            else:  # 40% là Listening
                listenings.append((lid, f"https://audio.fake/lesson{lid}.mp3"))

        if readings:
            cursor.executemany("INSERT INTO Reading (lesson_ID, readContent) VALUES (%s, %s);", readings)
        if listenings:
            cursor.executemany("INSERT INTO Listening (lesson_ID, linkAudio) VALUES (%s, %s);", listenings)
        conn.commit()
        print(f"✅ Đã thêm {len(readings)} Reading và {len(listenings)} Listening.")

        # ======================================================
        # 6️⃣ QUESTION (thuộc về Lesson)
        # ======================================================
        questions = []
        for i in range(num_questions):
            lesson_id = random.choice(lesson_ids)
            questions.append((
                lesson_id,
                f"Nội dung câu hỏi {i+1}",
                f"Option A-{i+1}",
                f"Option B-{i+1}",
                f"Option C-{i+1}",
                f"Option D-{i+1}",
                f"Giải thích câu hỏi {i+1}",
                f"Đáp án đúng là Option {random.choice(['A', 'B', 'C', 'D'])}"
            ))
        cursor.executemany("""
            INSERT INTO Question (lesson_ID, content, option1, option2, option3, option4, explanation, result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, questions)
        conn.commit()
        cursor.execute("SELECT question_ID FROM Question;")
        question_ids = [q[0] for q in cursor.fetchall()]
        print(f"✅ Đã thêm {num_questions} câu hỏi.")

        # ======================================================
        # 7️⃣ LEARN (N–N USER–LESSON)
        # ======================================================
        learn_records = []
        seen = set()
        for uid in user_ids:
            for _ in range(random.randint(1, 3)):
                lid = random.choice(lesson_ids)
                if (uid, lid) not in seen:
                    learn_records.append((uid, lid, random.choice([True, False]), round(random.uniform(0, 100), 2), random.randint(30, 180)))
                    seen.add((uid, lid))
        cursor.executemany("""
            INSERT INTO Learn (user_ID, lesson_ID, is_pass, progress, finishTime)
            VALUES (%s, %s, %s, %s, %s);
        """, learn_records)
        conn.commit()
        print(f"✅ Đã thêm {len(learn_records)} bản ghi Learn.")

        # ======================================================
        # 8️⃣ FLASHCARD (mỗi user học vài từ)
        # ======================================================
        flashcards = [(uid,) for uid in user_ids for _ in range(random.randint(1, 3))]
        cursor.executemany("INSERT INTO FlashCard (user_ID) VALUES (%s);", flashcards)
        conn.commit()
        cursor.execute("SELECT flashcard_ID FROM FlashCard;")
        flashcard_ids = [f[0] for f in cursor.fetchall()]
        print(f"✅ Đã thêm {len(flashcard_ids)} FlashCard.")

        # ======================================================
        # 9️⃣ FVocab (liên kết flashcard–vocab)
        # ======================================================
        fcvocab = [(fc, random.choice(word_ids), f"Từ đồng nghĩa của word {random.choice(word_ids)}") for fc in flashcard_ids]
        cursor.executemany("INSERT INTO FVocab (flashcard_ID, word_ID, synonym) VALUES (%s, %s, %s);", fcvocab)
        conn.commit()
        print(f"✅ Đã thêm {len(fcvocab)} bản ghi FVocab.")

        # ======================================================
        # 🔟 USERANSWER (user – question)
        # ======================================================
        answers = []
        for uid in user_ids:
            qid = random.choice(question_ids)
            answers.append((qid, uid, f"Câu trả lời của user {uid} cho câu {qid}", random.choice([True, False])))
        cursor.executemany("""
            INSERT INTO UserAnswer (question_ID, user_ID, content, isCorrect)
            VALUES (%s, %s, %s, %s);
        """, answers)
        conn.commit()
        print(f"✅ Đã thêm {len(answers)} UserAnswer.")

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
