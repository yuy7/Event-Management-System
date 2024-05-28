CREATE TABLE TimeSlot (
    timeID INT PRIMARY KEY AUTO_INCREMENT,
    timeDescription VARCHAR(100) NOT NULL
);
INSERT INTO TimeSlot (timeID, timeDescription) VALUES 
(1, '8:00-9:35'),
(2, '9:55-11:30'),
(3, '13:30-15:05'),
(4, '15:20-16:55'),
(5, '17:05-18:45'),
(6, '19:30-21:05');
