-- =============================
-- TẠO DỮ LIỆU MẪU CHO fc.Deck & fc.Words
-- =============================

-- 1️⃣ Decks
INSERT INTO fc.Deck (deck_name, deck_status) VALUES
('Daily Vocabulary', 1),
('Travel & Places', 1),
('Food & Drinks', 1),
('Technology', 1),
('Emotions', 1),
('Nature & Environment', 1),
('Jobs & Careers', 1),
('Health & Body', 1),
('Education', 1),
('Household Items', 1);

-- 2️⃣ Words (10–20 từ cho mỗi deck)
-- Deck 1: Daily Vocabulary
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('morning', 'the early part of the day', 'buổi sáng', 1, 1),
('evening', 'the later part of the day', 'buổi tối', 1, 1),
('work', 'to do a job or task', 'làm việc', 1, 1),
('rest', 'to relax or take a break', 'nghỉ ngơi', 1, 1),
('friend', 'a person you like', 'bạn bè', 1, 1),
('busy', 'having a lot to do', 'bận rộn', 1, 1),
('time', 'the continued progress of events', 'thời gian', 1, 1),
('family', 'a group of related people', 'gia đình', 1, 1),
('study', 'to learn about a subject', 'học tập', 1, 1),
('sleep', 'to rest by closing your eyes', 'ngủ', 1, 1);

-- Deck 2: Travel & Places
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('airport', 'place where airplanes take off', 'sân bay', 1, 2),
('hotel', 'a place to stay when traveling', 'khách sạn', 1, 2),
('ticket', 'a pass to travel', 'vé', 1, 2),
('map', 'a diagram showing locations', 'bản đồ', 1, 2),
('journey', 'the act of traveling', 'chuyến đi', 1, 2),
('guide', 'a person who shows the way', 'hướng dẫn viên', 1, 2),
('destination', 'place someone is going to', 'điểm đến', 1, 2),
('passport', 'official travel document', 'hộ chiếu', 1, 2),
('beach', 'sandy shore by the sea', 'bãi biển', 1, 2),
('mountain', 'a high natural elevation', 'núi', 1, 2),
('luggage', 'bags used for travel', 'hành lý', 1, 2);

-- Deck 3: Food & Drinks
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('bread', 'baked food made from flour', 'bánh mì', 1, 3),
('water', 'a clear liquid for drinking', 'nước', 1, 3),
('rice', 'a common grain food', 'gạo', 1, 3),
('meat', 'animal flesh used as food', 'thịt', 1, 3),
('vegetable', 'plant used as food', 'rau củ', 1, 3),
('fruit', 'edible part of a plant', 'trái cây', 1, 3),
('soup', 'liquid food', 'súp', 1, 3),
('juice', 'drink made from fruits', 'nước ép', 1, 3),
('milk', 'white liquid from cows', 'sữa', 1, 3),
('tea', 'drink made from tea leaves', 'trà', 1, 3);

-- Deck 4: Technology
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('computer', 'an electronic machine for processing data', 'máy tính', 1, 4),
('internet', 'a global network of computers', 'mạng internet', 1, 4),
('keyboard', 'device for typing', 'bàn phím', 1, 4),
('screen', 'display device', 'màn hình', 1, 4),
('software', 'programs used by a computer', 'phần mềm', 1, 4),
('smartphone', 'a mobile phone with advanced features', 'điện thoại thông minh', 1, 4),
('charger', 'device used to charge batteries', 'bộ sạc', 1, 4),
('camera', 'device used to take photos', 'máy ảnh', 1, 4),
('email', 'electronic mail', 'thư điện tử', 1, 4),
('file', 'a collection of data', 'tệp', 1, 4);

-- Deck 5: Emotions
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('happy', 'feeling good or pleased', 'vui vẻ', 1, 5),
('sad', 'feeling unhappy', 'buồn bã', 1, 5),
('angry', 'feeling strong displeasure', 'tức giận', 1, 5),
('afraid', 'feeling fear', 'sợ hãi', 1, 5),
('excited', 'feeling very happy and eager', 'hào hứng', 1, 5),
('nervous', 'worried about something', 'lo lắng', 1, 5),
('bored', 'feeling uninterested', 'chán nản', 1, 5),
('confident', 'feeling sure of yourself', 'tự tin', 1, 5),
('surprised', 'feeling unexpected emotion', 'ngạc nhiên', 1, 5),
('tired', 'feeling in need of rest', 'mệt mỏi', 1, 5);

-- Deck 6: Nature & Environment
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('tree', 'a tall plant with a trunk', 'cây', 1, 6),
('river', 'large stream of water', 'sông', 1, 6),
('rain', 'water falling from clouds', 'mưa', 1, 6),
('wind', 'moving air', 'gió', 1, 6),
('snow', 'frozen water from clouds', 'tuyết', 1, 6),
('sun', 'the star at the center of the solar system', 'mặt trời', 1, 6),
('moon', 'natural satellite of Earth', 'mặt trăng', 1, 6),
('mountain', 'large natural elevation', 'núi', 1, 6),
('forest', 'large area with many trees', 'khu rừng', 1, 6),
('earth', 'the planet we live on', 'trái đất', 1, 6);

-- Deck 7: Jobs & Careers
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('teacher', 'a person who teaches', 'giáo viên', 1, 7),
('doctor', 'a person who treats sick people', 'bác sĩ', 1, 7),
('engineer', 'a person who designs and builds things', 'kỹ sư', 1, 7),
('nurse', 'a person who cares for patients', 'y tá', 1, 7),
('police', 'a person who enforces laws', 'cảnh sát', 1, 7),
('chef', 'a professional cook', 'đầu bếp', 1, 7),
('driver', 'a person who drives vehicles', 'tài xế', 1, 7),
('farmer', 'a person who grows crops', 'nông dân', 1, 7),
('artist', 'a person who creates art', 'nghệ sĩ', 1, 7),
('scientist', 'a person who studies science', 'nhà khoa học', 1, 7);

-- Deck 8: Health & Body
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('head', 'part of the body with brain', 'đầu', 1, 8),
('eye', 'organ for seeing', 'mắt', 1, 8),
('ear', 'organ for hearing', 'tai', 1, 8),
('mouth', 'opening through which food passes', 'miệng', 1, 8),
('hand', 'part of the arm', 'tay', 1, 8),
('leg', 'used for walking', 'chân', 1, 8),
('heart', 'organ that pumps blood', 'trái tim', 1, 8),
('stomach', 'organ for digesting food', 'dạ dày', 1, 8),
('pain', 'unpleasant feeling', 'cơn đau', 1, 8),
('medicine', 'substance used to treat illness', 'thuốc', 1, 8);

-- Deck 9: Education
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('school', 'a place for learning', 'trường học', 1, 9),
('student', 'a person who studies', 'học sinh', 1, 9),
('teacher', 'person who gives lessons', 'giáo viên', 1, 9),
('subject', 'a branch of knowledge', 'môn học', 1, 9),
('exam', 'a test of knowledge', 'kỳ thi', 1, 9),
('classroom', 'room for teaching', 'phòng học', 1, 9),
('homework', 'work done outside class', 'bài tập về nhà', 1, 9),
('lesson', 'a unit of teaching', 'bài học', 1, 9),
('grade', 'a mark showing quality', 'điểm số', 1, 9),
('university', 'institution of higher education', 'trường đại học', 1, 9);

-- Deck 10: Household Items
INSERT INTO fc.Words (word, word_def, word_meaning, word_status, word_deck_id) VALUES
('chair', 'a seat for one person', 'ghế', 1, 10),
('table', 'a piece of furniture with a flat top', 'bàn', 1, 10),
('lamp', 'device that gives light', 'đèn', 1, 10),
('bed', 'furniture for sleeping', 'giường', 1, 10),
('sofa', 'comfortable seat for several people', 'ghế sofa', 1, 10),
('mirror', 'reflective surface', 'gương', 1, 10),
('clock', 'device that shows time', 'đồng hồ', 1, 10),
('curtain', 'piece of cloth covering a window', 'rèm cửa', 1, 10),
('door', 'entry to a room or building', 'cửa', 1, 10),
('window', 'opening in a wall for light and air', 'cửa sổ', 1, 10);
