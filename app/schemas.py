from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from uuid import uuid4
from datetime import datetime


def generate_uuid():
    return str(uuid4())


def generate_date():
    return str(datetime.now())

# Definición del Enum para el estado de la tarea
class TaskStatus(str, Enum):
    ASSIGNED = "asignada"
    IN_PROGRESS = "en proceso"
    UNDER_REVIEW = "revisión"
    COMPLETED = "finalizada"

class WorkspaceBase(BaseModel):
    name: str

class WorkspaceCreate(WorkspaceBase):
    pass

class Workspace(WorkspaceBase):
    id: int
    users: List["User"] = []  # Lista de usuarios en el workspace
    tasks: List["Task"] = []  # Lista de tareas del workspace

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str 
    workspace_ids: Optional[List[int]] = None  # Lista opcional de IDs de workspaces

class User(UserBase):
    id: int
    tasks: List["Task"] = []
    workspaces_ids: List[int] = []  # Lista de IDs de los workspaces

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.ASSIGNED  # Estado por defecto
    image_url: Optional[str] = None

class TaskCreate(TaskBase):
    workspace_id: int  # Incluir el ID del workspace en la creación de tareas

class Task(TaskBase):
    id: int
    owner_id: int
    workspace_id: int  # Agregar el ID del workspace al esquema

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    new_status: str
    
class Product(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    name: str
    price: float
    date: str = Field(default_factory=generate_date)