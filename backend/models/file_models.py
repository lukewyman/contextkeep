"""Data models for file operations."""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class FileNode(BaseModel):
    """Represents a file or directory in the tree."""
    
    name: str = Field(..., description="File or directory name")
    path: str = Field(..., description="Relative path from project root")
    type: Literal["file", "directory"] = Field(..., description="Node type")
    size: Optional[int] = Field(None, description="File size in bytes (files only)")
    children: Optional[list["FileNode"]] = Field(
        None, 
        description="Child nodes (directories only)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "handlers",
                    "path": "handlers",
                    "type": "directory",
                    "children": [
                        {
                            "name": "create_song.py",
                            "path": "handlers/create_song.py",
                            "type": "file",
                            "size": 1234
                        }
                    ]
                }
            ]
        }
    }


class FileTreeResponse(BaseModel):
    """Response for file tree endpoint."""
    
    project_id: str = Field(..., description="Project identifier")
    path: str = Field(..., description="Absolute path to project root")
    tree: list[FileNode] = Field(..., description="File tree structure")


class FileContentResponse(BaseModel):
    """Response for read file endpoint."""
    
    project_id: str = Field(..., description="Project identifier")
    file_path: str = Field(..., description="Relative file path")
    content: str = Field(..., description="File contents as text")
    size: int = Field(..., description="File size in bytes")
    encoding: str = Field(default="utf-8", description="Text encoding")


class FileWriteRequest(BaseModel):
    """Request to write file contents."""
    
    content: str = Field(..., description="File contents to write")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "def create_song():\n    return Song(...)\n"
                }
            ]
        }
    }


class FileWriteResponse(BaseModel):
    """Response for write file endpoint."""
    
    project_id: str = Field(..., description="Project identifier")
    file_path: str = Field(..., description="Relative file path")
    success: bool = Field(..., description="Whether write succeeded")
    size: int = Field(..., description="File size after write")
    created: bool = Field(..., description="True if file was newly created")