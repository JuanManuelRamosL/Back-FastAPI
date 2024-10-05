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
    # Si no se ha proporcionado un workspace_id, se crea o asigna uno por defecto
    if not user.workspace_id:
        # Intentar obtener un workspace por defecto
        default_workspace = db.query(models.Workspace).filter_by(name="Default Workspace").first()
        
        # Si no existe, crearlo
        if not default_workspace:
            default_workspace = models.Workspace(name="Default Workspace")
            db.add(default_workspace)
            db.commit()
            db.refresh(default_workspace)
        
        # Asignar el ID del workspace por defecto al usuario
        user.workspace_id = default_workspace.id
    
    # Crear el usuario con el workspace asignado
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

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# uvicorn app.main_alt:app_alt --reload --port 8001