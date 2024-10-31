from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from .database import Base
import enum

# Enum para el estado de la tarea
class TaskStatus(enum.Enum):
    ASSIGNED = "asignada"
    IN_PROGRESS = "en proceso"
    UNDER_REVIEW = "revisión"
    COMPLETED = "finalizada"

# Tabla intermedia para la relación muchos a muchos entre User y Workspace
user_workspaces = Table(
    "user_workspaces",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("workspace_id", Integer, ForeignKey("workspaces.id"), primary_key=True)
)

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # Relación muchos a muchos con los usuarios
    users = relationship("User", secondary=user_workspaces, back_populates="workspaces")
    
    # Relación uno a muchos con las tareas
    tasks = relationship("Task", back_populates="workspace")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Agregar el campo de contraseña
    image_url = Column(String, nullable=True)  # Campo opcional para la imagen

    workspaces = relationship("Workspace", secondary=user_workspaces, back_populates="users")
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))  # Agregar ForeignKey al workspace
    status = Column(Enum(TaskStatus), default=TaskStatus.ASSIGNED)  # Estado de la tarea
    
    owner = relationship("User", back_populates="tasks")  # Relación con el usuario
    workspace = relationship("Workspace", back_populates="tasks")  # Relación con el workspace
