-- =============================================
-- SCRIPT TẠO DỮ LIỆU MẪU (CHỈ GỒM ADMIN & USER)
-- =============================================

-- Bảng Roles
INSERT INTO Roles (role_name) VALUES 
('Admin'),
('User');

-- Bảng Users
INSERT INTO Users (user_name, user_password, user_role_id, user_rank, user_level, user_status) VALUES
('admin', 'admin123', 1, 10, 99, 1),
('alice', '123456', 2, 5, 10, 1),
('bob', 'password', 2, 3, 7, 1);

-- Bảng Units
INSERT INTO Units (unit_name) VALUES
('Unit 1: Basics'),
('Unit 2: Vocabulary'),
('Unit 3: Grammar');

-- Bảng Questions
INSERT INTO Questions (question_unit_id, question_answer, question_content) VALUES
(1, 'B', 'What is the capital of France?'),
(2, 'A', 'Choose the synonym of "happy"'),
(3, 'C', 'Which sentence is grammatically correct?');

-- Bảng Question_options
INSERT INTO Question_options (question_option_question_id, option_1, option_2, option_3, option_4) VALUES
(1, 'Berlin', 'Paris', 'Rome', 'Madrid'),
(2, 'Glad', 'Sad', 'Tired', 'Angry'),
(3, 'He go to school.', 'She are eating.', 'They are playing.', 'I has a pen.');

-- Bảng Lessons
INSERT INTO Lessons (lesson_unit_id, lesson_question_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Bảng Words
INSERT INTO Words (word, word_meaning, word_status, word_difficulty, word_lesson_id) VALUES
('apple', 'quả táo', 'active', 'easy', 1),
('happiness', 'hạnh phúc', 'active', 'medium', 2),
('grammar', 'ngữ pháp', 'active', 'hard', 3);

-- Bảng Listenings
INSERT INTO Listenings (listening_question_id, listening_content, listening_audio) VALUES
(1, 'Listen to the dialogue about travel.', 'audio1.mp3'),
(2, 'Listen and choose the correct synonym.', 'audio2.mp3'),
(3, 'Listen and complete the sentence.', 'audio3.mp3');

-- Bảng Readings
INSERT INTO Readings (reading_question_id, reading_content) VALUES
(1, 'Paris is the capital and most populous city of France.'),
(2, 'Happiness is a feeling of pleasure and satisfaction.'),
(3, 'Grammar helps us form correct sentences.');

-- Bảng Learnings
INSERT INTO Learnings (learning_user_id, learning_unit_id, learning_finished_time, learning_score, learning_is_pass, learning_user_progress, learning_date) VALUES
(2, 1, NOW(), 8.5, TRUE, 'Completed', NOW()),
(3, 2, NOW(), 7.0, TRUE, 'In progress', NOW());

-- Bảng Games
INSERT INTO Games (game_user_id, correct_word_quantity) VALUES
(2, 15),
(3, 10);

-- Bảng Answers
INSERT INTO Answers (answer_question_id, answer_user_id, answer_user_answer) VALUES
(1, 2, 'B'),
(2, 3, 'A');

-- =============================================
-- KẾT THÚC TẠO DỮ LIỆU
-- =============================================
