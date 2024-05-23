DROP TABLE IF EXISTS `tempevent`;

CREATE TABLE `tempevent` (
  `eventID` INT NOT NULL AUTO_INCREMENT,
  `eventName` VARCHAR(45) NOT NULL,
  `date` VARCHAR(10) NOT NULL,
  `reservationUserId` VARCHAR(8) NOT NULL,
  `eventTypeID` INT NOT NULL,
  `numberOfPeople` INT NOT NULL,
  `preferredLocation` VARCHAR(100) NOT NULL,
  `time` INT NOT NULL,
  PRIMARY KEY (`eventID`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO tempevent (`eventName`, `date`, `reservationUserId`, `eventTypeID`, `numberOfPeople`, `preferredLocation`, `time`) VALUES
('Event A', '2024-05-27', '001', 1, 100, 'Location 1', 0),
('Event B', '2024-05-27', '002', 2, 50, 'Location 2', 1),
('Event C', '2024-05-27', '003', 3, 200, 'Location 3', 1),
('Event D', '2024-05-27', '004', 4, 30, 'Location 4', 1),
('Event E', '2024-05-27', '005', 5, 150, 'Location 5', 1),
('Event F', '2024-05-28', '006', 1, 120, 'Location 1', 2),
('Event G', '2024-05-28', '007', 2, 60, 'Location 2', 2),
('Event H', '2024-05-28', '008', 3, 250, 'Location 3', 2),
('Event I', '2024-05-28', '009', 4, 35, 'Location 4', 3),
('Event J', '2024-05-28', '010', 5, 160, 'Location 5', 4);
