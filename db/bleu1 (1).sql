-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 14, 2025 at 08:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bleu1`
--

-- --------------------------------------------------------

--
-- Table structure for table `fc_cards`
--

CREATE TABLE `fc_cards` (
  `card_id` int(11) NOT NULL,
  `card_fe` varchar(500) DEFAULT NULL,
  `card_be` varchar(500) DEFAULT NULL,
  `card_status` int(11) DEFAULT NULL,
  `card_deck_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fc_cards`
--

INSERT INTO `fc_cards` (`card_id`, `card_fe`, `card_be`, `card_status`, `card_deck_id`) VALUES
(1, 'hello', 'xin chào', 1, 1),
(2, 'please', 'làm ơn', 1, 1),
(3, 'sorry', 'xin lỗi', 1, 1),
(7, 'guitar', 'đàn ghi-ta', 1, 3),
(8, 'painting', 'vẽ tranh', 1, 3),
(9, 'running', 'chạy bộ', 1, 3),
(11, 'The wind rises', 'Gió nổi', 0, 3);

-- --------------------------------------------------------

--
-- Table structure for table `fc_decks`
--

CREATE TABLE `fc_decks` (
  `deck_id` int(11) NOT NULL,
  `deck_name` varchar(500) DEFAULT NULL,
  `deck_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fc_decks`
--

INSERT INTO `fc_decks` (`deck_id`, `deck_name`, `deck_user_id`) VALUES
(1, 'Basics Deck', 2),
(2, 'Travel Deck', 2),
(3, 'Hobbies Deck', 3);

-- --------------------------------------------------------

--
-- Table structure for table `games`
--

CREATE TABLE `games` (
  `game_id` int(11) NOT NULL,
  `game_user_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `games`
--

INSERT INTO `games` (`game_id`, `game_user_id`, `score`) VALUES
(1, 2, 120),
(2, 3, 80);

-- --------------------------------------------------------

--
-- Table structure for table `learnings`
--

CREATE TABLE `learnings` (
  `learning_id` int(11) NOT NULL,
  `learning_user_id` int(11) DEFAULT NULL,
  `learning_test_id` int(11) DEFAULT NULL,
  `learning_score` float DEFAULT NULL,
  `learning_is_pass` tinyint(1) DEFAULT NULL,
  `learning_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `learnings`
--

INSERT INTO `learnings` (`learning_id`, `learning_user_id`, `learning_test_id`, `learning_score`, `learning_is_pass`, `learning_date`) VALUES
(1, 2, 1, 85, 1, '2025-11-10 10:00:00'),
(2, 2, 2, 60, 0, '2025-11-11 11:15:00'),
(3, 3, 1, 90, 1, '2025-11-09 09:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

CREATE TABLE `lessons` (
  `lesson_id` int(11) NOT NULL,
  `lesson_unit_id` int(11) DEFAULT NULL,
  `lesson_name` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`lesson_id`, `lesson_unit_id`, `lesson_name`) VALUES
(1, 1, 'Lesson 1 - Basics'),
(2, 2, 'Lesson 2 - Travel'),
(3, 3, 'Lesson 3 - Work'),
(4, 4, 'Lesson 4 - Food'),
(5, 5, 'Lesson 5 - Hobbies'),
(6, 1, 'Housechord'),
(7, 1, 'What\'s on earth is going on ?'),
(8, 1, 'Do what you like!');

-- --------------------------------------------------------

--
-- Table structure for table `listenings`
--

CREATE TABLE `listenings` (
  `listening_test_id` int(11) NOT NULL,
  `listening_content` varchar(500) DEFAULT NULL,
  `listening_audio` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `listenings`
--

INSERT INTO `listenings` (`listening_test_id`, `listening_content`, `listening_audio`) VALUES
(1, 'Listen: greeting dialog', 'audio/lesson1_greeting.mp3'),
(2, 'Listen: airport announcements', 'audio/lesson2_airport.mp3'),
(3, 'Listen: office conversation', 'audio/lesson3_office.mp3'),
(4, 'Listen: ordering food', 'audio/lesson4_food.mp3'),
(5, 'Listen: hobby talk', 'audio/lesson5_hobby.mp3');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `question_id` int(11) NOT NULL,
  `question_test_id` int(11) DEFAULT NULL,
  `question_answer` varchar(30) DEFAULT NULL,
  `question_content` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `question_test_id`, `question_answer`, `question_content`) VALUES
(1, 1, '1', 'What is the meaning of \"hello\"?'),
(2, 1, '2', 'Which word means \"xin lỗi\"?'),
(3, 2, '3', 'Where do you check in for a flight?'),
(4, 2, '1', 'Which one means \"hành lý\"?'),
(5, 3, '4', 'What is a deadline?'),
(6, 3, '2', 'Who works with you? (colleague)'),
(7, 4, '1', 'Which meal is \"bữa sáng\"?'),
(8, 4, '3', 'Which word describes food that is \"cay\"?'),
(9, 5, '2', 'Which hobby uses a camera?'),
(10, 5, '1', 'Which hobby is playing the guitar?');

-- --------------------------------------------------------

--
-- Table structure for table `question_options`
--

CREATE TABLE `question_options` (
  `question_option_question_id` int(11) DEFAULT NULL,
  `option_1` varchar(500) DEFAULT NULL,
  `option_2` varchar(500) DEFAULT NULL,
  `option_3` varchar(500) DEFAULT NULL,
  `option_4` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `question_options`
--

INSERT INTO `question_options` (`question_option_question_id`, `option_1`, `option_2`, `option_3`, `option_4`) VALUES
(1, 'xin chào', 'tạm biệt', 'làm ơn', 'cảm ơn'),
(2, 'xin chào', 'xin lỗi', 'tạm biệt', 'cảm ơn'),
(3, 'hotel', 'station', 'airport', 'restaurant'),
(4, 'passport', 'ticket', 'seat', 'luggage'),
(5, 'a meeting', 'a project', 'a colleague', 'a deadline'),
(6, 'manager', 'colleague', 'visitor', 'customer'),
(7, 'breakfast', 'lunch', 'dinner', 'snack'),
(8, 'sweet', 'salty', 'spicy', 'bitter'),
(9, 'guitar', 'photography', 'running', 'painting'),
(10, 'guitar', 'painting', 'photography', 'gardening');

-- --------------------------------------------------------

--
-- Table structure for table `readings`
--

CREATE TABLE `readings` (
  `reading_test_id` int(11) NOT NULL,
  `reading_content` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `readings`
--

INSERT INTO `readings` (`reading_test_id`, `reading_content`) VALUES
(1, 'Short text about greetings'),
(2, 'Short text about airports and travel'),
(3, 'Short text about workplace vocabulary'),
(4, 'Short recipe and food description'),
(5, 'Short paragraph about hobbies');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(1, 'admin'),
(2, 'user');

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE `tests` (
  `test_id` int(11) NOT NULL,
  `test_lesson_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tests`
--

INSERT INTO `tests` (`test_id`, `test_lesson_id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `units`
--

CREATE TABLE `units` (
  `unit_id` int(11) NOT NULL,
  `unit_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `units`
--

INSERT INTO `units` (`unit_id`, `unit_name`) VALUES
(1, 'Unit 1 - Basics'),
(2, 'Unit 2 - Travel'),
(3, 'Unit 3 - Work'),
(4, 'Unit 4 - Food'),
(5, 'Unit 5 - Hobbies');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(30) DEFAULT NULL,
  `user_password` varchar(30) DEFAULT NULL,
  `user_role_id` int(11) DEFAULT NULL,
  `user_rank` int(11) DEFAULT NULL,
  `user_status` int(11) DEFAULT NULL,
  `user_email` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_password`, `user_role_id`, `user_rank`, `user_status`, `user_email`) VALUES
(1, 'admin', 'admin123', 1, 100, 1, 'admin@example.com'),
(2, 'thanh', 'thanhbodoi', 2, 10, 1, 'thanh@example.com'),
(3, 'test_user', 'test123', 2, 5, 1, 'test@example.com'),
(4, 'thinh', 'thinhbodoi', 2, 0, 1, 'thinh@gmail.com'),
(5, '123', '123', 2, 0, 1, '123'),
(6, 'vy', 'vybodoi', 2, 0, 1, '1@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `words`
--

CREATE TABLE `words` (
  `word_id` int(11) NOT NULL,
  `word` varchar(255) DEFAULT NULL,
  `word_meaning` varchar(30) DEFAULT NULL,
  `word_status` varchar(30) DEFAULT NULL,
  `word_difficulty` varchar(30) DEFAULT NULL,
  `word_unit_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `words`
--

INSERT INTO `words` (`word_id`, `word`, `word_meaning`, `word_status`, `word_difficulty`, `word_unit_id`) VALUES
(1, 'hello', 'xin chào', 'active', 'easy', 1),
(2, 'goodbye', 'tạm biệt', 'active', 'easy', 1),
(3, 'please', 'làm ơn', 'active', 'easy', 1),
(4, 'thank you', 'cảm ơn', 'active', 'easy', 1),
(5, 'sorry', 'xin lỗi', 'active', 'easy', 1),
(6, 'airport', 'sân bay', 'active', 'medium', 2),
(7, 'ticket', 'vé', 'active', 'medium', 2),
(8, 'luggage', 'hành lý', 'active', 'medium', 2),
(9, 'passport', 'hộ chiếu', 'active', 'medium', 2),
(10, 'arrival', 'đến nơi', 'active', 'medium', 2),
(11, 'office', 'văn phòng', 'active', 'medium', 3),
(12, 'meeting', 'cuộc họp', 'active', 'medium', 3),
(13, 'project', 'dự án', 'active', 'hard', 3),
(14, 'deadline', 'hạn chót', 'active', 'hard', 3),
(15, 'colleague', 'đồng nghiệp', 'active', 'medium', 3),
(16, 'breakfast', 'bữa sáng', 'active', 'easy', 4),
(17, 'lunch', 'bữa trưa', 'active', 'easy', 4),
(18, 'dinner', 'bữa tối', 'active', 'easy', 4),
(19, 'recipe', 'công thức', 'active', 'medium', 4),
(20, 'spicy', 'cay', 'active', 'medium', 4),
(21, 'guitar', 'đàn ghi-ta', 'active', 'medium', 5),
(22, 'painting', 'vẽ tranh', 'active', 'medium', 5),
(23, 'running', 'chạy bộ', 'active', 'easy', 5),
(24, 'photography', 'nhiếp ảnh', 'active', 'hard', 5),
(25, 'gardening', 'làm vườn', 'active', 'easy', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fc_cards`
--
ALTER TABLE `fc_cards`
  ADD PRIMARY KEY (`card_id`),
  ADD KEY `word_deck_id` (`card_deck_id`);

--
-- Indexes for table `fc_decks`
--
ALTER TABLE `fc_decks`
  ADD PRIMARY KEY (`deck_id`),
  ADD KEY `deck_user_id` (`deck_user_id`);

--
-- Indexes for table `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`game_id`),
  ADD KEY `game_user_id` (`game_user_id`);

--
-- Indexes for table `learnings`
--
ALTER TABLE `learnings`
  ADD PRIMARY KEY (`learning_id`),
  ADD KEY `learning_user_id` (`learning_user_id`),
  ADD KEY `learning_test_id` (`learning_test_id`);

--
-- Indexes for table `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`lesson_id`),
  ADD KEY `lesson_unit_id` (`lesson_unit_id`);

--
-- Indexes for table `listenings`
--
ALTER TABLE `listenings`
  ADD PRIMARY KEY (`listening_test_id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`question_id`),
  ADD KEY `question_test_id` (`question_test_id`);

--
-- Indexes for table `question_options`
--
ALTER TABLE `question_options`
  ADD KEY `question_option_question_id` (`question_option_question_id`);

--
-- Indexes for table `readings`
--
ALTER TABLE `readings`
  ADD PRIMARY KEY (`reading_test_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `tests`
--
ALTER TABLE `tests`
  ADD PRIMARY KEY (`test_id`),
  ADD KEY `test_lesson_id` (`test_lesson_id`);

--
-- Indexes for table `units`
--
ALTER TABLE `units`
  ADD PRIMARY KEY (`unit_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `user_role_id` (`user_role_id`);

--
-- Indexes for table `words`
--
ALTER TABLE `words`
  ADD PRIMARY KEY (`word_id`),
  ADD KEY `word_unit_id` (`word_unit_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fc_cards`
--
ALTER TABLE `fc_cards`
  MODIFY `card_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `fc_decks`
--
ALTER TABLE `fc_decks`
  MODIFY `deck_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `games`
--
ALTER TABLE `games`
  MODIFY `game_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `learnings`
--
ALTER TABLE `learnings`
  MODIFY `learning_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `lessons`
--
ALTER TABLE `lessons`
  MODIFY `lesson_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `listenings`
--
ALTER TABLE `listenings`
  MODIFY `listening_test_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `readings`
--
ALTER TABLE `readings`
  MODIFY `reading_test_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tests`
--
ALTER TABLE `tests`
  MODIFY `test_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `units`
--
ALTER TABLE `units`
  MODIFY `unit_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `words`
--
ALTER TABLE `words`
  MODIFY `word_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fc_cards`
--
ALTER TABLE `fc_cards`
  ADD CONSTRAINT `fc_cards_ibfk_1` FOREIGN KEY (`card_deck_id`) REFERENCES `fc_decks` (`deck_id`);

--
-- Constraints for table `fc_decks`
--
ALTER TABLE `fc_decks`
  ADD CONSTRAINT `fc_decks_ibfk_1` FOREIGN KEY (`deck_user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `games`
--
ALTER TABLE `games`
  ADD CONSTRAINT `games_ibfk_1` FOREIGN KEY (`game_user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `learnings`
--
ALTER TABLE `learnings`
  ADD CONSTRAINT `learnings_ibfk_1` FOREIGN KEY (`learning_user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `learnings_ibfk_2` FOREIGN KEY (`learning_test_id`) REFERENCES `tests` (`test_id`);

--
-- Constraints for table `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`lesson_unit_id`) REFERENCES `units` (`unit_id`);

--
-- Constraints for table `listenings`
--
ALTER TABLE `listenings`
  ADD CONSTRAINT `listenings_ibfk_1` FOREIGN KEY (`listening_test_id`) REFERENCES `tests` (`test_id`);

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`question_test_id`) REFERENCES `tests` (`test_id`);

--
-- Constraints for table `question_options`
--
ALTER TABLE `question_options`
  ADD CONSTRAINT `question_options_ibfk_1` FOREIGN KEY (`question_option_question_id`) REFERENCES `questions` (`question_id`);

--
-- Constraints for table `readings`
--
ALTER TABLE `readings`
  ADD CONSTRAINT `readings_ibfk_1` FOREIGN KEY (`reading_test_id`) REFERENCES `tests` (`test_id`);

--
-- Constraints for table `tests`
--
ALTER TABLE `tests`
  ADD CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`test_lesson_id`) REFERENCES `lessons` (`lesson_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`user_role_id`) REFERENCES `roles` (`role_id`);

--
-- Constraints for table `words`
--
ALTER TABLE `words`
  ADD CONSTRAINT `words_ibfk_1` FOREIGN KEY (`word_unit_id`) REFERENCES `units` (`unit_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
