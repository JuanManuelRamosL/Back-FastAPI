from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

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

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int
    workspace_id: int  # Agregar el ID del workspace al esquema

    class Config:
        from_attributes = True
