DROP DATABASE IF EXISTS `emsdb`;
CREATE DATABASE `emsdb`;
USE `emsdb`;

SET FOREIGN_KEY_CHECKS=0;
set character_set_database=utf8;
set character_set_server=utf8;

CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20),
    Role VARCHAR(50),
    VerificationCode VARCHAR(20),
    RegistrationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LastLoginTime TIMESTAMP,
    AccountStatus VARCHAR(20)
);
CREATE TABLE Role (
    RoleID INT PRIMARY KEY AUTO_INCREMENT,
    RoleName VARCHAR(50) NOT NULL
);
CREATE TABLE Permission (
    PermissionID INT PRIMARY KEY AUTO_INCREMENT,
    PermissionName VARCHAR(50) NOT NULL
);
CREATE TABLE RolePermission (
    RolePermissionID INT PRIMARY KEY AUTO_INCREMENT,
    RoleID INT,
    PermissionID INT,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID),
    FOREIGN KEY (PermissionID) REFERENCES Permission(PermissionID)
);
CREATE TABLE `emsdb`.`event` (
  `EventID` INT NOT NULL AUTO_INCREMENT,
  `EventName` VARCHAR(45) NOT NULL,
  `EventDate` TIMESTAMP NOT NULL,
  `EventLocation` VARCHAR(45) NOT NULL,
  `EventTypeID` INT NOT NULL,
  PRIMARY KEY (`EventID`));

INSERT INTO User
(UserID, Username, Password, Email, PhoneNumber, Role, VerificationCode, RegistrationTime, LastLoginTime, AccountStatus)
VALUES
(251101163, 'yuyan2003', '123456', '2511011639@qq.com', '18067262965', '0', '123456', '2024-05-07 16:14:37', '2024-05-07 15:00:52', '123456');