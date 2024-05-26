DROP TABLE IF EXISTS `tempevent`;

CREATE TABLE `tempevent` (
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

INSERT INTO `tempevent` VALUES ('1', 'Event A', '2024-05-27', '1', '1', '100', '逸夫楼101', '逸夫楼101', '0', '0');
INSERT INTO `tempevent` VALUES ('2', 'Event B', '2024-05-27', '2', '2', '50', '逸夫楼101', '逸夫楼101', '0', '1');
INSERT INTO `tempevent` VALUES ('3', 'Event C', '2024-05-27', '3', '3', '200', '逸夫楼101', null, '0', '1');
INSERT INTO `tempevent` VALUES ('4', 'Event D', '2024-05-27', '1', '4', '30', '逸夫楼101', null, '0', '1');
INSERT INTO `tempevent` VALUES ('5', 'Event E', '2024-05-27', '3', '5', '150', '逸夫楼102', '逸夫楼102', '0', '1');
INSERT INTO `tempevent` VALUES ('6', 'Event F', '2024-05-28', '2', '1', '120', '逸夫楼102', '逸夫楼102', '0', '2');
INSERT INTO `tempevent` VALUES ('7', 'Event G', '2024-05-28', '1', '2', '60', '逸夫楼102', null, '0', '2');
INSERT INTO `tempevent` VALUES ('8', 'Event H', '2024-05-28', '2', '3', '250', '逸夫楼103', '逸夫楼103', '0', '2');
INSERT INTO `tempevent` VALUES ('9', 'Event I', '2024-05-28', '3', '4', '35', '逸夫楼103', '逸夫楼103', '0', '3');
INSERT INTO `tempevent` VALUES ('10', 'Event J', '2024-05-28', '1', '5', '160', '逸夫楼103', '逸夫楼103', '0', '4');
