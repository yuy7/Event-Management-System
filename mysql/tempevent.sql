DROP TABLE IF EXISTS `tempevent`;

CREATE TABLE `tempevent` (
  `eventID` int NOT NULL AUTO_INCREMENT,
  `eventName` varchar(45) NOT NULL,
  `week` int NOT NULL,
  `day` int NOT NULL,
  `reservationUserId` varchar(8) NOT NULL,
  `eventType` int NOT NULL,
  `numberOfPeople` INT NOT NULL,
  `preferredLocation` VARCHAR(100) NOT NULL,
  `reservationTimeSlots` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`eventID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `tempevent` (`eventName`, `week`, `day`, `reservationUserId`, `eventType`, `numberOfPeople`, `preferredLocation`, `reservationTimeSlots`)
VALUES ('考试', 1, 3, 'U1234567', 0, 100, '逸夫楼101', '0, 1, 2');