"""
Unit tests for project models.
"""
from datetime import datetime
from modules.projects.models import ProjectMetadata, ProjectSummary, ProjectListResponse


def test_project_metadata_valid():
    """Test ProjectMetadata with valid data"""
    data = {
        "project_name": "Test Project",
        "repo_name": "test-project",
        "description": "A test project",
        "created_at": "2025-11-15T10:30:00Z",
        "contextkeep_version": "0.1.0"
    }
    
    metadata = ProjectMetadata(**data)
    
    assert metadata.project_name == "Test Project"
    assert metadata.repo_name == "test-project"
    assert metadata.description == "A test project"
    assert isinstance(metadata.created_at, datetime)


def test_project_summary_valid():
    """Test ProjectSummary with valid data"""
    summary = ProjectSummary(
        project_name="KJBot",
        repo_name="kjbot",
        description="Karaoke system",
        created_at=datetime.now()
    )
    
    assert summary.project_name == "KJBot"
    assert summary.repo_name == "kjbot"


def test_project_list_response_empty():
    """Test ProjectListResponse with empty list"""
    response = ProjectListResponse(projects=[])
    assert response.projects == []


def test_project_list_response_with_projects():
    """Test ProjectListResponse with projects"""
    projects = [
        ProjectSummary(
            project_name="Project1",
            repo_name="project1",
            description="First",
            created_at=datetime.now()
        ),
        ProjectSummary(
            project_name="Project2",
            repo_name="project2",
            description="Second",
            created_at=datetime.now()
        )
    ]
    
    response = ProjectListResponse(projects=projects)
    assert len(response.projects) == 2