DROP TABLE IF EXISTS `eventFeedback`;

CREATE TABLE `eventFeedback` (
    `id` int NOT NULL AUTO_INCREMENT,
    `userID` int NOT NULL,
    `eventID` int NOT NULL,
    `feedback` varchar(1000) NOT NULL
)