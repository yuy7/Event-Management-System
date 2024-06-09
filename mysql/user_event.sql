CREATE TABLE `user_event` (
  `userEventID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `eventID` int NOT NULL,
  PRIMARY KEY (`userEventID`),
  KEY `user_FK_idx` (`userID`),
  KEY `event_FK_idx` (`eventID`),
  CONSTRAINT `event_FK` FOREIGN KEY (`eventID`) REFERENCES `event` (`eventID`),
  CONSTRAINT `user_FK` FOREIGN KEY (`userID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
SELECT * FROM emsdb.user_add_event;