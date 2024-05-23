DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `locationId` INT NOT NULL AUTO_INCREMENT,
  `number` INT NOT NULL,
  `building` INT NOT NULL,
  `capacity` INT NOT NULL,
  `type` INT NOT NULL,
  `occupy` VARCHAR(45) NOT NULL,
  PRIMARY KEY(`locationId`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO location (`number`, `building`, `capacity`, `type`, `occupy`) VALUES
(101, 1, 100, 1, '03FFFFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF'),
(102, 1, 100, 1, '03FFFFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF'),
(103, 1, 100, 1, '03FFFFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF');
