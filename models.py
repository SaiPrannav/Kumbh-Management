from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

from sqlalchemy import Column, String, Integer, Text, Boolean, Enum, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Authorities(Base):
    __tablename__ = 'Authorities'

    User_ID = Column(Integer, primary_key=True)
    Username = Column(String(50))
    hash_pwd = Column(String(255))

class Pilgrim(Base):
    __tablename__ = 'Pilgrims'
    
    Pilgrim_ID = Column(String(50), primary_key=True)
    Name = Column(String(100), nullable=False)
    Age = Column(Integer)
    Gender = Column(Enum('Male', 'Female', 'Other'))
    Contact_Number = Column(String(20))
    Email_Address = Column(String(100))
    Address = Column(Text)
    Emergency_Contact = Column(String(20))
    Medical_Condition = Column(Text)
    
    # Relationships
    accommodations = relationship("PilgrimAccommodation", back_populates="pilgrim")
    transportation = relationship("PilgrimTransportation", back_populates="pilgrim")
    incidents = relationship("PilgrimIncident", back_populates="pilgrim")
    purchases = relationship("PilgrimPurchase", back_populates="pilgrim")
    treatments = relationship("PilgrimTreatment", back_populates="pilgrim")


class Hospital(Base):
    __tablename__ = 'Hospitals'
    
    Hospital_ID = Column(String(50), primary_key=True)
    Hospital_Name = Column(String(100), nullable=False)
    Location = Column(String(255), nullable=False)
    Number_Of_Available_Beds = Column(Integer)
    Emergency_Contact_Number = Column(String(20), nullable=False)
    Facilities = Column(Text)
    Specialized_Medical_Services = Column(Text)
    
    # Relationships
    doctors = relationship("Doctor", back_populates="hospital")
    treatments = relationship("PilgrimTreatment", back_populates="hospital")


class Doctor(Base):
    __tablename__ = 'Doctors'
    
    Doctor_ID = Column(String(50), primary_key=True)
    Name = Column(String(100), nullable=False)
    Specialization = Column(String(100))
    Contact_Number = Column(String(20))
    Hospital_ID = Column(String(50), ForeignKey('Hospitals.Hospital_ID'))
    
    # Relationships
    hospital = relationship("Hospital", back_populates="doctors")
    treatments = relationship("PilgrimTreatment", back_populates="doctor")


class EmergencyResponse(Base):
    __tablename__ = 'Emergency_Response'
    
    Response_ID = Column(String(50), primary_key=True)
    Ambulance_Availability = Column(Boolean)
    Emergency_Contact_Number = Column(String(20), nullable=False)
    Location = Column(String(255))


class FireStation(Base):
    __tablename__ = 'Fire_Stations'
    
    Fire_Station_ID = Column(String(50), primary_key=True)
    Fire_Station_Name = Column(String(100), nullable=False)
    Location = Column(String(255), nullable=False)
    Contact = Column(String(20), nullable=False)
    Number_Of_Trucks = Column(Integer)


class PoliceStation(Base):
    __tablename__ = 'Police_Stations'
    
    Station_ID = Column(String(50), primary_key=True)
    Station_Name = Column(String(100), nullable=False)
    Location = Column(String(255), nullable=False)
    Contact_Number = Column(String(20), nullable=False)
    Assigned_Area = Column(String(255))
    
    # Relationships
    officers = relationship("PoliceOfficer", back_populates="station")


class PoliceOfficer(Base):
    __tablename__ = 'Police_Officers'
    
    Officer_ID = Column(String(50), primary_key=True)
    Officer_Name = Column(String(100), nullable=False)
    Rank = Column(String(50))
    Contact_Number = Column(String(20))
    Shift_Timings = Column(String(100))
    Station_ID = Column(String(50), ForeignKey('Police_Stations.Station_ID'))
    
    # Relationships
    station = relationship("PoliceStation", back_populates="officers")
    managers = relationship("ManagementHierarchy", foreign_keys="ManagementHierarchy.Subordinate_ID", back_populates="subordinate")
    subordinates = relationship("ManagementHierarchy", foreign_keys="ManagementHierarchy.Manager_ID", back_populates="manager")


class Ghat(Base):
    __tablename__ = 'Ghats'
    
    Ghat_ID = Column(String(50), primary_key=True)
    Ghat_Name = Column(String(100), nullable=False)
    Location = Column(String(255), nullable=False)
    Royal_Bath_Timings = Column(String(100))
    Number_Of_Lifeguards = Column(Integer)
    Safety_Measures = Column(Text)
    Emergency_Contact = Column(String(20), nullable=False)


class Accommodation(Base):
    __tablename__ = 'Accommodation'
    
    Tent_ID = Column(String(50), primary_key=True)
    Tent_Name = Column(String(100))
    Location = Column(String(255), nullable=False)
    Capacity = Column(Integer)
    Availability = Column(Boolean)
    Contact_For_Booking = Column(String(20), nullable=False)
    
    # Relationships
    pilgrim_accommodations = relationship("PilgrimAccommodation", back_populates="accommodation")


class Vendor(Base):
    __tablename__ = 'Vendors'
    
    Vendor_ID = Column(String(50), primary_key=True)
    Vendor_Name = Column(String(100), nullable=False)
    Stall_Type = Column(String(100))
    Location = Column(String(255))
    Contact_Number = Column(String(20))
    Operating_Hours = Column(String(100))
    License_Status = Column(Enum('Active', 'Pending', 'Suspended', 'Expired'))
    
    # Relationships
    purchases = relationship("PilgrimPurchase", back_populates="vendor")


class Transportation(Base):
    __tablename__ = 'Transportation'
    
    Transport_ID = Column(String(50), primary_key=True)
    Transport_Type = Column(String(50), nullable=False)
    Operator_Name = Column(String(100))
    Route_Information = Column(Text)
    Departure_And_Arrival_Timings = Column(Text)
    Contact_Information = Column(String(20))
    Emergency_Services = Column(Boolean)
    
    # Relationships
    pilgrim_transportation = relationship("PilgrimTransportation", back_populates="transportation")


class LostAndFound(Base):
    __tablename__ = 'Lost_And_Found'
    
    Lost_Item_Person_ID = Column(String(50), primary_key=True)
    Description = Column(Text, nullable=False)
    Date_Time = Column(DateTime, nullable=False)
    Reported_By = Column(String(100))
    Availability = Column(Boolean)
    Claim_Status = Column(Enum('Unclaimed', 'Claimed'))
    Location = Column(String(255))


class IncidentReport(Base):
    __tablename__ = 'Incident_Reports'
    
    Incident_ID = Column(String(50), primary_key=True)
    Incident_Type = Column(String(100), nullable=False)
    Date_Time = Column(DateTime, nullable=False)
    Location = Column(String(255), nullable=False)
    Reported_By = Column(String(100))
    Status = Column(Enum('Reported', 'In Progress', 'Resolved', 'Closed'))
    Assigned_Authority = Column(String(100))
    
    # Relationships
    pilgrim_incidents = relationship("PilgrimIncident", back_populates="incident")


class PilgrimAccommodation(Base):
    __tablename__ = 'Pilgrim_Accommodation'
    
    Pilgrim_ID = Column(String(50), ForeignKey('Pilgrims.Pilgrim_ID'), primary_key=True)
    Tent_ID = Column(String(50), ForeignKey('Accommodation.Tent_ID'), primary_key=True)
    Check_In_Date = Column(Date)
    Check_Out_Date = Column(Date)
    
    # Relationships
    pilgrim = relationship("Pilgrim", back_populates="accommodations")
    accommodation = relationship("Accommodation", back_populates="pilgrim_accommodations")


class PilgrimTransportation(Base):
    __tablename__ = 'Pilgrim_Transportation'
    
    Pilgrim_ID = Column(String(50), ForeignKey('Pilgrims.Pilgrim_ID'), primary_key=True)
    Transport_ID = Column(String(50), ForeignKey('Transportation.Transport_ID'), primary_key=True)
    Travel_Date = Column(DateTime, primary_key=True)
    
    # Relationships
    pilgrim = relationship("Pilgrim", back_populates="transportation")
    transportation = relationship("Transportation", back_populates="pilgrim_transportation")


class PilgrimIncident(Base):
    __tablename__ = 'Pilgrim_Incidents'
    
    Pilgrim_ID = Column(String(50), ForeignKey('Pilgrims.Pilgrim_ID'), primary_key=True)
    Incident_ID = Column(String(50), ForeignKey('Incident_Reports.Incident_ID'), primary_key=True)
    
    # Relationships
    pilgrim = relationship("Pilgrim", back_populates="incidents")
    incident = relationship("IncidentReport", back_populates="pilgrim_incidents")


class PilgrimPurchase(Base):
    __tablename__ = 'Pilgrim_Purchases'
    
    Pilgrim_ID = Column(String(50), ForeignKey('Pilgrims.Pilgrim_ID'), primary_key=True)
    Vendor_ID = Column(String(50), ForeignKey('Vendors.Vendor_ID'), primary_key=True)
    Purchase_Date = Column(DateTime, primary_key=True)
    Item_Description = Column(Text)
    
    # Relationships
    pilgrim = relationship("Pilgrim", back_populates="purchases")
    vendor = relationship("Vendor", back_populates="purchases")


class PilgrimTreatment(Base):
    __tablename__ = 'Pilgrim_Treatments'
    
    Pilgrim_ID = Column(String(50), ForeignKey('Pilgrims.Pilgrim_ID'), primary_key=True)
    Hospital_ID = Column(String(50), ForeignKey('Hospitals.Hospital_ID'), primary_key=True)
    Doctor_ID = Column(String(50), ForeignKey('Doctors.Doctor_ID'))
    Treatment_Date = Column(DateTime, primary_key=True)
    Diagnosis = Column(Text)
    Treatment = Column(Text)
    
    # Relationships
    pilgrim = relationship("Pilgrim", back_populates="treatments")
    hospital = relationship("Hospital", back_populates="treatments")
    doctor = relationship("Doctor", back_populates="treatments")


class ManagementHierarchy(Base):
    __tablename__ = 'Management_Hierarchy'
    
    Manager_ID = Column(String(50), ForeignKey('Police_Officers.Officer_ID'), primary_key=True)
    Subordinate_ID = Column(String(50), ForeignKey('Police_Officers.Officer_ID'), primary_key=True)
    Role = Column(String(100))
    
    # Relationships
    manager = relationship("PoliceOfficer", foreign_keys=[Manager_ID], back_populates="subordinates")
    subordinate = relationship("PoliceOfficer", foreign_keys=[Subordinate_ID], back_populates="managers")