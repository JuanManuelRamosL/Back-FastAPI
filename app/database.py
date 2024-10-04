from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:juanma123@localhost:1111/fast_api"
# https://back-fastapi.onrender.com
DATABASE_URL= "postgresql://fast_api_b6t5_user:G08GSMNHndlAbHFEMYFe8FBpLx6ZhOZJ@dpg-cs022hi3esus7399bi2g-a.oregon-postgres.render.com/fast_api_b6t5"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
