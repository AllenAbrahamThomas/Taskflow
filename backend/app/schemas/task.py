from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, Literal
from app.schemas.user import UserOut

class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Literal["todo", "in_progress", "review", "done"] = Field("todo")
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: UUID
    assigned_to: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[Literal["todo", "in_progress", "review", "done"]] = None
    due_date: Optional[datetime] = None

class TaskAssign(BaseModel):
    assigned_to: Optional[UUID] = None

class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "review", "done"]

class ProjectMinOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class TaskOut(TaskBase):
    id: UUID
    project_id: UUID
    assigned_to: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TaskOutDetailed(TaskOut):
    project: ProjectMinOut
    assignee: Optional[UserOut] = None

    class Config:
        from_attributes = True

# Pagination helper
class PaginatedTasks(BaseModel):
    items: list[TaskOutDetailed]
    total: int
    page: int
    limit: int
    pages: int
