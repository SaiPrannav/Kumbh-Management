from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# Enum definitions
class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class LicenseStatusEnum(str, Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    SUSPENDED = "Suspended"
    EXPIRED = "Expired"


class ClaimStatusEnum(str, Enum):
    UNCLAIMED = "Unclaimed"
    CLAIMED = "Claimed"


class IncidentStatusEnum(str, Enum):
    Ongoing = "Ongoing"
    Pending = "Pending"
    Resolved = "Resolved"


# Base Models (for shared fields)

class RegisterInput(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    password: str

class PilgrimBase(BaseModel):
    Name: str
    Age: Optional[int] = None
    Gender: Optional[GenderEnum] = None
    Contact_Number: Optional[str] = None
    Email_Address: Optional[str] = None
    Address: Optional[str] = None
    Emergency_Contact: Optional[str] = None
    Medical_Condition: Optional[str] = None


class HospitalBase(BaseModel):
    Hospital_Name: str
    Location: str
    Number_Of_Available_Beds: Optional[int] = None
    Emergency_Contact_Number: str
    Facilities: Optional[str] = None
    Specialized_Medical_Services: Optional[str] = None


class DoctorBase(BaseModel):
    Name: str
    Specialization: Optional[str] = None
    Contact_Number: Optional[str] = None
    Hospital_ID: Optional[str] = None


class EmergencyResponseBase(BaseModel):
    Ambulance_Availability: Optional[bool] = None
    Emergency_Contact_Number: str
    Location: Optional[str] = None

class HealthcareDataResponse(BaseModel):
    hospitals: List[HospitalBase]
    doctors: List[DoctorBase]
    emergency_responses: List[EmergencyResponseBase]

class FireStationBase(BaseModel):
    Fire_Station_ID: str
    Fire_Station_Name: str
    Location: str
    Contact: str
    Number_Of_Trucks: Optional[int] = None


class PoliceStationBase(BaseModel):
    Station_Name: str
    Location: str
    Contact_Number: str
    Assigned_Area: Optional[str] = None


class PoliceOfficerBase(BaseModel):
    Officer_Name: str
    Rank: Optional[str] = None
    Contact_Number: Optional[str] = None
    Shift_Timings: Optional[str] = None
    Station_ID: Optional[str] = None


class GhatBase(BaseModel):
    Ghat_Name: str
    Location: str
    Royal_Bath_Timings: Optional[str] = None
    Number_Of_Lifeguards: Optional[int] = None
    Safety_Measures: Optional[str] = None
    Emergency_Contact: str


class AccommodationBase(BaseModel):
    Tent_Name: Optional[str] = None
    Location: str
    Capacity: Optional[int] = None
    Availability: Optional[bool] = None
    Contact_For_Booking: str


class VendorBase(BaseModel):
    Vendor_Name: str
    Stall_Type: Optional[str] = None
    Location: Optional[str] = None
    Contact_Number: Optional[str] = None
    Operating_Hours: Optional[str] = None
    License_Status: Optional[LicenseStatusEnum] = None


class TransportationBase(BaseModel):
    Transport_Type: str
    Operator_Name: Optional[str] = None
    Route_Information: Optional[str] = None
    Departure_And_Arrival_Timings: Optional[str] = None
    Contact_Information: Optional[str] = None
    Emergency_Services: Optional[bool] = None


class LostAndFoundBase(BaseModel):
    Description: str
    Date_Time: datetime
    Reported_By: Optional[str] = None
    Availability: Optional[bool] = None
    Claim_Status: Optional[ClaimStatusEnum] = None
    Location: Optional[str] = None


class IncidentReportBase(BaseModel):
    Incident_Type: str
    Date_Time: datetime
    Location: str
    Reported_By: Optional[str] = None
    Status: Optional[IncidentStatusEnum] = None
    Assigned_Authority: Optional[str] = None


class PilgrimAccommodationBase(BaseModel):
    Pilgrim_ID: str
    Tent_ID: str
    Check_In_Date: Optional[date] = None
    Check_Out_Date: Optional[date] = None


class PilgrimTransportationBase(BaseModel):
    Pilgrim_ID: str
    Transport_ID: str
    Travel_Date: datetime


class PilgrimIncidentBase(BaseModel):
    Pilgrim_ID: str
    Incident_ID: str


class PilgrimPurchaseBase(BaseModel):
    Pilgrim_ID: str
    Vendor_ID: str
    Purchase_Date: datetime
    Item_Description: Optional[str] = None


class PilgrimTreatmentBase(BaseModel):
    Pilgrim_ID: str
    Hospital_ID: str
    Doctor_ID: Optional[str] = None
    Treatment_Date: datetime
    Diagnosis: Optional[str] = None
    Treatment: Optional[str] = None


class ManagementHierarchyBase(BaseModel):
    Manager_ID: str
    Subordinate_ID: str
    Role: Optional[str] = None


# Create Models (for request body when creating resources)
class PilgrimCreate(PilgrimBase):
    Pilgrim_ID: str


class HospitalCreate(HospitalBase):
    Hospital_ID: str


class DoctorCreate(DoctorBase):
    Doctor_ID: str


class EmergencyResponseCreate(EmergencyResponseBase):
    Response_ID: str


class FireStationCreate(FireStationBase):
    Fire_Station_ID: str


class PoliceStationCreate(PoliceStationBase):
    Station_ID: str


class PoliceOfficerCreate(PoliceOfficerBase):
    Officer_ID: str


class GhatCreate(GhatBase):
    Ghat_ID: str


class AccommodationCreate(AccommodationBase):
    Tent_ID: str


class VendorCreate(VendorBase):
    Vendor_ID: str


class TransportationCreate(TransportationBase):
    Transport_ID: str


class LostAndFoundCreate(LostAndFoundBase):
    Lost_Item_Person_ID: str


class IncidentReportCreate(IncidentReportBase):
    Incident_ID: str


class PilgrimAccommodationCreate(PilgrimAccommodationBase):
    pass


class PilgrimTransportationCreate(PilgrimTransportationBase):
    pass


class PilgrimIncidentCreate(PilgrimIncidentBase):
    pass


class PilgrimPurchaseCreate(PilgrimPurchaseBase):
    pass


class PilgrimTreatmentCreate(PilgrimTreatmentBase):
    pass


class ManagementHierarchyCreate(ManagementHierarchyBase):
    pass


# Response Models (for API responses)
class Pilgrim(PilgrimBase):
    Pilgrim_ID: str

    class Config:
        orm_mode = True


class Hospital(HospitalBase):
    Hospital_ID: str

    class Config:
        orm_mode = True


class Doctor(DoctorBase):
    Doctor_ID: str

    class Config:
        orm_mode = True


class EmergencyResponse(EmergencyResponseBase):
    Response_ID: str

    class Config:
        orm_mode = True


class FireStation(FireStationBase):
    Fire_Station_ID: str

    class Config:
        orm_mode = True


class PoliceStation(PoliceStationBase):
    Station_ID: str

    class Config:
        orm_mode = True


class PoliceOfficer(PoliceOfficerBase):
    Officer_ID: str

    class Config:
        orm_mode = True


class Ghat(GhatBase):
    Ghat_ID: str

    class Config:
        orm_mode = True


class Accommodation(AccommodationBase):
    Tent_ID: str

    class Config:
        orm_mode = True


class Vendor(VendorBase):
    Vendor_ID: str

    class Config:
        orm_mode = True


class Transportation(TransportationBase):
    Transport_ID: str

    class Config:
        orm_mode = True


class LostAndFound(LostAndFoundBase):
    Lost_Item_Person_ID: str

    class Config:
        orm_mode = True


class IncidentReport(IncidentReportBase):
    Incident_ID: str

    class Config:
        orm_mode = True


class PilgrimAccommodation(PilgrimAccommodationBase):
    class Config:
        orm_mode = True


class PilgrimTransportation(PilgrimTransportationBase):
    class Config:
        orm_mode = True


class PilgrimIncident(PilgrimIncidentBase):
    class Config:
        orm_mode = True


class PilgrimPurchase(PilgrimPurchaseBase):
    class Config:
        orm_mode = True


class PilgrimTreatment(PilgrimTreatmentBase):
    class Config:
        orm_mode = True


class ManagementHierarchy(ManagementHierarchyBase):
    class Config:
        orm_mode = True


# Enhanced response models with relationships
class DoctorWithRelationships(Doctor):
    hospital: Optional[Hospital] = None
    treatments: List[PilgrimTreatment] = []


class HospitalWithRelationships(Hospital):
    doctors: List[Doctor] = []
    treatments: List[PilgrimTreatment] = []


class PilgrimWithRelationships(Pilgrim):
    accommodations: List[PilgrimAccommodation] = []
    transportation: List[PilgrimTransportation] = []
    incidents: List[PilgrimIncident] = []
    purchases: List[PilgrimPurchase] = []
    treatments: List[PilgrimTreatment] = []


class PoliceStationWithRelationships(PoliceStation):
    officers: List[PoliceOfficer] = []


class PoliceOfficerWithRelationships(PoliceOfficer):
    station: Optional[PoliceStation] = None
    managers: List[ManagementHierarchy] = []
    subordinates: List[ManagementHierarchy] = []


class AccommodationWithRelationships(Accommodation):
    pilgrim_accommodations: List[PilgrimAccommodation] = []


class VendorWithRelationships(Vendor):
    purchases: List[PilgrimPurchase] = []


class TransportationWithRelationships(Transportation):
    pilgrim_transportation: List[PilgrimTransportation] = []


class IncidentReportWithRelationships(IncidentReport):
    pilgrim_incidents: List[PilgrimIncident] = []