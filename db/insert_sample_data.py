import mysql.connector
import random
from datetime import date

def insert_random_data():
    try:
        # 🔗 Kết nối tới MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # nếu có mật khẩu thì điền vào đây
            database="bleu"
        )
        cursor = conn.cursor()

        print("✅ Kết nối thành công tới cơ sở dữ liệu 'bleu'.\n")

        # ==== NHẬP SỐ LƯỢNG NGẪU NHIÊN ====
        num_users = int(input("👤 Số lượng người dùng cần thêm: "))
        num_units = int(input("📘 Số lượng Unit cần thêm: "))
        num_vocab = int(input("🔤 Số lượng từ vựng cần thêm: "))
        num_questions = int(input("❓ Số lượng câu hỏi cần thêm: "))

        # ======================================================
        # 1️⃣ UNIT
        # ======================================================
        units = [(f"Unit {i+1}: Lesson {i+1}",) for i in range(num_units)]
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
                f"Đang học Unit {random.choice(unit_ids)}",
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
        vocab = []
        for i in range(num_vocab):
            vocab.append((
                f"word{i+1}",
                f"nghĩa {i+1}",
                random.choice(["easy", "medium", "hard"])
            ))

        cursor.executemany("""
            INSERT INTO Vocab (word, meaning, difficulty)
            VALUES (%s, %s, %s);
        """, vocab)
        conn.commit()
        cursor.execute("SELECT word_ID FROM Vocab;")
        word_ids = [w[0] for w in cursor.fetchall()]
        print(f"✅ Đã thêm {num_vocab} từ vựng.")

        # ======================================================
        # 4️⃣ LESSON (mỗi Unit có ít nhất 1 Lesson)
        # ======================================================
        lessons = []
        for i, uid in enumerate(unit_ids):
            lessons.append((uid, f"Lesson của Unit {uid}",))
        cursor.executemany("INSERT INTO Lesson (unit_ID, lessonName) VALUES (%s, %s);", lessons)
        conn.commit()
        cursor.execute("SELECT lesson_ID FROM Lesson;")
        lesson_ids = [l[0] for l in cursor.fetchall()]
        print(f"✅ Đã thêm {len(lesson_ids)} Lesson.")

        # ======================================================
        # 5️⃣ READING & LISTENING (kế thừa từ Lesson)
        # ======================================================
        readings = [(lid, f"Nội dung đọc cho Lesson {lid}", random.choice([None, None, None])) for lid in lesson_ids]
        cursor.executemany("INSERT INTO Reading (lesson_ID, readContent, question_ID) VALUES (%s, %s, %s);", readings)

        listenings = [(lid, f"https://audio.fake/unit{lid}.mp3", random.choice([None, None, None])) for lid in lesson_ids]
        cursor.executemany("INSERT INTO Listening (lesson_ID, linkAudio, question_ID) VALUES (%s, %s, %s);", listenings)
        conn.commit()
        print(f"✅ Đã thêm {len(readings)} Reading và {len(listenings)} Listening.")

        # ======================================================
        # 6️⃣ QUESTION
        # ======================================================
        questions = []
        for i in range(num_questions):
            unit_id = random.choice(unit_ids)
            questions.append((
                f"Nội dung câu hỏi {i+1}",
                unit_id,
                f"Giải thích cho câu hỏi {i+1}",
                f"Kết quả {i+1}"
            ))
        cursor.executemany("""
            INSERT INTO Question (content, unit_ID, explanation, result)
            VALUES (%s, %s, %s, %s);
        """, questions)
        conn.commit()
        cursor.execute("SELECT question_ID FROM Question;")
        question_ids = [q[0] for q in cursor.fetchall()]
        print(f"✅ Đã thêm {num_questions} câu hỏi.")

        # ======================================================
        # 7️⃣ LEARN (N–N USER–UNIT)
        # ======================================================
        learn_records = []
        seen = set()
        for uid in user_ids:
            unit_id = random.choice(unit_ids)
            if (uid, unit_id) not in seen:
                learn_records.append((unit_id, uid, random.choice([True, False]), random.randint(30, 180)))
                seen.add((uid, unit_id))
        cursor.executemany("""
            INSERT INTO Learn (unit_ID, user_ID, is_pass, finishTime)
            VALUES (%s, %s, %s, %s);
        """, learn_records)
        conn.commit()
        print(f"✅ Đã thêm {len(learn_records)} bản ghi Learn.")

        # ======================================================
        # 8️⃣ FLASHCARD (mỗi user học 3 từ)
        # ======================================================
        flashcards = []
        seen_flash = set()
        for uid in user_ids:
            sampled_words = random.sample(word_ids, min(3, len(word_ids)))
            for wid in sampled_words:
                if (uid, wid) not in seen_flash:
                    flashcards.append((wid, uid))
                    seen_flash.add((uid, wid))
        cursor.executemany("""
            INSERT INTO FlashCard (word_ID, user_ID)
            VALUES (%s, %s);
        """, flashcards)
        conn.commit()
        cursor.execute("SELECT flashcard_ID FROM FlashCard;")
        flashcard_ids = [f[0] for f in cursor.fetchall()]
        print(f"✅ Đã thêm {len(flashcards)} FlashCard.")

        # ======================================================
        # 9️⃣ USERFC (liên kết user–flashcard)
        # ======================================================
        userfc = []
        for fc in flashcard_ids:
            uid = random.choice(user_ids)
            userfc.append((fc, uid))
        cursor.executemany("INSERT INTO UserFC (flashcard_ID, user_ID) VALUES (%s, %s);", userfc)
        conn.commit()
        print(f"✅ Đã thêm {len(userfc)} bản ghi UserFC.")

        # ======================================================
        # 🔟 FCVOCAB (liên kết flashcard–vocab)
        # ======================================================
        fcvocab = []
        for fc in flashcard_ids:
            wid = random.choice(word_ids)
            fcvocab.append((fc, wid, f"Từ đồng nghĩa của word {wid}"))
        cursor.executemany("""
            INSERT INTO FCVocab (flashcard_ID, word_ID, synonym)
            VALUES (%s, %s, %s);
        """, fcvocab)
        conn.commit()
        print(f"✅ Đã thêm {len(fcvocab)} bản ghi FCVocab.")

        # ======================================================
        # 1️⃣1️⃣ USERANSWER
        # ======================================================
        answers = []
        for uid in user_ids:
            qid = random.choice(question_ids)
            unit_id = random.choice(unit_ids)
            if random.random() < 0.5:
                content = None
                result = None
            else:
                content = f"Câu trả lời của user {uid} cho câu {qid}"
                result = random.choice([True, False])
            answers.append((qid, uid, unit_id, content, result))
        cursor.executemany("""
            INSERT INTO UserAnswer (question_ID, user_ID, unit_ID, content, result)
            VALUES (%s, %s, %s, %s, %s);
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
