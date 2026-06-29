from typing import List, Tuple, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.repositories.base import BaseRepository
from app.models.task import Task

class TaskRepository(BaseRepository[Task]):
    def get_tasks_paginated(
        self,
        db: Session,
        *,
        project_id: Optional[UUID] = None,
        status: Optional[str] = None,
        assigned_to: Optional[UUID] = None,
        page: int = 1,
        limit: int = 10
    ) -> Tuple[List[Task], int]:
        """
        Query tasks dynamically with optional filters (project_id, status, assigned_to).
        Pre-loads related project and assignee models to avoid N+1 queries.
        """
        # Load related data eagerly
        query = db.query(self.model).options(
            joinedload(self.model.project),
            joinedload(self.model.assignee)
        )
        
        # Apply filters if provided
        if project_id is not None:
            query = query.filter(self.model.project_id == project_id)
        if status is not None:
            query = query.filter(self.model.status == status)
        if assigned_to is not None:
            query = query.filter(self.model.assigned_to == assigned_to)
            
        # Count total records matching filters
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        items = query.order_by(self.model.created_at.desc()).offset(offset).limit(limit).all()
        
        return items, total

task_repository = TaskRepository(Task)
