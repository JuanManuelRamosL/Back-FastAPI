from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

# Definir un Enum para el estado de la tarea
class TaskStatus(enum.Enum):
    ASSIGNED = "asignada"
    IN_PROGRESS = "en proceso"
    UNDER_REVIEW = "revisión"
    COMPLETED = "finalizada"

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    users = relationship("User", back_populates="workspace")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)  
    
    tasks = relationship("Task", back_populates="owner")
    workspace = relationship("Workspace", back_populates="users")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(TaskStatus), default=TaskStatus.ASSIGNED)  # Estado de la tarea
    
    owner = relationship("User", back_populates="tasks")
