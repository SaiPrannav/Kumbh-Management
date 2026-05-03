import logging
from fastapi import FastAPI, HTTPException, Depends, status, Request
from pydantic import BaseModel
from typing import Generator, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydanticmodel import *
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
import uuid
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt_sha256

logging.basicConfig(level=logging.DEBUG)
#this basically helps us get the detailed debugging info in the terminal and hence feels helpful while handling requests and api calls 
#as I can easily track the errors

app = FastAPI(title="Kumbh Management")
#creates an object of the FastAPI class and renames the title of the API in the docs to Kumbh Management

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#now here in the snippet I have utilized the add middleware/cors middleware the basic function of this is to simply allow the FstAPI backend to 
#communicate with the fetch requests from the js files in the frontend or if my frontend is hosted on different url and the backend is hosted on the different url
#this acts as a medium for them to communicate by allowing different origins to talk to each other

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") #this segment utilizes a library called as jinja 2 that can help us fetch static and templates front the backend and present them dynamically

#this section simply creates the key that hashes the passwords
SECRET_KEY = "momentarylapseofreason_25"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency to get the database session
#this functions helps us access database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#this section simply contains all the APIs

@app.get("/", response_class=HTMLResponse)
async def get_homepage(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login1.html", response_class=HTMLResponse)
async def get_homepage(request:Request):
    return templates.TemplateResponse("login1.html", {"request": request})

@app.get("/index.html", response_class=HTMLResponse)
async def get_home(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accomodation.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_accomodationpage(request:Request):
    return templates.TemplateResponse("accomodation.html", {"request": request})

@app.get("/dashboard.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_accomodationpage(request:Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/healthcare.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_health(request:Request):
    return templates.TemplateResponse("healthcare.html", {"request": request})

@app.get("/incident.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_inchident(request:Request):
    return templates.TemplateResponse("incident.html", {"request": request})

@app.get("/fire.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_fire(request:Request):
    return templates.TemplateResponse("fire.html", {"request": request})

@app.get("/lost_found.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_lost(request:Request):
    return templates.TemplateResponse("lost_found.html", {"request": request})

@app.get("/police.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_pols(request:Request):
    return templates.TemplateResponse("police.html", {"request": request})

@app.get("/register.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_regis(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/stall.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_stalls(request:Request):
    return templates.TemplateResponse("stall.html", {"request": request})

@app.get("/transport.html", response_class=HTMLResponse)  # Fixed trailing slash
async def get_trans(request:Request):
    return templates.TemplateResponse("transport.html", {"request": request})

@app.post("/pilgrims/register", status_code=201)
async def register_pilgrims(pilgrim_data: PilgrimBase, db:Session = Depends(get_db)):
    pilgrim_id = str(uuid.uuid4())
    query = text(""" 
        INSERT INTO Pilgrims(PILGRIM_ID, NAME, AGE, GENDER, CONTACT_NUMBER, EMAIL_ADDRESS, ADDRESS, EMERGENCY_CONTACT, MEDICAL_CONDITION)
        VALUES(:pilgrim_id, :name, :age, :gender, :contact_number,
                :email_address, :address, :emergency_contact, :medical_condition)
    """)
    try:
        db.execute(
            query,
            {
                "pilgrim_id": pilgrim_id,
                "name": pilgrim_data.Name,
                "age": pilgrim_data.Age,
                "gender": pilgrim_data.Gender.value if hasattr(pilgrim_data.Gender, 'value') else pilgrim_data.Gender,
                "contact_number": pilgrim_data.Contact_Number,
                "email_address": pilgrim_data.Email_Address,
                "address": pilgrim_data.Address,
                "emergency_contact": pilgrim_data.Emergency_Contact,
                "medical_condition": pilgrim_data.Medical_Condition
            }
        )

        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error in pilgrim registration: {str(e)}")
        return {'message': f'Error occurred: {str(e)}'}

    return {
        'message' : 'Successfully Created the user',
        'id' : pilgrim_id
        }

@app.post("/incidents/report", status_code=202)
async def register_incident(incident_data: IncidentReportBase, db:Session = Depends(get_db)):
    incident_id = str(uuid.uuid4())
    query = text(""" 
        INSERT INTO incident_reports(Incident_ID, Incident_Type, Date_Time, Location, Reported_By, Status, Assigned_Authority)
        VALUES(:incident_id, :type, :date_time, :location, :reported_by, :status, :assigned_auth);

    """)
    try:
        db.execute(
            query,
            {
                "incident_id" : incident_id,
                "type" : incident_data.Incident_Type,
                "date_time" : incident_data.Date_Time,
                "location" : incident_data.Location,
                "reported_by" : incident_data.Reported_By,
                "status" : incident_data.Status,
                "assigned_auth" : incident_data.Assigned_Authority
            }
        )

        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error in incident reporting: {str(e)}")
        return {'message': f'Error occurred: {str(e)}'}

    return {
        'message' : 'Successfully registered Incident',
        'caseId' : incident_id
        }


@app.post("/lostfound/report", status_code=203)
async def lost_found_reporting(incident_data: LostAndFoundBase, db:Session = Depends(get_db)):
    incident_id = str(uuid.uuid4())
    query = text(""" 
        INSERT INTO lost_and_found(Lost_Item_Person_ID, Description, Date_Time, Reported_By, Availability, Claim_Status, Location)
        VALUES(:lost_person, :desc, :date_time, :reported_by, :avail, :claim, :location);

    """)
    try:
        db.execute(
            query,
            {
                "lost_person" : incident_id,
                "desc" : incident_data.Description,
                "date_time" : incident_data.Date_Time,
                "reported_by" : incident_data.Reported_By,
                "avail" : incident_data.Availability,
                "claim" : incident_data.Claim_Status,
                "location" : incident_data.Location
            }
        )

        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error in lost and found reporting: {str(e)}")
        return {'message': f'Error occurred: {str(e)}'}

    return {
        'message' : 'Successfully registered lost&found',
        'referenceId' : incident_id
        }


@app.get("/firestations", response_model=List[FireStation])
async def get_fire_stations(db: Session = Depends(get_db)):
    query = text("""
        SELECT Fire_Station_ID, Fire_Station_Name, Location, Contact, Number_Of_Trucks
        FROM Fire_Stations;
    """)

    try:
        result = db.execute(query)
        stations = result.fetchall()

        return [
            FireStation(
                Fire_Station_ID=station[0],  
                Fire_Station_Name=station[1],
                Location=station[2],
                Contact=station[3],
                Number_of_trucks=station[4]
            )
            for station in stations
        ]
    except Exception as e:
        logging.error(f"Error fetching fire stations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
@app.get("/healthcare-data")
async def get_healthcare_data(db: Session = Depends(get_db)):
    try:
        hospitals = db.execute(text("SELECT Hospital_ID, Hospital_Name, Location, Number_Of_Available_Beds, Emergency_Contact_Number, Facilities, Specialized_Medical_Services FROM Hospitals")).mappings().all()

        doctors = db.execute(text("SELECT Doctor_ID, Name, Specialization, Contact_Number, Hospital_ID FROM Doctors")).mappings().all()

        emergency_responses = db.execute(text("SELECT Response_ID, Ambulance_Availability, Emergency_Contact_Number, Location FROM Emergency_Response")).mappings().all()

        return {
            "hospitals": hospitals if hospitals else [],
            "doctors": doctors if doctors else [],
            "emergency_responses": emergency_responses if emergency_responses else []
        }
    except Exception as e:
        logging.error(f"Error fetching healthcare data: {str(e)}")
        return {"message": f"Error fetching healthcare data: {str(e)}"}
    
    
@app.get("/transportation", response_model=List[Transportation])
async def get_transports(db: Session = Depends(get_db)):
    query = text("""
                 SELECT Transport_ID, Transport_Type, Operator_Name, Route_Information, Departure_And_Arrival_Timings, Contact_Information, Emergency_Services
                 FROM Transportation;
            """)

    try:
        result = db.execute(query)
        transports = result.fetchall()

        return [
            Transportation(
                Transport_ID=transport[0],  
                Transport_Type=transport[1],
                Operator_Name=transport[2],
                Route_Information=transport[3],
                Departure_And_Arrival_Timings=transport[4],
                Contact_Information=transport[5],
                Emergency_Services=transport[6]
            )
            for transport in transports
        ]
    except Exception as e:
        logging.error(f"Error fetching transportation data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
@app.get("/accommodation", response_model=List[Accommodation])
async def get_accomodation(db: Session = Depends(get_db)):
    query = text("""
                 SELECT Tent_ID, Tent_Name, Location, Capacity, Availability, Contact_For_Booking
                 FROM Accommodation;
            """)

    try:
        result = db.execute(query)
        hotels = result.mappings().all() #so either we can do manual mapping like we have been doing up above or what we can do is simply use mappings.all function and it
                                        # essentially does that for us quite and interesting thing to be honest

        return [
            Accommodation(**hotel)
            for hotel in hotels
        ]
    except Exception as e:
        logging.error(f"Error fetching transportation data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
# Here lies the code to handle the successfull login/logout implementation 
# this section employs the security of the code

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def fetch_user(db: Session, username: str):
    # Keep your raw SQL query approach
    result = db.execute(text("SELECT * FROM authorities WHERE USERNAME = :username"), {"username": username}).fetchone()
    return result

def verify_password(plain_password: str, hashed_password: str):
    # Use bcrypt_sha256 directly as in your original code
    return bcrypt_sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode and verify token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    
    user = fetch_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = fetch_user(db, form_data.username)
    print(user)
    if not user or not verify_password(form_data.password, user.hash_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[1]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_authority(data: RegisterInput, db: Session = Depends(get_db)):
    
    existing_user = fetch_user(db, data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Username '{data.username}' already exists"
        )
    
    hashi = bcrypt_sha256.hash(data.password)
    
    try:
        def generate_unique_id():
            return uuid.uuid4().int >> (128 - 32)
        uni = generate_unique_id()

        db.execute(
            text("INSERT INTO authorities (User_ID ,Username, hash_pwd) VALUES (:unique, :username, :password)"),
            {"unique":uni ,"username": data.username, "password": hashi}
        )
        db.commit()
        return {"message": f"Authority '{data.username}' registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Registration failed: {str(e)}")