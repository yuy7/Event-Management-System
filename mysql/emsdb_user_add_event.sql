CREATE TABLE `event` (
  `eventID` int NOT NULL AUTO_INCREMENT,
  `eventName` varchar(45) NOT NULL,
  `date` varchar(10) NOT NULL,
  `reservationUserId` int NOT NULL,
  `eventTypeID` int NOT NULL,
  `numberOfPeople` int NOT NULL,
  `preferredLocation` varchar(100) NOT NULL,
  `arrangedLocation` varchar(100) DEFAULT NULL,
  `requireApproval` tinyint(1) DEFAULT '0',
  `time` int NOT NULL,
  PRIMARY KEY (`eventID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
SELECT * FROM emsdb.event;CREATE TABLE `user_add_event` (
  `userID` int NOT NULL,
  `eventID` int NOT NULL,
  `state` tinyint(1) NOT NULL,
  PRIMARY KEY (`userID`,`eventID`),
  KEY `eventID` (`eventID`),
  CONSTRAINT `user__add_event_ibfk_2` FOREIGN KEY (`eventID`) REFERENCES `event` (`eventID`),
  CONSTRAINT `user_add_event_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
