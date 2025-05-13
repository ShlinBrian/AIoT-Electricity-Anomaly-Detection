from sqlalchemy import create_engine, engine_from_config, pool
from sqlalchemy.orm import sessionmaker
import os 
from database.models import Base

SQLALCHEMY_DATABASE_URL = os.environ.get("DB_URL","")

engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={}
            )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()