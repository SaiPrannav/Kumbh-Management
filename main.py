import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
import jwt
from datetime import datetime, timedelta

from pydanticmodel import *
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Kumbh Management")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ STATIC (NO CONDITION — ALWAYS MOUNT)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ TEMPLATES (NO None — MUST EXIST)
templates = Jinja2Templates(directory="templates")


# ✅ SAFE TEMPLATE FUNCTION
def render_template(template_name: str, request: Request):
    try:
        return templates.TemplateResponse(template_name, {"request": request})
    except Exception as e:
        return HTMLResponse(f"Template error: {str(e)}")


# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 🌐 HTML ROUTES
# =========================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return render_template("index.html", request)

@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):
    return render_template("index.html", request)

@app.get("/login1.html", response_class=HTMLResponse)
async def login_page(request: Request):
    return render_template("login1.html", request)

@app.get("/accomodation.html", response_class=HTMLResponse)
async def accomodation(request: Request):
    return render_template("accomodation.html", request)

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard(request: Request):
    return render_template("dashboard.html", request)

@app.get("/healthcare.html", response_class=HTMLResponse)
async def healthcare(request: Request):
    return render_template("healthcare.html", request)

@app.get("/incident.html", response_class=HTMLResponse)
async def incident(request: Request):
    return render_template("incident.html", request)

@app.get("/fire.html", response_class=HTMLResponse)
async def fire(request: Request):
    return render_template("fire.html", request)

@app.get("/lost_found.html", response_class=HTMLResponse)
async def lost(request: Request):
    return render_template("lost_found.html", request)

@app.get("/police.html", response_class=HTMLResponse)
async def police(request: Request):
    return render_template("police.html", request)

@app.get("/register.html", response_class=HTMLResponse)
async def register(request: Request):
    return render_template("register.html", request)

@app.get("/stall.html", response_class=HTMLResponse)
async def stall(request: Request):
    return render_template("stall.html", request)

@app.get("/transport.html", response_class=HTMLResponse)
async def transport(request: Request):
    return render_template("transport.html", request)


# =========================
# 🧾 PILGRIM REGISTER API
# =========================

@app.post("/pilgrims/register", status_code=201)
async def register_pilgrims(pilgrim_data: PilgrimBase, db: Session = Depends(get_db)):
    pilgrim_id = str(uuid.uuid4())

    query = text("""
        INSERT INTO Pilgrims
        (PILGRIM_ID, NAME, AGE, GENDER, CONTACT_NUMBER, EMAIL_ADDRESS, ADDRESS, EMERGENCY_CONTACT, MEDICAL_CONDITION)
        VALUES
        (:pid, :name, :age, :gender, :contact, :email, :addr, :emergency, :medical)
    """)

    try:
        db.execute(query, {
            "pid": pilgrim_id,
            "name": pilgrim_data.Name,
            "age": pilgrim_data.Age,
            "gender": pilgrim_data.Gender,
            "contact": pilgrim_data.Contact_Number,
            "email": pilgrim_data.Email_Address,
            "addr": pilgrim_data.Address,
            "emergency": pilgrim_data.Emergency_Contact,
            "medical": pilgrim_data.Medical_Condition
        })
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    return {"message": "Success", "id": pilgrim_id}


# =========================
# 🔐 AUTH
# =========================

SECRET_KEY = "secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict):
    data.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(
        text("SELECT * FROM authorities WHERE username=:u"),
        {"u": form_data.username}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user[1]})
    return {"access_token": token}