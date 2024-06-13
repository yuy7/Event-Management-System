CREATE TABLE `budget` (
  `budgetID` int NOT NULL AUTO_INCREMENT,
  `eventID` int DEFAULT NULL,
  `userID` int DEFAULT NULL,
  `initialBudget` double DEFAULT NULL,
  `actualCost` double DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`budgetID`),
  KEY `budget_event_FK` (`eventID`),
  KEY `budget_user_FK` (`userID`),
  CONSTRAINT `budget_event_FK` FOREIGN KEY (`eventID`) REFERENCES `event` (`EventID`),
  CONSTRAINT `budget_user_FK` FOREIGN KEY (`userID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
SELECT * FROM emsdb.budget;