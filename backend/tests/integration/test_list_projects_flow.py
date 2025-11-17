"""
Integration tests for list projects - full stack with real I/O.

These tests use NO MOCKS - they test the complete flow from
API → Service → File I/O using real fixture files.
"""
from pathlib import Path


def test_list_projects_end_to_end(test_client, test_projects_fixture_path, monkeypatch):
    """
    TC-I1: GET /api/projects - end-to-end with real files
    
    Full integration test - NO MOCKS, uses real fixture files.
    
    Given: Real fixture project directories with .contextkeep/project.json files
    When: GET /api/projects is called
    Then: System reads actual files from fixtures
    And: Returns 200 OK with correctly parsed projects
    And: Projects are sorted alphabetically
    
    This test verifies the full stack:
    - API endpoint (projects/api.py)
    - Service layer (projects/service.py)
    - File I/O operations (files/service.py)
    - Pydantic parsing (projects/models.py)
    """
    # Point settings to use test fixtures directory (real files!)
    from config import settings
    monkeypatch.setattr(settings, 'projects_base_dir', test_projects_fixture_path)
    
    # Make actual API call - will read real files, no mocks
    response = test_client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify it read and parsed real fixture files correctly
    assert len(data["projects"]) == 3
    assert data["projects"][0]["project_name"] == "KJBot"
    assert data["projects"][1]["project_name"] == "TaskFlow"
    assert data["projects"][2]["project_name"] == "WeatherAPI"
    
    # Verify full data integrity from actual JSON files
    kjbot = data["projects"][0]
    assert kjbot["repo_name"] == "kjbot"
    assert kjbot["description"] == "Karaoke DJ system with queue management"
    assert "created_at" in kjbot