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
    users: list["User"] = []  # Lista de usuarios en el workspace

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    workspace_id: int  # Ahora se pasa el ID del workspace al crear un usuario

class User(UserBase):
    id: int
    tasks: list["Task"] = []
    workspace_id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.ASSIGNED  # Campo de estado por defecto

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
