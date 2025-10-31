"""API endpoints for file operations."""

from fastapi import APIRouter, HTTPException, Query, Path as PathParam
from pathlib import Path

from config import settings
from services.file_service import FileService
from models.file_models import (
    FileTreeResponse,
    FileContentResponse,
    FileWriteRequest,
    FileWriteResponse,
)

router = APIRouter(prefix="/projects", tags=["files"])

# Initialize file service with configured projects directory
file_service = FileService(settings.projects_base)


@router.get("/{project_id}/tree", response_model=FileTreeResponse)
async def get_file_tree(
    project_id: str = PathParam(..., description="Project identifier"),
    max_depth: int = Query(default=3, ge=1, le=10, description="Maximum tree depth"),
    show_hidden: bool = Query(default=False, description="Include hidden files"),
):
    """Get project file tree.
    
    Returns a hierarchical tree structure of all files and directories
    in the project, respecting the max_depth parameter.
    
    Example:
        GET /projects/my-project/tree?max_depth=2&show_hidden=false
    """
    try:
        project_path = file_service.get_project_path(project_id)
        tree = file_service.build_tree(
            project_path,
            max_depth=max_depth,
            show_hidden=show_hidden
        )
        
        return FileTreeResponse(
            project_id=project_id,
            path=str(project_path),
            tree=tree,
        )
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/{project_id}/files/{file_path:path}", response_model=FileContentResponse)
async def read_file(
    project_id: str = PathParam(..., description="Project identifier"),
    file_path: str = PathParam(..., description="Relative file path from project root"),
):
    """Read file contents.
    
    Returns the text content of a file within the project.
    
    Example:
        GET /projects/my-project/files/src/main.py
    """
    try:
        project_path = file_service.get_project_path(project_id)
        content, size = file_service.read_file(project_path, file_path)
        
        return FileContentResponse(
            project_id=project_id,
            file_path=file_path,
            content=content,
            size=size,
        )
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/{project_id}/files/{file_path:path}", response_model=FileWriteResponse)
async def write_file(
    request: FileWriteRequest,
    project_id: str = PathParam(..., description="Project identifier"),
    file_path: str = PathParam(..., description="Relative file path from project root"),
):
    """Write file contents.
    
    Creates or overwrites a file with the provided content.
    Parent directories are created automatically if needed.
    
    Example:
        POST /projects/my-project/files/src/new_file.py
        Body: {"content": "print('hello')"}
    """
    try:
        project_path = file_service.get_project_path(project_id)
        size, created = file_service.write_file(
            project_path,
            file_path,
            request.content
        )
        
        return FileWriteResponse(
            project_id=project_id,
            file_path=file_path,
            success=True,
            size=size,
            created=created,
        )
    
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")