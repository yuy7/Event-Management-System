CREATE TABLE `event` (
  `EventID` int NOT NULL AUTO_INCREMENT,
  `EventName` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `EventDate` timestamp NOT NULL,
  `EventLocation` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `EventTypeID` int NOT NULL,
  PRIMARY KEY (`EventID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `permission` (
  `PermissionID` int NOT NULL AUTO_INCREMENT,
  `PermissionName` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`PermissionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `role` (
  `RoleID` int NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `rolepermission` (
  `RolePermissionID` int NOT NULL AUTO_INCREMENT,
  `RoleID` int DEFAULT NULL,
  `PermissionID` int DEFAULT NULL,
  PRIMARY KEY (`RolePermissionID`),
  KEY `RoleID` (`RoleID`),
  KEY `PermissionID` (`PermissionID`),
  CONSTRAINT `rolepermission_ibfk_1` FOREIGN KEY (`RoleID`) REFERENCES `role` (`RoleID`),
  CONSTRAINT `rolepermission_ibfk_2` FOREIGN KEY (`PermissionID`) REFERENCES `permission` (`PermissionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `user` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Password` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `Email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `PhoneNumber` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Role` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `VerificationCode` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `RegistrationTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `LastLoginTime` timestamp NULL DEFAULT NULL,
  `AccountStatus` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=251101164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;