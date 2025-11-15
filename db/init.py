'''
Chú ý: Script này tạo cấu trúc bảng BLEU tự động.
Nó sẽ chạy khi được import hoặc thực thi độc lập.
'''

from db.db import db
import time

my_db = db()
my_db.dml_ddl_operator(
'''
CREATE TABLE `fc_Decks` (
  `deck_id` integer PRIMARY KEY AUTO_INCREMENT,
  `deck_name` varchar(500),
  `deck_user_id` integer,
  `deck_status` integer
);

CREATE TABLE `fc_Cards` (
  `card_id` integer PRIMARY KEY AUTO_INCREMENT,
  `card_fe` varchar(500),
  `card_be` varchar(500),
  `card_status` integer,
  `word_deck_id` integer
);

CREATE TABLE `Users` (
  `user_id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_name` varchar(30),
  `user_password` varchar(30),
  `user_role_id` integer,
  `user_rank` integer,
  `user_status` integer,
  `user_email` varchar(500)
);

CREATE TABLE `Roles` (
  `role_id` integer PRIMARY KEY AUTO_INCREMENT,
  `role_name` varchar(255)
);

CREATE TABLE `Words` (
  `word_id` integer PRIMARY KEY AUTO_INCREMENT,
  `word` varchar(255),
  `word_meaning` varchar(30),
  `word_status` varchar(30),
  `word_difficulty` varchar(30),
  `word_unit_id` int
);

CREATE TABLE `Units` (
  `unit_id` integer PRIMARY KEY AUTO_INCREMENT,
  `unit_name` varchar(50)
);

CREATE TABLE `Tests` (
  `test_id` integer PRIMARY KEY AUTO_INCREMENT,
  `test_lesson_id` int
);

CREATE TABLE `Lessons` (
  `lesson_id` int PRIMARY KEY AUTO_INCREMENT,
  `lesson_unit_id` int,
  `lesson_name` varchar(500)
);

CREATE TABLE `Questions` (
  `question_id` integer PRIMARY KEY AUTO_INCREMENT,
  `question_test_id` integer,
  `question_answer` varchar(30),
  `question_content` varchar(500)
);

CREATE TABLE `Question_options` (
  `question_option_question_id` integer,
  `option_1` varchar(500),
  `option_2` varchar(500),
  `option_3` varchar(500),
  `option_4` varchar(500)
);

CREATE TABLE `Listenings` (
  `listening_test_id` int PRIMARY KEY AUTO_INCREMENT,
  `listening_content` varchar(500),
  `listening_audio` varchar(500)
);

CREATE TABLE `Readings` (
  `reading_test_id` integer PRIMARY KEY AUTO_INCREMENT,
  `reading_content` varchar(500)
);

CREATE TABLE `Learnings` (
  `learning_id` integer PRIMARY KEY AUTO_INCREMENT,
  `learning_user_id` integer,
  `learning_test_id` integer,
  `learning_score` float,
  `learning_is_pass` bool,
  `learning_date` datetime
);

CREATE TABLE `Games` (
  `game_id` integer PRIMARY KEY AUTO_INCREMENT,
  `game_user_id` integer,
  `score` int
);

ALTER TABLE `fc_Decks` ADD FOREIGN KEY (`deck_user_id`) REFERENCES `Users` (`user_id`);

ALTER TABLE `fc_Cards` ADD FOREIGN KEY (`word_deck_id`) REFERENCES `fc_Decks` (`deck_id`);

ALTER TABLE `Users` ADD FOREIGN KEY (`user_role_id`) REFERENCES `Roles` (`role_id`);

ALTER TABLE `Words` ADD FOREIGN KEY (`word_unit_id`) REFERENCES `Units` (`unit_id`);

ALTER TABLE `Tests` ADD FOREIGN KEY (`test_lesson_id`) REFERENCES `Lessons` (`lesson_id`);

ALTER TABLE `Lessons` ADD FOREIGN KEY (`lesson_unit_id`) REFERENCES `Units` (`unit_id`);

ALTER TABLE `Questions` ADD FOREIGN KEY (`question_test_id`) REFERENCES `Tests` (`test_id`);

ALTER TABLE `Question_options` ADD FOREIGN KEY (`question_option_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Listenings` ADD FOREIGN KEY (`listening_test_id`) REFERENCES `Tests` (`test_id`);

ALTER TABLE `Readings` ADD FOREIGN KEY (`reading_test_id`) REFERENCES `Tests` (`test_id`);

ALTER TABLE `Learnings` ADD FOREIGN KEY (`learning_user_id`) REFERENCES `Users` (`user_id`);

ALTER TABLE `Learnings` ADD FOREIGN KEY (`learning_test_id`) REFERENCES `Tests` (`test_id`);

ALTER TABLE `Games` ADD FOREIGN KEY (`game_user_id`) REFERENCES `Users` (`user_id`);

'''
)

print("ạo bảng BLEU thành công.")
