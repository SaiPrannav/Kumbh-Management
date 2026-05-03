
SET FOREIGN_KEY_CHECKS = 0;

USE kumbhmanagement;

CREATE TABLE Pilgrims (
    Pilgrim_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT,
    Gender ENUM('Male', 'Female', 'Other'),
    Contact_Number VARCHAR(20),
    Email_Address VARCHAR(100),
    Address TEXT,
    Emergency_Contact VARCHAR(20),
    Medical_Condition TEXT
);

CREATE TABLE Hospitals (
    Hospital_ID VARCHAR(50) PRIMARY KEY,
    Hospital_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Number_Of_Available_Beds INT,
    Emergency_Contact_Number VARCHAR(20) NOT NULL,
    Facilities TEXT,
    Specialized_Medical_Services TEXT
);

CREATE TABLE Doctors (
    Doctor_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    Contact_Number VARCHAR(20),
    Hospital_ID VARCHAR(50),
    FOREIGN KEY (Hospital_ID) REFERENCES Hospitals(Hospital_ID)
);

CREATE TABLE Emergency_Response (
    Response_ID VARCHAR(50) PRIMARY KEY,
    Ambulance_Availability BOOLEAN,
    Emergency_Contact_Number VARCHAR(20) NOT NULL,
    Location VARCHAR(255)
);

CREATE TABLE Fire_Stations (
    Fire_Station_ID VARCHAR(50) PRIMARY KEY,
    Fire_Station_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Contact VARCHAR(20) NOT NULL,
    Number_Of_Trucks INT
);

CREATE TABLE Police_Stations (
    Station_ID VARCHAR(50) PRIMARY KEY,
    Station_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Contact_Number VARCHAR(20) NOT NULL,
    Assigned_Area VARCHAR(255)
);

CREATE TABLE Police_Officers (
    Officer_ID VARCHAR(50) PRIMARY KEY,
    Officer_Name VARCHAR(100) NOT NULL,
    Rank VARCHAR(50),
    Contact_Number VARCHAR(20),
    Shift_Timings VARCHAR(100),
    Station_ID VARCHAR(50),
    FOREIGN KEY (Station_ID) REFERENCES Police_Stations(Station_ID)
);

CREATE TABLE Ghats (
    Ghat_ID VARCHAR(50) PRIMARY KEY,
    Ghat_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Royal_Bath_Timings VARCHAR(100),
    Number_Of_Lifeguards INT,
    Safety_Measures TEXT,
    Emergency_Contact VARCHAR(20) NOT NULL
);

CREATE TABLE Accommodation (
    Tent_ID VARCHAR(50) PRIMARY KEY,
    Tent_Name VARCHAR(100),
    Location VARCHAR(255) NOT NULL,
    Capacity INT,
    Availability BOOLEAN,
    Contact_For_Booking VARCHAR(20) NOT NULL
);

CREATE TABLE Vendors (
    Vendor_ID VARCHAR(50) PRIMARY KEY,
    Vendor_Name VARCHAR(100) NOT NULL,
    Stall_Type VARCHAR(100),
    Location VARCHAR(255),
    Contact_Number VARCHAR(20),
    Operating_Hours VARCHAR(100),
    License_Status ENUM('Active', 'Pending', 'Suspended', 'Expired')
);

CREATE TABLE Transportation (
    Transport_ID VARCHAR(50) PRIMARY KEY,
    Transport_Type VARCHAR(50) NOT NULL,
    Operator_Name VARCHAR(100),
    Route_Information TEXT,
    Departure_And_Arrival_Timings TEXT,
    Contact_Information VARCHAR(20),
    Emergency_Services BOOLEAN
);

CREATE TABLE Lost_And_Found (
    Lost_Item_Person_ID VARCHAR(50) PRIMARY KEY,
    Description TEXT NOT NULL,
    Date_Time DATETIME NOT NULL,
    Reported_By VARCHAR(100),
    Availability BOOLEAN,
    Claim_Status ENUM('Unclaimed', 'Claimed'),
    Location VARCHAR(255)
);

CREATE TABLE Incident_Reports (
    Incident_ID VARCHAR(50) PRIMARY KEY,
    Incident_Type VARCHAR(100) NOT NULL,
    Date_Time DATETIME NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Reported_By VARCHAR(100),
    Status ENUM('Reported', 'In Progress', 'Resolved', 'Closed'),
    Assigned_Authority VARCHAR(100)
);

CREATE TABLE Pilgrim_Accommodation (
    Pilgrim_ID VARCHAR(50),
    Tent_ID VARCHAR(50),
    Check_In_Date DATE,
    Check_Out_Date DATE,
    PRIMARY KEY (Pilgrim_ID, Tent_ID),
    FOREIGN KEY (Pilgrim_ID) REFERENCES Pilgrims(Pilgrim_ID),
    FOREIGN KEY (Tent_ID) REFERENCES Accommodation(Tent_ID)
);

CREATE TABLE Pilgrim_Transportation (
    Pilgrim_ID VARCHAR(50),
    Transport_ID VARCHAR(50),
    Travel_Date DATETIME,
    PRIMARY KEY (Pilgrim_ID, Transport_ID, Travel_Date),
    FOREIGN KEY (Pilgrim_ID) REFERENCES Pilgrims(Pilgrim_ID),
    FOREIGN KEY (Transport_ID) REFERENCES Transportation(Transport_ID)
);

CREATE TABLE Pilgrim_Incidents (
    Pilgrim_ID VARCHAR(50),
    Incident_ID VARCHAR(50),
    PRIMARY KEY (Pilgrim_ID, Incident_ID),
    FOREIGN KEY (Pilgrim_ID) REFERENCES Pilgrims(Pilgrim_ID),
    FOREIGN KEY (Incident_ID) REFERENCES Incident_Reports(Incident_ID)
);

CREATE TABLE Pilgrim_Purchases (
    Pilgrim_ID VARCHAR(50),
    Vendor_ID VARCHAR(50),
    Purchase_Date DATETIME,
    Item_Description TEXT,
    PRIMARY KEY (Pilgrim_ID, Vendor_ID, Purchase_Date),
    FOREIGN KEY (Pilgrim_ID) REFERENCES Pilgrims(Pilgrim_ID),
    FOREIGN KEY (Vendor_ID) REFERENCES Vendors(Vendor_ID)
);

CREATE TABLE Pilgrim_Treatments (
    Pilgrim_ID VARCHAR(50),
    Hospital_ID VARCHAR(50),
    Doctor_ID VARCHAR(50),
    Treatment_Date DATETIME,
    Diagnosis TEXT,
    Treatment TEXT,
    PRIMARY KEY (Pilgrim_ID, Hospital_ID, Treatment_Date),
    FOREIGN KEY (Pilgrim_ID) REFERENCES Pilgrims(Pilgrim_ID),
    FOREIGN KEY (Hospital_ID) REFERENCES Hospitals(Hospital_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctors(Doctor_ID)
);

CREATE TABLE Management_Hierarchy (
    Manager_ID VARCHAR(50),
    Subordinate_ID VARCHAR(50),
    Role VARCHAR(100),
    PRIMARY KEY (Manager_ID, Subordinate_ID),
    FOREIGN KEY (Manager_ID) REFERENCES Police_Officers(Officer_ID),
    FOREIGN KEY (Subordinate_ID) REFERENCES Police_Officers(Officer_ID)
);

SET FOREIGN_KEY_CHECKS = 1;