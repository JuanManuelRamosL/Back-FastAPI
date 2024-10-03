from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:juanma123@localhost:1111/fast_api"
DATABASE_URL= "postgresql://fast_api_dw2i_user:MMv9SyAXeS9xGp5uQ6yhlNI6IjjSZbA6@dpg-crvhhk9u0jms73do5u9g-a.oregon-postgres.render.com/fast_api_dw2i"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
