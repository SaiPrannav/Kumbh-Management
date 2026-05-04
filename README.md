🪔 Kumbh Mela Management System
A full-stack web application for managing pilgrim safety, logistics, and services during the Kumbh Mela festival. Built with FastAPI and PostgreSQL, deployed on Railway.
🌐 Live Demo: https://kumbh-management-production-81f9.up.railway.app/index.html

📋 Table of Contents

Features
Tech Stack
Project Structure
Database Schema
Getting Started
API Documentation
Deployment


✨ Features

Pilgrim Management — Register, track, and manage pilgrims with medical and emergency contact info
Incident Reporting — Log and monitor incidents with status tracking (Reported → In Progress → Resolved → Closed)
Lost & Found — Track lost items and manage claim status
Hospital & Doctor Directory — Real-time availability of hospitals, doctors, and emergency response units
Accommodation Booking — Tent/camp availability and pilgrim check-in/check-out
Vendor Licensing — Manage food stalls and vendor licenses
Transportation — Track routes, timings, and emergency services
Police & Fire Services — Station management and officer hierarchy
Ghat Safety — Monitor bathing ghats with lifeguard counts and Royal Bath timings
JWT Authentication — Secure authority login system


🛠️ Tech Stack
LayerTechnologyBackendFastAPI (Python)DatabasePostgreSQLORM / DB DriverSQLAlchemy / psycopg2ValidationPydanticFrontendHTML, CSS, JavaScript (Jinja2 templates)AuthJWT (JSON Web Tokens)DeploymentRailwayProcess ManagerUvicorn via Procfile

📁 Project Structure
kumbh-management/
├── static/                  # CSS, JS, and static assets
├── templates/               # HTML templates (Jinja2)
├── main.py                  # FastAPI app, routes, and endpoints
├── database.py              # PostgreSQL connection (SQLAlchemy)
├── models.py                # SQLAlchemy ORM models
├── pydanticmodel.py         # Pydantic schemas for request/response validation
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway/Heroku process definition
└── DDL_For_KumbhDB.sql      # Full PostgreSQL DDL (table creation script)

🗄️ Database Schema
The database contains 17 tables covering all aspects of festival management:

Authorities — Admin users with hashed passwords
Pilgrims — Pilgrim profiles with medical info
Hospitals + Doctors — Medical infrastructure
Emergency_Response — Ambulance and emergency contacts
Police_Stations + Police_Officers + Management_Hierarchy — Law enforcement
Fire_Stations — Fire safety services
Ghats — Bathing ghat monitoring
Accommodation + Pilgrim_Accommodation — Camp bookings
Vendors + Pilgrim_Purchases — Market and vendor management
Transportation + Pilgrim_Transportation — Travel coordination
Lost_And_Found — Lost item tracking
Incident_Reports + Pilgrim_Incidents — Incident management

Custom PostgreSQL enums used: gender_enum, license_status_enum, claim_status_enum, incident_status_enum
To recreate the schema, run the SQL in DDL_For_KumbhDB.sql.

🚀 Getting Started
Prerequisites

Python 3.9+
PostgreSQL (local or cloud)
Git

Local Setup

Clone the repository

bash   git clone https://github.com/SaiPrannav/kumbh-management.git
   cd kumbh-management

Install dependencies

bash   pip install -r requirements.txt

Set environment variables
Create a .env file or export these variables:

env   PGHOST=localhost
   PGPORT=5432
   PGUSER=your_db_user
   PGPASSWORD=your_db_password
   PGDATABASE=kumbhdb
   SECRET_KEY=your_secret_key_here

Set up the database
Connect to your PostgreSQL instance and run:

bash   psql -U your_db_user -d kumbhdb -f DDL_For_KumbhDB.sql

Run the application

bash   uvicorn main:app --reload
Visit http://localhost:8000 in your browser.

📖 API Documentation
Once the app is running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

Or on the live deployment:
https://kumbh-management-production-81f9.up.railway.app/docs

☁️ Deployment
This project is deployed on Railway with a managed PostgreSQL database.
Environment Variables (Railway)
VariableValuePGHOST${{Postgres.PGHOST}}PGPORT${{Postgres.PGPORT}}PGUSER${{Postgres.PGUSER}}PGPASSWORD${{Postgres.PGPASSWORD}}PGDATABASE${{Postgres.PGDATABASE}}SECRET_KEY(your secret key)
The Procfile tells Railway how to start the server:
web: uvicorn main:app --host 0.0.0.0 --port $PORT

🙏 About
Built as part of a database management project to explore real-world use of relational databases, REST APIs, and cloud deployment. The Kumbh Mela is one of the largest human gatherings on Earth — this system aims to model the complexity of managing pilgrim safety and services at such a scale.
