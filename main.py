import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
import jwt
from datetime import datetime, timedelta
import os

from pydanticmodel import *
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Kumbh Management")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (CSS, images, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES_DIR = "templates"

def serve_html(filename: str):
    """Serve a plain HTML file from the templates directory."""
    filepath = os.path.join(TEMPLATES_DIR, filename)
    if not os.path.exists(filepath):
        return HTMLResponse(f"<h2>Page not found: {filename}</h2>", status_code=404)
    return FileResponse(filepath, media_type="text/html")


# =========================
# HTML ROUTES
# =========================

@app.get("/", response_class=HTMLResponse)
async def root():
    return serve_html("index.html")

@app.get("/index.html", response_class=HTMLResponse)
async def index():
    return serve_html("index.html")

@app.get("/login1.html", response_class=HTMLResponse)
async def login_page():
    return serve_html("login1.html")

@app.get("/accomodation.html", response_class=HTMLResponse)
async def accomodation():
    return serve_html("accomodation.html")

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard():
    return serve_html("dashboard.html")

@app.get("/healthcare.html", response_class=HTMLResponse)
async def healthcare():
    return serve_html("healthcare.html")

@app.get("/incident.html", response_class=HTMLResponse)
async def incident():
    return serve_html("incident.html")

@app.get("/fire.html", response_class=HTMLResponse)
async def fire():
    return serve_html("fire.html")

@app.get("/lost_found.html", response_class=HTMLResponse)
async def lost():
    return serve_html("lost_found.html")

@app.get("/police.html", response_class=HTMLResponse)
async def police():
    return serve_html("police.html")

@app.get("/register.html", response_class=HTMLResponse)
async def register_page():
    return serve_html("register.html")

@app.get("/stall.html", response_class=HTMLResponse)
async def stall():
    return serve_html("stall.html")

@app.get("/transport.html", response_class=HTMLResponse)
async def transport():
    return serve_html("transport.html")


# =========================
# DB Dependency
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# PILGRIM REGISTER API
# =========================

@app.post("/pilgrims/register", status_code=201)
async def register_pilgrims(pilgrim_data: PilgrimBase, db: Session = Depends(get_db)):
    pilgrim_id = str(uuid.uuid4())

    query = text("""
        INSERT INTO Pilgrims
        (Pilgrim_ID, Name, Age, Gender, Contact_Number, Email_Address, Address, Emergency_Contact, Medical_Condition)
        VALUES
        (:pid, :name, :age, :gender, :contact, :email, :addr, :emergency, :medical)
    """)

    try:
        db.execute(query, {
            "pid": pilgrim_id,
            "name": pilgrim_data.Name,
            "age": pilgrim_data.Age,
            "gender": pilgrim_data.Gender.value if pilgrim_data.Gender else None,
            "contact": pilgrim_data.Contact_Number,
            "email": pilgrim_data.Email_Address,
            "addr": pilgrim_data.Address,
            "emergency": pilgrim_data.Emergency_Contact,
            "medical": pilgrim_data.Medical_Condition
        })
        db.commit()
        logging.info(f"Registered pilgrim: {pilgrim_id}")
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to register pilgrim: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Success", "id": pilgrim_id}


# =========================
# AUTH
# =========================

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(
        text("SELECT * FROM Authorities WHERE Username=:u"),
        {"u": form_data.username}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user[1]})
    return {"access_token": token, "token_type": "bearer"}

# =========================
# LOST & FOUND API
# =========================

@app.post("/lost-and-found/report", status_code=201)
async def report_lost_found(item: LostAndFoundCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO Lost_And_Found
        (Lost_Item_Person_ID, Description, Date_Time, Reported_By, Availability, Claim_Status, Location)
        VALUES
        (:id, :desc, :dt, :by, :avail, :claim, :loc)
    """)
    try:
        db.execute(query, {
            "id":    item.Lost_Item_Person_ID,
            "desc":  item.Description,
            "dt":    item.Date_Time,
            "by":    item.Reported_By,
            "avail": item.Availability,
            "claim": item.Claim_Status.value if item.Claim_Status else "Unclaimed",
            "loc":   item.Location,
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Reported successfully"}


# =========================
# INCIDENT REPORT API
# =========================

@app.post("/incidents/report", status_code=201)
async def report_incident(incident: IncidentReportCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO Incident_Reports
        (Incident_ID, Incident_Type, Date_Time, Location, Reported_By, Status, Assigned_Authority)
        VALUES
        (:id, :type, :dt, :loc, :by, :status, :auth)
    """)
    try:
        db.execute(query, {
            "id":     incident.Incident_ID,
            "type":   incident.Incident_Type,
            "dt":     incident.Date_Time,
            "loc":    incident.Location,
            "by":     incident.Reported_By,
            "status": incident.Status.value if incident.Status else "Pending",
            "auth":   incident.Assigned_Authority,
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Incident reported successfully"}