CREATE TABLE `budgetapp` (
  `BudgetAppID` int NOT NULL AUTO_INCREMENT,
  `cost` double DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `userID` int DEFAULT NULL,
  `eventID` int DEFAULT NULL,
  PRIMARY KEY (`BudgetAppID`),
  KEY `eventID_idx` (`eventID`),
  KEY `userID_idx` (`userID`),
  CONSTRAINT `eventID` FOREIGN KEY (`eventID`) REFERENCES `event` (`eventID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
SELECT * FROM emsdb.budgetapp;