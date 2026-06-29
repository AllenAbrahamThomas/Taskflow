from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class ProjectOut(ProjectBase):
    id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True
