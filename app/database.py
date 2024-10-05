from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://postgres:juanma123@localhost:1111/fast_api"
# https://back-fastapi.onrender.com
DATABASE_URL= "postgresql://fast_api_ecrv_user:PeEhpAFHWYKwk4c8feLgP9PulADhf2VY@dpg-cs08d2jtq21c73e8l3dg-a.oregon-postgres.render.com/fast_api_ecrv"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
