"""
Unit tests for projects API endpoints.
"""
from unittest.mock import patch
from datetime import datetime
from modules.projects.models import ProjectSummary


@patch('modules.projects.api.list_projects')
def test_get_projects_endpoint_unit(mock_list_projects, test_client):
    """
    TC-P5: GET /api/projects endpoint (mocked service)
    
    Unit test for API endpoint - mocks service layer.
    
    Given: Service layer is mocked to return project list
    When: GET /api/projects is called
    Then: Returns 200 OK
    And: Response matches expected structure
    And: Service was called once
    """
    # Mock the service layer
    mock_list_projects.return_value = [
        ProjectSummary(
            project_name="KJBot",
            repo_name="kjbot",
            description="Test project",
            created_at=datetime(2025, 11, 15, 10, 30)
        ),
        ProjectSummary(
            project_name="TaskFlow",
            repo_name="taskflow",
            description="Another test",
            created_at=datetime(2025, 11, 14, 15, 22)
        )
    ]
    
    response = test_client.get("/api/projects")
    
    assert response.status_code == 200
    assert mock_list_projects.call_count == 1
    
    data = response.json()
    assert len(data["projects"]) == 2
    assert data["projects"][0]["project_name"] == "KJBot"