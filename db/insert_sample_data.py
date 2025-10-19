import mysql.connector
import random
from datetime import date

def insert_random_data():
    try:
        # 🔗 Kết nối tới MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",         # Container mysql-nompass: không có mật khẩu
            database="bleu"
        )
        cursor = conn.cursor()

        print("✅ Kết nối thành công tới cơ sở dữ liệu 'bleu'.\n")

        # ---- Nhập số lượng ----
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
        print(f"✅ Đã thêm {num_units} Unit.")

        cursor.execute("SELECT unit_ID FROM Unit;")
        unit_ids = [u[0] for u in cursor.fetchall()]

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
                f"Đang học Unit {random.choice(unit_ids)}"
            ))
        cursor.executemany("""
            INSERT INTO USER (createDate, name, email, account, password, level, progress)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, users)
        conn.commit()
        print(f"✅ Đã thêm {num_users} người dùng.")

        cursor.execute("SELECT user_ID FROM USER;")
        user_ids = [u[0] for u in cursor.fetchall()]

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
        print(f"✅ Đã thêm {num_vocab} từ vựng.")

        cursor.execute("SELECT word_ID FROM Vocab;")
        word_ids = [w[0] for w in cursor.fetchall()]

        # ======================================================
        # 4️⃣ QUESTION
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
        print(f"✅ Đã thêm {num_questions} câu hỏi.")

        cursor.execute("SELECT question_ID FROM Question;")
        question_ids = [q[0] for q in cursor.fetchall()]

        # ======================================================
        # 5️⃣ Reading & Listening
        # ======================================================
        readings = [(f"Nội dung đọc {i+1}", unit_ids[i % len(unit_ids)]) for i in range(num_units)]
        cursor.executemany("INSERT INTO Reading (readContent, unit_ID) VALUES (%s, %s);", readings)

        listenings = [(f"https://audio.fake/unit{i+1}.mp3", unit_ids[i % len(unit_ids)]) for i in range(num_units)]
        cursor.executemany("INSERT INTO Listening (linkAudio, unit_ID) VALUES (%s, %s);", listenings)
        conn.commit()
        print(f"✅ Đã thêm {num_units} Reading và Listening.")

        # ======================================================
        # 6️⃣ Learn (liên kết user - unit)
        # ======================================================
        learn_records = []
        seen = set()
        for uid in user_ids:
            unit_id = random.choice(unit_ids)
            if (uid, unit_id) not in seen:
                learn_records.append((unit_id, uid))
                seen.add((uid, unit_id))
        cursor.executemany("INSERT INTO Learn (unit_ID, user_ID) VALUES (%s, %s);", learn_records)
        conn.commit()
        print(f"✅ Đã thêm {len(learn_records)} bản ghi Learn.")

        # ======================================================
        # 7️⃣ FlashCard (giống Learn — không trùng cặp)
        # ======================================================
        flashcards = []
        seen_flash = set()
        for uid in user_ids:
            sampled_words = random.sample(word_ids, min(3, len(word_ids)))  # mỗi user học 3 từ khác nhau
            for wid in sampled_words:
                if (uid, wid) not in seen_flash:
                    flashcards.append((wid, uid))
                    seen_flash.add((uid, wid))
        cursor.executemany("""
            INSERT INTO FlashCard (word_ID, user_ID)
            VALUES (%s, %s);
        """, flashcards)
        conn.commit()
        print(f"✅ Đã thêm {len(flashcards)} FlashCard (mỗi người dùng học 3 từ ngẫu nhiên, không trùng).")

        # ======================================================
        # 8️⃣ UserAnswer — 50% người dùng chưa trả lời
        # ======================================================
        answers = []
        for uid in user_ids:
            qid = random.choice(question_ids)
            unit_id = random.choice(unit_ids)

            if random.random() < 0.5:  # 50% chưa trả lời
                content = None
                result = None
            else:
                content = f"Câu trả lời của user {uid} cho câu {qid}"
                result = random.choice([True, False])

            answers.append((qid, content, unit_id, result, uid))

        cursor.executemany("""
            INSERT INTO UserAnswer (question_ID, content, unit_ID, result, user_ID)
            VALUES (%s, %s, %s, %s, %s);
        """, answers)
        conn.commit()
        print(f"✅ Đã thêm {len(answers)} UserAnswer (có cả các câu chưa trả lời).")

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
