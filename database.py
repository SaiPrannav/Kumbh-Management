from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
URL_DATABASE = "mysql+pymysql://root:prp12345@localhost/kumbhmanagement"

engine = create_engine(URL_DATABASE, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit =False, autoflush= False, bind=engine)

Base = declarative_base()