# blockchain/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_config import DATABASE_URL
from .models import Base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
