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
    IPaddress VARCHAR(15) NOT NULL
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
    SeverityLevel VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ScanResult (
    ResultID INT PRIMARY KEY AUTO_INCREMENT,
    ScanDate DATE NOT NULL,
    CriticalVulnerabilities INT NOT NULL,
    TotalVulnerabilities INT NOT NULL
);

CREATE TABLE IF NOT EXISTS VulnerabilitiesInScanResult (
    ResultID INT,
    VulnerabilityID INT,
    PRIMARY KEY (ResultID, VulnerabilityID),
    FOREIGN KEY (ResultID) REFERENCES ScanResult(ResultID),
    FOREIGN KEY (VulnerabilityID) REFERENCES vulnerabilities(VulnerabilityID)
);

CREATE TABLE IF NOT EXISTS ScanProfileVulnerabilities (
    ProfileID INT,
    VulnerabilityID INT,
    PRIMARY KEY (ProfileID, VulnerabilityID),
    FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (VulnerabilityID) REFERENCES Vulnerabilities(VulnerabilityID) ON DELETE CASCADE ON UPDATE CASCADE
);
