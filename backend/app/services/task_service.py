from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List, Tuple
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskUpdate, PaginatedTasks
from app.repositories.task_repository import task_repository
from app.core.exceptions import ResourceNotFoundException, PermissionDeniedException

class TaskService:
    def create_task(self, db: Session, *, task_in: TaskCreate) -> Task:
        """
        Create a new task under a project.
        Verifies that both project and optional assignee exist before creation.
        """
        # Validate project exists
        project = db.get(Project, task_in.project_id)
        if not project:
            raise ResourceNotFoundException("Project")
            
        # Validate assignee exists if provided
        if task_in.assigned_to:
            assignee = db.get(User, task_in.assigned_to)
            if not assignee:
                raise ResourceNotFoundException("Assignee user")

        task_data = task_in.model_dump()
        return task_repository.create(db, obj_in_data=task_data)

    def get_task_by_id(self, db: Session, *, task_id: UUID) -> Task:
        """Fetch task by ID, raising an exception if not found."""
        task = task_repository.get(db, id=task_id)
        if not task:
            raise ResourceNotFoundException("Task")
        return task

    def assign_task(self, db: Session, *, task_id: UUID, assignee_id: Optional[UUID]) -> Task:
        """
        Assign a task to a user.
        Uses a nested database transaction (savepoint) for transactional integrity.
        """
        task = self.get_task_by_id(db, task_id=task_id)
        
        if assignee_id is not None:
            assignee = db.get(User, assignee_id)
            if not assignee:
                raise ResourceNotFoundException("Assignee user")
        
        try:
            # Transaction block
            with db.begin_nested():
                task.assigned_to = assignee_id
                db.add(task)
            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            db.rollback()
            raise e

    def update_task_status(self, db: Session, *, task_id: UUID, status: str, current_user: User) -> Task:
        """
        Update the status of a task.
        Enforces Role-Based Access Control:
        - Admin can update any task.
        - Developer can only update tasks assigned directly to themselves.
        """
        task = self.get_task_by_id(db, task_id=task_id)
        
        # Check permissions for developer
        if current_user.role == "developer":
            if not task.assigned_to or task.assigned_to != current_user.id:
                raise PermissionDeniedException("Developers can only update the status of tasks assigned to themselves")
        
        task.status = status
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def list_tasks(
        self,
        db: Session,
        *,
        project_id: Optional[UUID] = None,
        status: Optional[str] = None,
        assigned_to: Optional[UUID] = None,
        page: int = 1,
        limit: int = 10
    ) -> PaginatedTasks:
        """Fetch tasks with advanced filters and pagination metadata."""
        items, total = task_repository.get_tasks_paginated(
            db,
            project_id=project_id,
            status=status,
            assigned_to=assigned_to,
            page=page,
            limit=limit
        )
        
        # Calculate pagination metadata
        pages = (total + limit - 1) // limit if total > 0 else 1
        
        return PaginatedTasks(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

task_service = TaskService()
