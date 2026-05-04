from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus

PGUSER     = os.environ.get("PGUSER", "postgres")
PGPASSWORD = quote_plus(os.environ.get("PGPASSWORD", ""))
PGHOST     = os.environ.get("PGHOST", "localhost")
PGPORT     = os.environ.get("PGPORT", "5432")
PGDATABASE = os.environ.get("PGDATABASE", "railway")

URL_DATABASE = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

engine = create_engine(URL_DATABASE, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()