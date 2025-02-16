CREATE DATABASE IF NOT EXISTS vscanner;
USE vscanner;

CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    UserName VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ScanProfile (
    ProfileID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ScanFrequency INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS NetworkDevice (
    DeviceID INT PRIMARY KEY AUTO_INCREMENT,
    DeviceName VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    IPaddress VARCHAR(15) NOT NULL,
    UNIQUE(IPaddress)
);

CREATE TABLE IF NOT EXISTS ScanProfileDevices (
    ProfileID INT,
    DeviceID INT,
    PRIMARY KEY (ProfileID, DeviceID),
    FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID),
    FOREIGN KEY (DeviceID) REFERENCES NetworkDevice(DeviceID)
);

CREATE TABLE IF NOT EXISTS Vulnerabilities (
    VulnerabilityID INT PRIMARY KEY AUTO_INCREMENT,
    CVE_ID VARCHAR(20) NOT NULL,
    Description TEXT NOT NULL,
    SeverityLevel VARCHAR(50) NOT NULL,
    UNIQUE(CVE_ID)
);

CREATE TABLE IF NOT EXISTS ScanResult (
    ResultID INT PRIMARY KEY AUTO_INCREMENT,
    ProfileID INT,
    ScanDate DATE NOT NULL,
    Result VARCHAR(50000) NOT NULL,
    FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID)
);

CREATE TABLE IF NOT EXISTS ScanProfileVulnerabilities (
    ProfileID INT,
    VulnerabilityID INT,
    PRIMARY KEY (ProfileID, VulnerabilityID),
    FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID),
    FOREIGN KEY (VulnerabilityID) REFERENCES Vulnerabilities(VulnerabilityID)
);

INSERT INTO users (UserName, Password, Role) VALUES ('admin', '$2b$12$LjF//9Csfgd1bF86Xfe4FOydezWNXOflvCbHTT2xrQZVL8ktaCFoe', 'admin')
