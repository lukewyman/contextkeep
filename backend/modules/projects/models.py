"""
Project models for ContextKeep.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class ProjectMetadata(BaseModel):
    """
    Project metadata stored in .contextkeep/project.json
    """
    project_name: str = Field(..., description="Human-readable project name")
    repo_name: str = Field(..., description="Repository/directory name")
    description: str = Field(..., description="Project description")
    created_at: datetime = Field(..., description="Project creation timestamp")
    contextkeep_version: str = Field(default="0.1.0", description="ContextKeep version")


class ProjectSummary(BaseModel):
    """
    Summary view of a project for list display
    """
    project_name: str
    repo_name: str
    description: str
    created_at: datetime


class ProjectListResponse(BaseModel):
    """
    API response for GET /api/projects
    """
    projects: List[ProjectSummary] = Field(default_factory=list)