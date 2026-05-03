from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus

MYSQLUSER = os.environ.get("MYSQLUSER", "root")
MYSQLPASSWORD = quote_plus(os.environ.get("MYSQLPASSWORD", ""))
MYSQLHOST = os.environ.get("MYSQLHOST", "localhost")
MYSQLPORT = os.environ.get("MYSQLPORT", "3306")
MYSQLDATABASE = os.environ.get("MYSQLDATABASE", "railway")

URL_DATABASE = f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"

engine = create_engine(URL_DATABASE, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()