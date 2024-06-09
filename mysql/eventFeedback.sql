DROP TABLE IF EXISTS `eventFeedback`;

CREATE TABLE `eventFeedback` (
    `feedbackId` int NOT NULL AUTO_INCREMENT,
    `userID` int NOT NULL,
    `eventID` int NOT NULL,
    `feedback` varchar(1000) NOT NULL,
    `feedbackTime` TIMESTAMP,
    PRIMARY KEY (`feedbackId`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;