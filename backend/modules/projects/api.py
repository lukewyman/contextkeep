"""
Projects API endpoints.
"""
from fastapi import APIRouter
from modules.projects.service import list_projects
from modules.projects.models import ProjectListResponse

router = APIRouter()


@router.get("/projects", response_model=ProjectListResponse)
def get_projects():
    """
    List all ContextKeep projects.
    
    Returns:
        ProjectListResponse with list of projects sorted alphabetically.
    """
    projects = list_projects()
    return ProjectListResponse(projects=projects)