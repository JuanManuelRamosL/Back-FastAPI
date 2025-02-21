from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://postgres:juanma123@localhost:1111/fast_api"
# https://back-fastapi.onrender.com
DATABASE_URL= "postgresql://tareas_rroe_user:O4iRxv7hRZD1h0lHEzMIhzZPJ7fWnqI0@dpg-cusfjg3tq21c73b45m9g-a.oregon-postgres.render.com/tareas_rroe"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
