from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.core.database import get_db
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.schemas.task import (
    TaskCreate, 
    TaskOutDetailed, 
    TaskAssign, 
    TaskStatusUpdate, 
    PaginatedTasks
)
from app.services.task_service import task_service

router = APIRouter()

@router.post("/", response_model=TaskOutDetailed, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Create a new task.
    Admin role required.
    """
    # Create the task and retrieve the detailed view (with eager-loaded relationships)
    task = task_service.create_task(db, task_in=task_in)
    return task_service.get_task_by_id(db, task_id=task.id)

@router.put("/{task_id}/assign", response_model=TaskOutDetailed)
def assign_task(
    task_id: UUID,
    assignment: TaskAssign,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Assign a task to a user.
    Admin role required. Uses database transactions for safety.
    """
    task = task_service.assign_task(
        db, 
        task_id=task_id, 
        assignee_id=assignment.assigned_to
    )
    return task_service.get_task_by_id(db, task_id=task.id)

@router.put("/{task_id}/status", response_model=TaskOutDetailed)
def update_task_status(
    task_id: UUID,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task's status.
    Any logged-in user can update:
    - Admin can update the status of any task.
    - Developer can ONLY update the status of tasks assigned to themselves.
    """
    task = task_service.update_task_status(
        db, 
        task_id=task_id, 
        status=status_update.status, 
        current_user=current_user
    )
    return task_service.get_task_by_id(db, task_id=task.id)

@router.get("/", response_model=PaginatedTasks)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    project_id: Optional[UUID] = Query(None, description="Filter by project UUID"),
    status: Optional[str] = Query(None, description="Filter by task status"),
    assigned_to: Optional[UUID] = Query(None, description="Filter by assignee user UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Tasks per page")
):
    """
    List tasks.
    Supports filtering by project, status, and assigned user.
    Includes full pagination metadata.
    """
    return task_service.list_tasks(
        db,
        project_id=project_id,
        status=status,
        assigned_to=assigned_to,
        page=page,
        limit=limit
    )
