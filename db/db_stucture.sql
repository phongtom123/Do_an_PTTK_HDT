-- =============================================
-- 🚀 RESET DATABASE
-- =============================================
DROP DATABASE IF EXISTS bleu1;
CREATE DATABASE bleu1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bleu1;

SET FOREIGN_KEY_CHECKS = 0;

-- =============================================
-- 🧱 TẠO BẢNG
-- =============================================

CREATE TABLE Roles (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(255)
);

CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(30),
  user_password VARCHAR(30),
  user_role_id INT,
  user_rank INT,
  user_level INT,
  user_status INT,
  user_email VARCHAR(500),
  FOREIGN KEY (user_role_id) REFERENCES Roles(role_id)
);

CREATE TABLE Units (
  unit_id INT AUTO_INCREMENT PRIMARY KEY,
  unit_name VARCHAR(50)
);

CREATE TABLE Lessons (
  lesson_id INT AUTO_INCREMENT PRIMARY KEY,
  lesson_name VARCHAR(255),
  lesson_unit_id INT,
  lesson_question_id INT,
  FOREIGN KEY (lesson_unit_id) REFERENCES Units(unit_id)
);

CREATE TABLE Questions (
  question_id INT AUTO_INCREMENT PRIMARY KEY,
  question_unit_id INT,
  question_answer VARCHAR(30),
  question_content VARCHAR(500),
  FOREIGN KEY (question_unit_id) REFERENCES Units(unit_id)
);

CREATE TABLE Question_options (
  question_option_id INT AUTO_INCREMENT PRIMARY KEY,
  question_option_question_id INT,
  option_1 VARCHAR(500),
  option_2 VARCHAR(500),
  option_3 VARCHAR(500),
  option_4 VARCHAR(500),
  FOREIGN KEY (question_option_question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Readings (
  reading_question_id INT PRIMARY KEY,
  reading_content TEXT,
  FOREIGN KEY (reading_question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Listenings (
  listening_question_id INT PRIMARY KEY,
  listening_content VARCHAR(500),
  listening_audio VARCHAR(500),
  FOREIGN KEY (listening_question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Words (
  word_id INT AUTO_INCREMENT PRIMARY KEY,
  word VARCHAR(255),
  word_meaning VARCHAR(255),
  word_status VARCHAR(30),
  word_difficulty VARCHAR(30),
  word_lesson_id INT,
  FOREIGN KEY (word_lesson_id) REFERENCES Lessons(lesson_id)
);

-- Lưu lịch sử chơi game
CREATE TABLE GameHistory (
  history_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  score INT,
  game_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- 👥 ROLES + USERS
-- =============================================

INSERT INTO Roles (role_name) VALUES ('Admin'), ('User');

INSERT INTO Users (user_name, user_password, user_role_id, user_rank, user_level, user_status, user_email)
VALUES
('admin', 'admin123', 1, 10, 99, 1, 'admin@hocanh.vn'),
('alice', '123456', 2, 5, 10, 1, 'alice@gmail.com'),
('bob', 'password', 2, 3, 7, 1, 'bob@gmail.com');

-- =============================================
-- 📘 UNITS + LESSONS
-- =============================================

INSERT INTO Units (unit_name) VALUES
('Unit 1: Daily Life'),
('Unit 2: Travel and Transport'),
('Unit 3: Food and Drinks'),
('Unit 4: Technology'),
('Unit 5: Emotions');

INSERT INTO Lessons (lesson_name, lesson_unit_id, lesson_question_id) VALUES
('Morning Routine', 1, NULL),
('At Home', 1, NULL),
('At the Airport', 2, NULL),
('On the Road', 2, NULL),
('Favorite Meals', 3, NULL),
('Healthy Food', 3, NULL),
('Computers', 4, NULL),
('Internet Life', 4, NULL),
('Feeling Happy', 5, NULL),
('Overcoming Fear', 5, NULL);

-- =============================================
-- ❓ QUESTIONS + OPTIONS
-- =============================================

INSERT INTO Questions (question_unit_id, question_answer, question_content) VALUES
(1, 'C', 'What time does the person wake up every morning?'),
(1, 'A', 'What does he drink after brushing his teeth?'),
(2, 'D', 'Which document is needed before boarding?'),
(2, 'A', 'Where is the departure gate located?'),
(3, 'B', 'Which food is considered healthy?'),
(3, 'D', 'What should we avoid to stay fit?'),
(4, 'A', 'What part of a computer shows images?'),
(4, 'B', 'What is the main benefit of the Internet?'),
(5, 'C', 'What makes the girl feel happy in the passage?'),
(5, 'A', 'What helps the boy overcome fear?');

INSERT INTO Question_options (question_option_question_id, option_1, option_2, option_3, option_4) VALUES
(1, 'At 5 AM', 'At 6 AM', 'At 7 AM', 'At 8 AM'),
(2, 'Milk', 'Juice', 'Tea', 'Water'),
(3, 'Ticket', 'Visa', 'Bag', 'Passport'),
(4, 'Gate 1', 'Gate 5', 'Gate 9', 'Gate 11'),
(5, 'Fast food', 'Salad', 'Pizza', 'Cake'),
(6, 'Exercise', 'Sleep', 'Junk food', 'Overeating'),
(7, 'Screen', 'Mouse', 'Keyboard', 'Speaker'),
(8, 'Entertainment', 'Communication', 'Shopping', 'Cooking'),
(9, 'Playing games', 'Eating sweets', 'Meeting friends', 'Watching TV'),
(10, 'Confidence', 'Friends', 'Running', 'Fear itself');

-- =============================================
-- 📚 WORDS (LIÊN KẾT VỚI LESSONS)
-- =============================================

INSERT INTO Words (word, word_meaning, word_status, word_difficulty, word_lesson_id) VALUES
('morning', 'buổi sáng', 'active', 'easy', 1),
('work', 'làm việc', 'active', 'medium', 1),
('family', 'gia đình', 'active', 'easy', 2),
('passport', 'hộ chiếu', 'active', 'medium', 3),
('train', 'tàu hỏa', 'active', 'medium', 4),
('fruit', 'trái cây', 'active', 'easy', 5),
('junk food', 'đồ ăn nhanh', 'inactive', 'medium', 6),
('screen', 'màn hình', 'active', 'easy', 7),
('Internet', 'mạng internet', 'active', 'medium', 😎,
('happy', 'vui vẻ', 'active', 'easy', 9),
('fear', 'nỗi sợ', 'active', 'medium', 10);

-- =============================================
-- 📖 READINGS (CÓ CHỨA ÍT NHẤT 1 TỪ TỪ VỰNG)
-- =============================================

INSERT INTO Readings (reading_question_id, reading_content) VALUES
(1, 'Every morning, I wake up early and go to work. Morning coffee always helps me start the day better.'),
(2, 'After brushing my teeth, I usually drink milk and then prepare breakfast for my family.'),
(3, 'Before traveling abroad, make sure you have your passport and ticket ready.'),
(4, 'Traveling by train is fun because you can look outside and see the mountains passing by.'),
(5, 'Eating fruit and vegetables keeps your body healthy and full of energy.'),
(6, 'Avoid eating too much junk food; it can make you tired and unhealthy.'),
(7, 'The computer screen is bright, and I can see all my work clearly on it.'),
(8, 'The Internet helps people communicate, study, and share ideas all over the world.'),
(9, 'The girl feels happy because her friends gave her a beautiful gift.'),
(10, 'The boy was afraid at first, but later he faced his fear with confidence.');

-- =============================================
-- 🎧 LISTENINGS (MẪU)
-- =============================================

INSERT INTO Listenings (listening_question_id, listening_content, listening_audio) VALUES
(1, 'A man describes his daily morning routine.', './audio/listening1.mp3'),
(2, 'A woman talks about eating breakfast with her family.', './audio/listening2.mp3'),
(3, 'An airport staff gives passport checking instructions.', './audio/listening3.mp3'),
(4, 'A traveler shares his train experience.', './audio/listening4.mp3'),
(5, 'A doctor talks about eating fruit and vegetables.', './audio/listening5.mp3'),
(6, 'A coach advises to avoid junk food.', './audio/listening6.mp3'),
(7, 'A student explains how to use a computer screen.', './audio/listening7.mp3'),
(8, 'A teacher talks about the benefits of the Internet.', './audio/listening8.mp3'),
(9, 'A child shares what makes her happy.', './audio/listening9.mp3'),
(10, 'A psychologist helps a boy overcome fear.', './audio/listening10.mp3');

-- =============================================
-- 🧠 LIÊN KẾT LESSON → QUESTION
-- =============================================
UPDATE Lessons SET lesson_question_id = 1 WHERE lesson_id = 1;
UPDATE Lessons SET lesson_question_id = 2 WHERE lesson_id = 2;
UPDATE Lessons SET lesson_question_id = 3 WHERE lesson_id = 3;
UPDATE Lessons SET lesson_question_id = 4 WHERE lesson_id = 4;
UPDATE Lessons SET lesson_question_id = 5 WHERE lesson_id = 5;
UPDATE Lessons SET lesson_question_id = 6 WHERE lesson_id = 6;
UPDATE Lessons SET lesson_question_id = 7 WHERE lesson_id = 7;
UPDATE Lessons SET lesson_question_id = 8 WHERE lesson_id = 8;
UPDATE Lessons SET lesson_question_id = 9 WHERE lesson_id = 9;
UPDATE Lessons SET lesson_question_id = 10 WHERE lesson_id = 10;

-- =============================================
-- ✅ KIỂM TRA
-- =============================================
SELECT COUNT(*) AS total_units FROM Units;
SELECT COUNT(*) AS total_lessons FROM Lessons;
SELECT COUNT(*) AS total_questions FROM Questions;
SELECT COUNT(*) AS total_words FROM Words;
SELECT COUNT(*) AS total_readings FROM Readings;