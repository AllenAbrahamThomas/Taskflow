from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import project_repository
from app.core.exceptions import ResourceNotFoundException

class ProjectService:
    def create_project(self, db: Session, *, project_in: ProjectCreate, creator_id: UUID) -> Project:
        """Create a new project."""
        project_data = project_in.model_dump()
        project_data["created_by"] = creator_id
        return project_repository.create(db, obj_in_data=project_data)

    def get_project_by_id(self, db: Session, *, project_id: UUID) -> Project:
        """Retrieve project by ID, raises exception if not found."""
        project = project_repository.get(db, id=project_id)
        if not project:
            raise ResourceNotFoundException("Project")
        return project

    def list_projects(self, db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
        """List all projects."""
        return project_repository.get_multi(db, skip=skip, limit=limit)

    def update_project(self, db: Session, *, project_id: UUID, project_in: ProjectUpdate) -> Project:
        """Update an existing project's fields."""
        project = self.get_project_by_id(db, project_id=project_id)
        # Filter out fields that are None
        update_data = project_in.model_dump(exclude_unset=True)
        return project_repository.update(db, db_obj=project, obj_in_data=update_data)

    def delete_project(self, db: Session, *, project_id: UUID) -> Project:
        """Delete project."""
        project = self.get_project_by_id(db, project_id=project_id)
        return project_repository.remove(db, id=project_id)

project_service = ProjectService()
