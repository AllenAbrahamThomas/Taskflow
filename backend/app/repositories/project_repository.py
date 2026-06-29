from app.repositories.base import BaseRepository
from app.models.project import Project

class ProjectRepository(BaseRepository[Project]):
    pass

project_repository = ProjectRepository(Project)
