'''
Chú ý đây là script tạo cấu trúc bảng tự động. Scripts sẽ chạy tự động khi được import hoặc khi được biên dịch.

'''

from db import db
import time

my_db = db()
my_db.dml_ddl_operator(
'''
CREATE TABLE `Users` (
  `user_id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_name` varchar(30),
  `user_password` varchar(30),
  `user_role_id` integer,
  `user_rank` integer,
  `user_level` integer,
  `user_status` integer
);

CREATE TABLE `Roles` (
  `role_id` integer PRIMARY KEY AUTO_INCREMENT,
  `role_name` varchar(255)
);

CREATE TABLE `Words` (
  `word` varchar(30) PRIMARY KEY,
  `word_meaning` varchar(30),
  `word_status` varchar(30),
  `word_difficulty` varchar(30),
  `word_question_id` int
);

CREATE TABLE `Units` (
  `unit_id` integer PRIMARY KEY AUTO_INCREMENT,
  `unit_name` varchar(50)
);

CREATE TABLE `Lessons` (
  `lesson_id` int PRIMARY KEY AUTO_INCREMENT,
  `lesson_unit_id` int,
  `lesson_question_id` int
);

CREATE TABLE `Questions` (
  `question_id` integer PRIMARY KEY AUTO_INCREMENT,
  `question_unit_id` integer,
  `question_answer` varchar(30),
  `question_content` varchar(500)
);

CREATE TABLE `Question_options` (
  `question_option_id` integer PRIMARY KEY AUTO_INCREMENT,
  `question_option_question_id` integer,
  `option_1` varchar(500),
  `option_2` varchar(500),
  `option_3` varchar(500),
  `option_4` varchar(500)
);

CREATE TABLE `Listenings` (
  `listening_question_id` integer PRIMARY KEY AUTO_INCREMENT,
  `listening_content` varchar(500),
  `listening_audio` varchar(500)
);

CREATE TABLE `Readings` (
  `reading_question_id` integer PRIMARY KEY AUTO_INCREMENT,
  `reading_content` varchar(500)
);

CREATE TABLE `Learnings` (
  `learning_id` integer PRIMARY KEY AUTO_INCREMENT,
  `learning_user_id` integer,
  `learning_unit_id` integer,
  `learning_finished_time` timestamp,
  `learning_score` float,
  `learning_is_pass` bool,
  `learning_user_progress` varchar(30)
);

CREATE TABLE `Games` (
  `game_id` integer PRIMARY KEY AUTO_INCREMENT,
  `game_user_id1` integer,
  `game_user_id2` integer,
  `game_user_id_won` integer
);

CREATE TABLE `Answers` (
  `answer_id` integer PRIMARY KEY AUTO_INCREMENT,
  `answer_question_id` integer,
  `answer_user_id` integer,
  `answer_user_answer` varchar(50)
);

ALTER TABLE `Users` ADD FOREIGN KEY (`user_role_id`) REFERENCES `Roles` (`role_id`);

ALTER TABLE `Words` ADD FOREIGN KEY (`word_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Lessons` ADD FOREIGN KEY (`lesson_unit_id`) REFERENCES `Units` (`unit_id`);

ALTER TABLE `Lessons` ADD FOREIGN KEY (`lesson_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Questions` ADD FOREIGN KEY (`question_unit_id`) REFERENCES `Units` (`unit_id`);

ALTER TABLE `Questions` ADD FOREIGN KEY (`question_id`) REFERENCES `Question_options` (`question_option_question_id`);

ALTER TABLE `Listenings` ADD FOREIGN KEY (`listening_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Readings` ADD FOREIGN KEY (`reading_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Learnings` ADD FOREIGN KEY (`learning_user_id`) REFERENCES `Users` (`user_id`);

ALTER TABLE `Learnings` ADD FOREIGN KEY (`learning_unit_id`) REFERENCES `Units` (`unit_id`);

ALTER TABLE `Users` ADD FOREIGN KEY (`user_id`) REFERENCES `Games` (`game_user_id1`);

ALTER TABLE `Users` ADD FOREIGN KEY (`user_id`) REFERENCES `Games` (`game_user_id2`);

ALTER TABLE `Answers` ADD FOREIGN KEY (`answer_question_id`) REFERENCES `Questions` (`question_id`);

ALTER TABLE `Answers` ADD FOREIGN KEY (`answer_user_id`) REFERENCES `Users` (`user_id`);
'''
)
print("Tạo bảng thành công.")
