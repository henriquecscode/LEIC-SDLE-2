from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import utils

SQLALCHEMY_DATABASE_URL = f"sqlite:///./test_{utils.get_port()}.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL , connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)
