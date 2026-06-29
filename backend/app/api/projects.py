from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.services.project_service import project_service

router = APIRouter()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Create a new project.
    Admin role required.
    """
    return project_service.create_project(
        db, 
        project_in=project_in, 
        creator_id=current_admin.id
    )

@router.get("/", response_model=List[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    List all projects.
    Any logged-in Admin or Developer can fetch the project list.
    """
    return project_service.list_projects(db, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get project details by ID.
    Any logged-in Admin or Developer can view project details.
    """
    return project_service.get_project_by_id(db, project_id=project_id)

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Update a project.
    Admin role required.
    """
    return project_service.update_project(
        db, 
        project_id=project_id, 
        project_in=project_in
    )

@router.delete("/{project_id}", response_model=ProjectOut)
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Delete a project.
    Admin role required. Cascades deletion to all child tasks.
    """
    return project_service.delete_project(db, project_id=project_id)
