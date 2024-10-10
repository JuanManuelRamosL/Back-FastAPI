from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:juanma123@localhost:1111/fast_api"
# https://back-fastapi.onrender.com
#DATABASE_URL= "postgresql://fast_api_ljvm_user:tZftr2NLTbcse1Oe4a45NvcAHt4GpAEy@dpg-cs1k05tds78s73b71be0-a.oregon-postgres.render.com/fast_api_ljvm"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
