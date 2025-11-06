from db import db

my_db = db()
my_db.dml_ddl_operator(
'''
-- Dữ liệu cho bảng Roles
INSERT INTO `Roles` (`role_id`, `role_name`) VALUES
(1, 'Admin'),
(2, 'User'),
(3, 'Guest');

-- Dữ liệu cho bảng Units
INSERT INTO `Units` (`unit_id`, `unit_name`) VALUES
(1, 'Unit 1: Greetings and Introductions'),
(2, 'Unit 2: Daily Routines'),
(3, 'Unit 3: Food and Drinks'),
(4, 'Unit 4: Travel');

-- Dữ liệu cho bảng Users
-- user_role_id tham chiếu đến Roles.role_id (1=Admin, 2=User)
INSERT INTO `Users` (`user_id`, `user_name`, `user_password`, `user_role_id`, `user_rank`, `user_level`, `user_status`) VALUES
(101, 'nguyenvana', 'pass123', 2, 1, 5, 1),
(102, 'tranvanb', 'secure456', 2, 2, 4, 1),
(103, 'lethic', 'adminpass', 1, 0, 10, 1),
(104, 'phamvand', 'testpass', 2, 3, 3, 0);

-- Dữ liệu cho bảng Questions
-- question_unit_id tham chiếu đến Units.unit_id
INSERT INTO `Questions` (`question_id`, `question_unit_id`, `question_answer`, `question_content`) VALUES
(201, 1, 'Hello', 'Choose the best response: "Hi, how are you?"'),
(202, 1, 'Nice to meet you', 'Fill in the blank: "My name is Tom. ___, Sarah."'),
(203, 2, 'breakfast', 'What is the first meal of the day?'),
(204, 3, 'Water', 'Which of the following is a drink?');

-- Dữ liệu cho bảng Question_options
-- question_option_question_id tham chiếu đến Questions.question_id
-- (Lưu ý: Bạn có ràng buộc khóa ngoại Questions.question_id tham chiếu đến Question_options.question_option_question_id, điều này hơi bất thường. Tôi đang giả sử Question_options.question_option_question_id là FK)
INSERT INTO `Question_options` (`question_option_id`, `question_option_question_id`, `option_1`, `option_2`, `option_3`, `option_4`) VALUES
(301, 201, 'Goodbye', 'Hello', 'See you later', 'Thank you'),
(302, 202, 'I am fine', 'Nice to meet you', 'Good morning', 'I go to school'),
(303, 203, 'dinner', 'lunch', 'breakfast', 'supper'),
(304, 204, 'Bread', 'Apple', 'Water', 'Cheese');

-- Dữ liệu cho bảng Words
-- word_question_id tham chiếu đến Questions.question_id (Đây là một ràng buộc hơi lạ, tôi sẽ giả định đây là ID của một câu hỏi liên quan đến từ vựng đó)
INSERT INTO `Words` (`word`, `word_meaning`, `word_status`, `word_difficulty`, `word_question_id`) VALUES
('Hello', 'Xin chào', 'Learned', 'Easy', 201),
('Breakfast', 'Bữa sáng', 'Studying', 'Medium', 203),
('Travel', 'Du lịch', 'New', 'Hard', 204);

-- Dữ liệu cho bảng Lessons
-- lesson_unit_id tham chiếu đến Units.unit_id
-- lesson_question_id tham chiếu đến Questions.question_id
INSERT INTO `Lessons` (`lesson_id`, `lesson_unit_id`, `lesson_question_id`) VALUES
(401, 1, 201),
(402, 1, 202),
(403, 2, 203),
(404, 3, 204);

-- Dữ liệu cho bảng Listenings
-- listening_question_id tham chiếu đến Questions.question_id
INSERT INTO `Listenings` (`listening_question_id`, `listening_content`, `listening_audio`) VALUES
(201, 'Nghe và chọn câu trả lời đúng cho cuộc hội thoại chào hỏi.', 'audio/greeting_conv.mp3');

-- Dữ liệu cho bảng Readings
-- reading_question_id tham chiếu đến Questions.question_id
INSERT INTO `Readings` (`reading_question_id`, `reading_content`) VALUES
(202, 'Đọc đoạn văn ngắn về việc giới thiệu bản thân và trả lời câu hỏi.');

-- Dữ liệu cho bảng Learnings
-- learning_user_id tham chiếu đến Users.user_id
-- learning_unit_id tham chiếu đến Units.unit_id
INSERT INTO `Learnings` (`learning_id`, `learning_user_id`, `learning_unit_id`, `learning_finished_time`, `learning_score`, `learning_is_pass`, `learning_user_progress`) VALUES
(501, 101, 1, '2025-10-25 10:30:00', 9.5, TRUE, 'Finished'),
(502, 102, 1, '2025-10-26 15:00:00', 7.0, TRUE, 'Finished'),
(503, 101, 2, '2025-10-27 08:00:00', 0.0, FALSE, 'In Progress');

-- Dữ liệu cho bảng Games
-- game_user_id1, game_user_id2, game_user_id_won tham chiếu đến Users.user_id
INSERT INTO `Games` (`game_id`, `game_user_id1`, `game_user_id2`, `game_user_id_won`) VALUES
(601, 101, 102, 101), -- user 101 thắng user 102
(602, 102, 103, 102); -- user 102 thắng user 103

-- Dữ liệu cho bảng Answers
-- answer_question_id tham chiếu đến Questions.question_id
-- answer_user_id tham chiếu đến Users.user_id
INSERT INTO `Answers` (`answer_id`, `answer_question_id`, `answer_user_id`, `answer_user_answer`) VALUES
(701, 201, 101, 'Hello'), -- Đúng
(702, 202, 101, 'I am fine'), -- Sai
(703, 203, 102, 'breakfast'), -- Đúng
(704, 201, 104, 'See you later'); -- Sai
'''
)