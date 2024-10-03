from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

def create_workspace(db: Session, workspace: schemas.WorkspaceCreate):
    try:
        db_workspace = models.Workspace(name=workspace.name)
        db.add(db_workspace)
        db.commit()
        db.refresh(db_workspace)
        return db_workspace
    except Exception as e:
        print(f"Error creando workspace: {e}")
        raise HTTPException(status_code=500, detail="Error al crear workspace")

def get_workspace(db: Session, workspace_id: int):
    return db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, workspace_id=user.workspace_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# uvicorn app.main_alt:app_alt --reload --port 8001