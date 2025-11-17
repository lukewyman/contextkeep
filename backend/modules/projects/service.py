"""
Project business logic.

This module handles project discovery and metadata management.
"""
from pathlib import Path
from typing import List
import json
from modules.files.service import list_directories, read_json_file
from modules.projects.models import ProjectMetadata, ProjectSummary
from config import settings


def list_projects() -> List[ProjectSummary]:
    """
    List all valid ContextKeep projects.
    
    Scans the projects_base_dir for directories containing valid
    .contextkeep/project.json files.
    
    Returns:
        List of ProjectSummary objects, sorted alphabetically by project_name.
        Projects without valid metadata are silently skipped.
    """
    projects_dir = settings.projects_base_dir
    
    # Get all project directories
    project_dirs = list_directories(projects_dir)
    
    projects = []
    for project_dir in project_dirs:
        try:
            # Look for .contextkeep/project.json
            metadata_file = project_dir / ".contextkeep" / "project.json"
            metadata_dict = read_json_file(metadata_file)
            
            # Parse and validate with Pydantic
            metadata = ProjectMetadata(**metadata_dict)
            
            # Add to results
            projects.append(ProjectSummary(
                project_name=metadata.project_name,
                repo_name=metadata.repo_name,
                description=metadata.description,
                created_at=metadata.created_at
            ))
            
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Skip invalid projects silently
            continue
    
    # Sort alphabetically by project_name (case-insensitive)
    projects.sort(key=lambda p: p.project_name.lower())
    
    return projects