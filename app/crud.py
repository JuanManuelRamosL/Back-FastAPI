from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

# Crear un workspace
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

# Obtener un workspace por ID
def get_workspace(db: Session, workspace_id: int):
    return db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()

# Crear un usuario
def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(name=user.name, email=user.email)
        
        # Si se ha pasado workspace_ids, agregar los workspaces al usuario
        if user.workspace_ids:
            workspaces = db.query(models.Workspace).filter(models.Workspace.id.in_(user.workspace_ids)).all()
            if not workspaces:
                raise HTTPException(status_code=404, detail="Uno o más workspaces no encontrados")
            db_user.workspaces = workspaces

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error creando usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al crear usuario")

# Obtener un usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Crear una tarea para un usuario
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Eliminar una tarea por ID
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Obtener usuario por correo electrónico
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Agregar un workspace a un usuario
def add_workspace_to_user(db: Session, user_id: int, workspace_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    workspace = db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace no encontrado")
    
    # Verificar si el workspace ya está asociado al usuario
    if workspace in user.workspaces:
        raise HTTPException(status_code=400, detail="Workspace ya asignado al usuario")

    user.workspaces.append(workspace)
    db.commit()
    db.refresh(user)
    return user

# Agregar un usuario a un workspace
def add_user_to_workspace(db: Session, user_id: int, workspace_id: int):
    workspace = db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace no encontrado")
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si el usuario ya está en el workspace
    if user in workspace.users:
        raise HTTPException(status_code=400, detail="Usuario ya asignado al workspace")

    workspace.users.append(user)
    db.commit()
    db.refresh(workspace)
    return workspace

# uvicorn app.main_alt:app_alt --reload --port 8001