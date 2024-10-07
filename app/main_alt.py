from fastapi import FastAPI, Depends, HTTPException, Request,Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware
from typing import  List
# Crear la app de FastAPI
app_alt = FastAPI()

""" app_alt.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Reemplaza con el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """
app_alt.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Ruta raíz
@app_alt.get("/")
def read_root():
    return {"message": "Hola Mundo desde main_alt.py"}

@app_alt.post("/workspaces/", response_model=schemas.Workspace)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    return crud.create_workspace(db, workspace)

@app_alt.get("/workspaces/{workspace_id}", response_model=schemas.Workspace)
def get_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return crud.get_workspace(db, workspace_id)

@app_alt.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app_alt.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app_alt.post("/users/{user_id}/tasks/", response_model=schemas.Task)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, user_id=user_id)

@app_alt.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db=db, task_id=task_id)

@app_alt.post("/login/")
async def login_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email es requerido")
    db_user = crud.get_user_by_email(db=db, email=email)
    # Si no se encuentra el usuario, lanzar una excepción
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@app_alt.post("/users/{user_id}/workspaces/")
def add_workspace(user_id: int, workspace_id: int, db: Session = Depends(get_db)):
    user = crud.add_workspace_to_user(db=db, user_id=user_id, workspace_id=workspace_id)
    return {"message": f"Workspace {workspace_id} agregado al usuario {user_id}", "user": user}

# Endpoint para agregar un Workspace a un Usuario
@app_alt.post("/users/{user_id}/workspaces/{workspace_id}/add", response_model=schemas.User)
def add_workspace_to_user(user_id: int, workspace_id: int, db: Session = Depends(get_db)):
    return crud.add_workspace_to_user(db, user_id=user_id, workspace_id=workspace_id)

# Endpoint para agregar un Usuario a un Workspace
@app_alt.post("/workspaces/{workspace_id}/users/{user_id}/add", response_model=schemas.Workspace)
def add_user_to_workspace(workspace_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.add_user_to_workspace(db, user_id=user_id, workspace_id=workspace_id)

# Endpoint para obtener todos los workspaces de un usuario
@app_alt.get("/users/{user_id}/workspaces", response_model=List[schemas.Workspace])
def get_user_workspaces(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user.workspaces  # Devuelve todos los workspaces asociados al usuario

@app_alt.post("/workspaces/{workspace_id}/tasks/", response_model=schemas.Task)
def create_task_in_workspace(workspace_id: int, task: schemas.TaskCreate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, workspace_id=workspace_id, user_id=user_id)

@app_alt.get("/workspaces/{workspace_id}/tasks", response_model=List[schemas.Task])
def get_tasks_by_workspace(workspace_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.workspace_id == workspace_id).all()
    return tasks

# Actualizar el estado de una tarea
@app_alt.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, new_status: str, db: Session = Depends(get_db)):
    updated_task = crud.update_task_status(db=db, task_id=task_id, new_status=new_status)
    return {"message": f"Tarea {task_id} actualizada con éxito", "task": updated_task}
# Instrucción para levantar la app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_alt:app_alt", host="127.0.0.1", port=8001, reload=True)


##uvicorn app.main_alt:app_alt --reload