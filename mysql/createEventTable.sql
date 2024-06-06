DROP TABLE IF EXISTS `event`;

CREATE TABLE `event` (
  `eventID` INT NOT NULL AUTO_INCREMENT,
  `eventName` VARCHAR(45) NOT NULL,
  `date` VARCHAR(10) NOT NULL,
  `reservationUserId` INT NOT NULL,
  `eventTypeID` INT NOT NULL,
  `numberOfPeople` INT NOT NULL,
  `preferredLocation` VARCHAR(100) NOT NULL,
  `arrangedLocation` VARCHAR(100),
  `requireApproval` tinyint(1) DEFAULT '0',
  `time` INT NOT NULL,
  PRIMARY KEY (`eventID`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

