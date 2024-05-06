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
