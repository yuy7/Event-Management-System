DROP TABLE IF EXISTS `user_add_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_add_event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `eventID` int NOT NULL,
  `state` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eventID` (`eventID`),
  CONSTRAINT `user_add_event_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `user` (`UserID`),
  CONSTRAINT `user__add_event_ibfk_2` FOREIGN KEY (`eventID`) REFERENCES `event` (`eventID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

