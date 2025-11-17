"""
Unit tests for project service.
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
from modules.projects.service import list_projects
from modules.projects.models import ProjectSummary


@patch('modules.projects.service.read_json_file')
@patch('modules.projects.service.list_directories')
def test_list_projects_empty(mock_list_dirs, mock_read_json):
    """
    TC-P1: List projects - empty directory
    
    Given: contextkeep-projects directory is empty
    When: list_projects() is called
    Then: Returns empty list
    And: files.service.list_directories() was called once
    """
    mock_list_dirs.return_value = []
    
    result = list_projects()
    
    assert result == []
    assert mock_list_dirs.call_count == 1


@patch('modules.projects.service.read_json_file')
@patch('modules.projects.service.list_directories')
def test_list_projects_three_valid(mock_list_dirs, mock_read_json):
    """
    TC-P2: List projects - three valid projects
    
    Given: contextkeep-projects has 3 project directories
    And: Each has valid .contextkeep/project.json
    When: list_projects() is called
    Then: Returns list of 3 ProjectSummary objects
    And: Projects are sorted alphabetically by project_name
    And: Each project has correct name, repo_name, description
    """
    # Mock directory listing
    mock_list_dirs.return_value = [
        Path('/home/user/contextkeep-projects/kjbot'),
        Path('/home/user/contextkeep-projects/weather-api'),
        Path('/home/user/contextkeep-projects/taskflow')
    ]
    
    # Mock JSON file reads (return in the order they're requested)
    mock_read_json.side_effect = [
        {
            "project_name": "KJBot",
            "repo_name": "kjbot",
            "description": "Karaoke DJ system",
            "created_at": "2025-11-15T10:30:00Z",
            "contextkeep_version": "0.1.0"
        },
        {
            "project_name": "WeatherAPI",
            "repo_name": "weather-api",
            "description": "Weather data",
            "created_at": "2025-11-13T09:15:00Z",
            "contextkeep_version": "0.1.0"
        },
        {
            "project_name": "TaskFlow",
            "repo_name": "taskflow",
            "description": "Workflow automation",
            "created_at": "2025-11-14T15:22:00Z",
            "contextkeep_version": "0.1.0"
        }
    ]
    
    result = list_projects()
    
    assert len(result) == 3
    # Check alphabetical sorting
    assert result[0].project_name == "KJBot"
    assert result[1].project_name == "TaskFlow"
    assert result[2].project_name == "WeatherAPI"
    
    # Check data integrity
    assert result[0].repo_name == "kjbot"
    assert result[0].description == "Karaoke DJ system"


@patch('modules.projects.service.read_json_file')
@patch('modules.projects.service.list_directories')
def test_list_projects_skip_invalid(mock_list_dirs, mock_read_json):
    """
    TC-P3: List projects - skip invalid project
    
    Given: contextkeep-projects has 2 project directories
    And: First project has valid .contextkeep/project.json
    And: Second project is missing .contextkeep/project.json
    When: list_projects() is called
    Then: Returns list with only 1 valid project
    And: Invalid project is silently skipped
    """
    mock_list_dirs.return_value = [
        Path('/home/user/contextkeep-projects/kjbot'),
        Path('/home/user/contextkeep-projects/invalid')
    ]
    
    # First call succeeds, second raises FileNotFoundError
    mock_read_json.side_effect = [
        {
            "project_name": "KJBot",
            "repo_name": "kjbot",
            "description": "Karaoke DJ system",
            "created_at": "2025-11-15T10:30:00Z",
            "contextkeep_version": "0.1.0"
        },
        FileNotFoundError()
    ]
    
    result = list_projects()
    
    assert len(result) == 1
    assert result[0].project_name == "KJBot"


@patch('modules.projects.service.read_json_file')
@patch('modules.projects.service.list_directories')
def test_list_projects_skip_malformed_json(mock_list_dirs, mock_read_json):
    """
    TC-P4: List projects - skip malformed JSON
    
    Given: contextkeep-projects has 2 project directories
    And: First project has valid .contextkeep/project.json
    And: Second project has malformed JSON
    When: list_projects() is called
    Then: Returns list with only 1 valid project
    And: Malformed project is silently skipped
    """
    mock_list_dirs.return_value = [
        Path('/home/user/contextkeep-projects/kjbot'),
        Path('/home/user/contextkeep-projects/bad-json')
    ]
    
    mock_read_json.side_effect = [
        {
            "project_name": "KJBot",
            "repo_name": "kjbot",
            "description": "Karaoke DJ system",
            "created_at": "2025-11-15T10:30:00Z",
            "contextkeep_version": "0.1.0"
        },
        json.JSONDecodeError("Invalid JSON", "", 0)
    ]
    
    result = list_projects()
    
    assert len(result) == 1
    assert result[0].project_name == "KJBot"