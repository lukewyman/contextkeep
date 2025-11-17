# UC-001: List Projects

**Feature**: Display all ContextKeep projects to the user  
**Status**: Draft  
**Created**: 2025-11-15  
**Modules**: `projects`, `files`

---

## Table of Contents

1. [User Story](#user-story)
2. [UI Specification](#ui-specification)
3. [API Contracts](#api-contracts)
4. [Module Architecture](#module-architecture)
5. [Data Models](#data-models)
6. [Test Cases](#test-cases)
7. [Implementation Notes](#implementation-notes)
8. [Code Structure](#code-structure)
9. [Implementation Guide](#implementation-guide)
10. [How to Run This Feature](#how-to-run-this-feature)

---

## 1. User Story

**As a** ContextKeep user  
**I want to** see a list of all my existing projects  
**So that** I can select which project to work on or create a new one

### Acceptance Criteria

- ✅ Projects are displayed in alphabetical order by `project_name`
- ✅ Each project shows: name, repo name (when expanded), and description (when expanded)
- ✅ Projects without valid `.contextkeep/project.json` are not displayed
- ✅ Empty project list displays helpful message
- ✅ User can expand/collapse project details with + icon
- ✅ User can click project name to open it
- ✅ "Create New Project" widget is visible below the list

---

## 2. UI Specification

### Initial View (Collapsed Projects)

```
┌─────────────────────────────────────────────┐
│  ContextKeep Projects                       │
├─────────────────────────────────────────────┤
│                                             │
│  [+] KJBot                                  │
│  [+] TaskFlow                               │
│  [+] WeatherAPI                             │
│                                             │
├─────────────────────────────────────────────┤
│  [+ Create New Project]                     │
└─────────────────────────────────────────────┘
```

### Expanded Project View

```
┌─────────────────────────────────────────────┐
│  ContextKeep Projects                       │
├─────────────────────────────────────────────┤
│                                             │
│  [-] KJBot                                  │
│      Repository: kjbot                      │
│      Description: Karaoke DJ system with    │
│                   queue management          │
│                                             │
│  [+] TaskFlow                               │
│  [+] WeatherAPI                             │
│                                             │
├─────────────────────────────────────────────┤
│  [+ Create New Project]                     │
└─────────────────────────────────────────────┘
```

### Empty State

```
┌─────────────────────────────────────────────┐
│  ContextKeep Projects                       │
├─────────────────────────────────────────────┤
│                                             │
│  No projects found.                         │
│  Create your first project to get started. │
│                                             │
├─────────────────────────────────────────────┤
│  [+ Create New Project]                     │
└─────────────────────────────────────────────┘
```

### UI Behavior

- **Click project name**: Opens project view (UC-002 or later)
- **Click [+] icon**: Expands to show repo_name and description
- **Click [-] icon**: Collapses to show only project_name
- **Click "Create New Project"**: Opens project creation flow (future UC)

### Theme

- Dark gray/black night theme (matching VS Code and Claude.ai)
- Consistent with existing ContextKeep UI palette

---

## 3. API Contracts

### GET /api/projects

**Description**: List all valid ContextKeep projects

**Request**: None

**Response**: 200 OK

```json
{
  "projects": [
    {
      "project_name": "KJBot",
      "repo_name": "kjbot",
      "description": "Karaoke DJ system with queue management",
      "created_at": "2025-11-15T10:30:00Z"
    },
    {
      "project_name": "TaskFlow",
      "repo_name": "taskflow",
      "description": "Workflow automation service",
      "created_at": "2025-11-14T15:22:00Z"
    },
    {
      "project_name": "WeatherAPI",
      "repo_name": "weather-api",
      "description": "Real-time weather data aggregation",
      "created_at": "2025-11-13T09:15:00Z"
    }
  ]
}
```

**Response**: 200 OK (Empty State)

```json
{
  "projects": []
}
```

**Error Responses**: None expected for this endpoint (always returns 200)

**Sorting**: Projects sorted alphabetically by `project_name` (case-insensitive)

---

## 4. Module Architecture

### Module Interaction Flow

```
Frontend
    │
    │ HTTP GET /api/projects
    ▼
projects/api.py (FastAPI Router)
    │
    │ list_projects()
    ▼
projects/service.py (Business Logic)
    │
    │ list_directories(path)
    │ read_file(path)
    ▼
files/service.py (File Operations)
    │
    │ OS/filesystem calls
    ▼
File System (~/.contextkeep-projects/)
```

### Module: `projects`

**Purpose**: Manage project lifecycle and metadata

**Location**: `backend/modules/projects/`

**Files**:
- `api.py` - FastAPI router with HTTP endpoints
- `service.py` - Business logic for project operations
- `models.py` - Pydantic schemas for project data
- `tests/` - Unit and integration tests

**Public Interface** (`service.py`):
```python
async def list_projects() -> List[ProjectSummary]:
    """
    List all valid ContextKeep projects.
    
    Returns:
        List of ProjectSummary objects, sorted by project_name.
        Projects without valid .contextkeep/project.json are excluded.
    """
```

### Module: `files`

**Purpose**: Low-level file system operations

**Location**: `backend/modules/files/`

**Files**:
- `api.py` - FastAPI router (future: file browser endpoints)
- `service.py` - File I/O operations
- `models.py` - File operation models
- `tests/` - Unit tests

**Public Interface** (`service.py`):
```python
def list_directories(base_path: Path) -> List[Path]:
    """
    List all directories within a base path.
    
    Args:
        base_path: Directory to scan
        
    Returns:
        List of Path objects for subdirectories (non-recursive)
    """

def read_json_file(file_path: Path) -> dict:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON as dict
        
    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If file is not valid JSON
    """
```

---

## 5. Data Models

### Project Metadata File

**Location**: `<project_root>/.contextkeep/project.json`

**Schema**:
```json
{
  "project_name": "KJBot",
  "repo_name": "kjbot",
  "description": "Karaoke DJ system with queue management",
  "created_at": "2025-11-15T10:30:00Z",
  "contextkeep_version": "0.1.0"
}
```

### Pydantic Models

**File**: `backend/modules/projects/models.py`

```python
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
```

---

## 6. Test Cases

### Test Organization

All tests are centralized in `backend/tests/` for clear separation from production code and easy exclusion from Electron builds.

```
backend/tests/
├── unit/                      # Fast, isolated, mocked dependencies
│   ├── files/
│   │   └── test_file_service.py
│   └── projects/
│       ├── test_models.py
│       ├── test_service.py    # Mocks file_service calls
│       └── test_api.py        # Mocks service layer
│
└── integration/               # Slower, uses real files (temp dirs)
    └── projects/
        └── test_api.py        # Full stack: API → service → file_service
```

### Unit Tests

#### Module: `files`

**File**: `backend/tests/unit/files/test_file_service.py`

```python
import pytest
from pathlib import Path
import tempfile
import json
from backend.modules.files.service import list_directories, read_json_file

def test_list_directories_empty():
    """TC-F1: Empty directory returns empty list"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = list_directories(Path(tmpdir))
        assert result == []

def test_list_directories_has_subdirs():
    """TC-F2: Returns list of subdirectories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        (base / "project1").mkdir()
        (base / "project2").mkdir()
        (base / "project3").mkdir()
        
        result = list_directories(base)
        assert len(result) == 3
        assert all(isinstance(p, Path) for p in result)

def test_list_directories_ignores_files():
    """TC-F3: Only returns directories, not files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        (base / "project1").mkdir()
        (base / "file.txt").touch()
        
        result = list_directories(base)
        assert len(result) == 1
        assert result[0].name == "project1"

def test_read_json_file_valid():
    """TC-F4: Valid JSON file is parsed correctly"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"key": "value"}, f)
        f.flush()
        
        result = read_json_file(Path(f.name))
        assert result == {"key": "value"}

def test_read_json_file_not_found():
    """TC-F5: FileNotFoundError for missing file"""
    with pytest.raises(FileNotFoundError):
        read_json_file(Path("/nonexistent/file.json"))

def test_read_json_file_invalid_json():
    """TC-F6: JSONDecodeError for malformed JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json")
        f.flush()
        
        with pytest.raises(json.JSONDecodeError):
            read_json_file(Path(f.name))
```

#### Module: `projects`

**File**: `backend/tests/unit/projects/test_models.py`

```python
import pytest
from datetime import datetime
from pydantic import ValidationError
from backend.modules.projects.models import (
    ProjectMetadata, ProjectSummary, ProjectListResponse
)

def test_project_metadata_valid():
    """TC-M1: Valid ProjectMetadata creation"""
    data = {
        "project_name": "TestProject",
        "repo_name": "test-project",
        "description": "A test project",
        "created_at": datetime.now()
    }
    project = ProjectMetadata(**data)
    assert project.project_name == "TestProject"
    assert project.contextkeep_version == "0.1.0"

def test_project_metadata_missing_required():
    """TC-M2: ValidationError for missing required fields"""
    with pytest.raises(ValidationError):
        ProjectMetadata(project_name="Test")

def test_project_summary_valid():
    """TC-M3: Valid ProjectSummary creation"""
    summary = ProjectSummary(
        project_name="Test",
        repo_name="test",
        description="A test",
        created_at=datetime.now()
    )
    assert summary.project_name == "Test"

def test_project_list_response_empty():
    """TC-M4: Empty project list"""
    response = ProjectListResponse()
    assert response.projects == []

def test_project_list_response_with_projects():
    """TC-M5: Response with multiple projects"""
    projects = [
        ProjectSummary(
            project_name="A",
            repo_name="a",
            description="First",
            created_at=datetime.now()
        ),
        ProjectSummary(
            project_name="B",
            repo_name="b",
            description="Second",
            created_at=datetime.now()
        )
    ]
    response = ProjectListResponse(projects=projects)
    assert len(response.projects) == 2
```

**File**: `backend/tests/unit/projects/test_service.py`

```python
import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime
from backend.modules.projects.service import list_projects
from backend.modules.projects.models import ProjectSummary

@pytest.fixture
def mock_file_service():
    """Fixture to mock file_service module"""
    with patch('backend.modules.projects.service.file_service') as mock:
        yield mock

def test_list_projects_empty_directory(mock_file_service):
    """TC-P1: Empty directory returns empty list"""
    mock_file_service.list_directories.return_value = []
    
    result = list_projects(Path("/test"))
    assert result == []

def test_list_projects_three_valid_projects(mock_file_service):
    """TC-P2: Three valid projects sorted alphabetically"""
    # Mock directory listing
    mock_file_service.list_directories.return_value = [
        Path("/test/zebra"),
        Path("/test/alpha"),
        Path("/test/beta")
    ]
    
    # Mock JSON reading for each project
    def mock_read_json(path):
        project_name = path.parent.name
        return {
            "project_name": project_name.capitalize(),
            "repo_name": project_name,
            "description": f"Description for {project_name}",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 3
    assert result[0].project_name == "Alpha"
    assert result[1].project_name == "Beta"
    assert result[2].project_name == "Zebra"

def test_list_projects_skip_invalid(mock_file_service):
    """TC-P3: Skip directories without .contextkeep/project.json"""
    mock_file_service.list_directories.return_value = [
        Path("/test/valid1"),
        Path("/test/invalid"),
        Path("/test/valid2")
    ]
    
    def mock_read_json(path):
        if "invalid" in str(path):
            raise FileNotFoundError("No project.json")
        project_name = path.parent.name
        return {
            "project_name": project_name.capitalize(),
            "repo_name": project_name,
            "description": f"Description for {project_name}",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 2
    assert all("Valid" in p.project_name for p in result)

def test_list_projects_skip_malformed_json(mock_file_service):
    """TC-P4: Skip projects with malformed JSON"""
    mock_file_service.list_directories.return_value = [
        Path("/test/good"),
        Path("/test/bad")
    ]
    
    def mock_read_json(path):
        if "bad" in str(path):
            raise json.JSONDecodeError("Invalid JSON", "", 0)
        return {
            "project_name": "Good",
            "repo_name": "good",
            "description": "A good project",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 1
    assert result[0].project_name == "Good"
```

**File**: `backend/tests/unit/projects/test_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime
from backend.main import app
from backend.modules.projects.models import ProjectSummary

client = TestClient(app)

@patch('backend.modules.projects.api.list_projects')
def test_get_projects_success(mock_list_projects):
    """TC-P5: GET /api/projects returns projects from service"""
    mock_list_projects.return_value = [
        ProjectSummary(
            project_name="Project A",
            repo_name="project-a",
            description="First project",
            created_at=datetime.now()
        ),
        ProjectSummary(
            project_name="Project B",
            repo_name="project-b",
            description="Second project",
            created_at=datetime.now()
        )
    ]
    
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["projects"]) == 2
    assert data["projects"][0]["project_name"] == "Project A"

@patch('backend.modules.projects.api.list_projects')
def test_get_projects_empty(mock_list_projects):
    """TC-P6: Empty project list returns empty array"""
    mock_list_projects.return_value = []
    
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    assert data["projects"] == []
```

### Integration Test

**File**: `backend/tests/integration/projects/test_api.py`

```python
import pytest
import tempfile
import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

client = TestClient(app)

@pytest.fixture
def temp_projects_dir():
    """Create temporary projects directory with fixtures"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create valid project 1
        p1 = base / "kjbot"
        (p1 / ".contextkeep").mkdir(parents=True)
        with open(p1 / ".contextkeep" / "project.json", "w") as f:
            json.dump({
                "project_name": "KJBot",
                "repo_name": "kjbot",
                "description": "Karaoke system",
                "created_at": "2025-11-15T10:00:00Z"
            }, f)
        
        # Create valid project 2
        p2 = base / "taskflow"
        (p2 / ".contextkeep").mkdir(parents=True)
        with open(p2 / ".contextkeep" / "project.json", "w") as f:
            json.dump({
                "project_name": "TaskFlow",
                "repo_name": "taskflow",
                "description": "Workflow automation",
                "created_at": "2025-11-14T10:00:00Z"
            }, f)
        
        # Create invalid project (no .contextkeep)
        p3 = base / "invalid"
        p3.mkdir()
        
        # Temporarily override settings
        original_base = settings.projects_base_dir
        settings.projects_base_dir = base
        
        yield base
        
        settings.projects_base_dir = original_base

def test_get_projects_integration(temp_projects_dir):
    """TC-I1: Full integration test with real file system"""
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have 2 valid projects (alphabetically sorted)
    assert len(data["projects"]) == 2
    assert data["projects"][0]["project_name"] == "KJBot"
    assert data["projects"][0]["repo_name"] == "kjbot"
    assert data["projects"][1]["project_name"] == "TaskFlow"
    assert data["projects"][1]["repo_name"] == "taskflow"
```

---

## 7. Implementation Notes

### Error Handling

**Philosophy**: Graceful degradation
- Invalid projects are silently skipped (logged, not shown to user)
- The app never crashes due to malformed project data
- Empty state is a valid, expected UI state

**Specific Behaviors**:
- Missing `.contextkeep/project.json` → skip directory
- Malformed JSON → skip project, log warning
- Missing fields in JSON → skip project, log warning
- File read errors → skip project, log error

### Performance

- **Lazy loading**: For future UCs, consider pagination if project count > 100
- **Caching**: Not needed for MVP (projects rarely change during a session)
- **File I/O**: All file operations are synchronous (acceptable for local FS)

### Security

- **Path traversal**: All paths validated to be within `projects_base_dir`
- **Symlinks**: Not followed if they escape base directory
- **File permissions**: Respects OS-level permissions

### Future Enhancements (Not in This UC)

- Search/filter projects
- Sort by: name, created date, last modified
- Project icons/avatars
- Project tags/categories
- Bulk operations (archive, delete)

---

## 8. Code Structure

### 8.1 Backend Files

#### File: `backend/config.py`

```python
"""
Application configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """App-wide settings"""
    
    # Project storage
    projects_base_dir: Path = Path.home() / ".contextkeep-projects"
    
    # API settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_prefix = "CONTEXTKEEP_"

settings = Settings()

# Ensure base directory exists
settings.projects_base_dir.mkdir(parents=True, exist_ok=True)
```

---

#### File: `backend/modules/files/models.py`

```python
"""
Data models for file operations
"""
from pydantic import BaseModel
from pathlib import Path
from typing import List

class DirectoryListing(BaseModel):
    """Result of listing directory contents"""
    base_path: Path
    directories: List[Path]
    
class FileContent(BaseModel):
    """Content read from a file"""
    path: Path
    content: str
```

---

#### File: `backend/modules/files/service.py`

```python
"""
Low-level file system operations
"""
from pathlib import Path
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

def list_directories(base_path: Path) -> List[Path]:
    """
    List all immediate subdirectories in a path.
    
    Args:
        base_path: Directory to scan
        
    Returns:
        List of Path objects for subdirectories (non-recursive)
    """
    if not base_path.exists():
        logger.warning(f"Base path does not exist: {base_path}")
        return []
    
    if not base_path.is_dir():
        logger.warning(f"Path is not a directory: {base_path}")
        return []
    
    try:
        return [p for p in base_path.iterdir() if p.is_dir()]
    except PermissionError:
        logger.error(f"Permission denied reading directory: {base_path}")
        return []

def read_json_file(file_path: Path) -> dict:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON as dict
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

---

#### File: `backend/modules/projects/models.py`

```python
"""
Project data models
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
```

---

#### File: `backend/modules/projects/service.py`

```python
"""
Project business logic
"""
from pathlib import Path
from typing import List
import logging
import json
from backend.modules.files import service as file_service
from backend.modules.projects.models import ProjectMetadata, ProjectSummary
from backend.config import settings

logger = logging.getLogger(__name__)

def list_projects(base_dir: Path = None) -> List[ProjectSummary]:
    """
    List all valid ContextKeep projects.
    
    Args:
        base_dir: Base directory to search (defaults to settings.projects_base_dir)
        
    Returns:
        List of ProjectSummary objects, sorted alphabetically by project_name
    """
    if base_dir is None:
        base_dir = settings.projects_base_dir
    
    projects = []
    
    # Get all directories
    directories = file_service.list_directories(base_dir)
    
    for project_dir in directories:
        try:
            # Try to read project.json
            project_json_path = project_dir / ".contextkeep" / "project.json"
            metadata_dict = file_service.read_json_file(project_json_path)
            
            # Validate against schema
            metadata = ProjectMetadata(**metadata_dict)
            
            # Create summary
            summary = ProjectSummary(
                project_name=metadata.project_name,
                repo_name=metadata.repo_name,
                description=metadata.description,
                created_at=metadata.created_at
            )
            projects.append(summary)
            
        except FileNotFoundError:
            # Not a ContextKeep project (no .contextkeep/project.json)
            logger.debug(f"Skipping {project_dir.name}: no project.json found")
            continue
            
        except json.JSONDecodeError as e:
            # Malformed JSON
            logger.warning(f"Skipping {project_dir.name}: malformed JSON - {e}")
            continue
            
        except Exception as e:
            # Other validation errors
            logger.warning(f"Skipping {project_dir.name}: {e}")
            continue
    
    # Sort alphabetically by project_name (case-insensitive)
    projects.sort(key=lambda p: p.project_name.lower())
    
    return projects
```

---

#### File: `backend/modules/projects/api.py`

```python
"""
FastAPI routes for project operations
"""
from fastapi import APIRouter, HTTPException
from backend.modules.projects.service import list_projects
from backend.modules.projects.models import ProjectListResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=ProjectListResponse)
async def get_projects():
    """
    List all ContextKeep projects.
    
    Returns:
        ProjectListResponse with list of projects
    """
    try:
        projects = list_projects()
        return ProjectListResponse(projects=projects)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

#### File: `backend/main.py`

```python
"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.modules.projects.api import router as projects_router

app = FastAPI(
    title="ContextKeep API",
    version="0.1.0",
    description="Backend API for ContextKeep project management"
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(projects_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "ContextKeep API"}
```

---

### 8.2 Frontend Files (JavaScript)

#### File: `frontend/package.json`

```json
{
  "name": "contextkeep-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.2"
  }
}
```

---

#### File: `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});
```

---

#### File: `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ContextKeep</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

#### File: `frontend/src/main.jsx`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

#### File: `frontend/src/index.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #1e1e1e;
  color: #d4d4d4;
}
```

---

#### File: `frontend/src/api/client.js`

```javascript
/**
 * API client using native fetch
 */

const API_BASE_URL = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  async listProjects() {
    const response = await fetch(`${API_BASE_URL}/projects`);
    return handleResponse(response);
  }
};
```

---

#### File: `frontend/src/components/ProjectList/ProjectItem.jsx`

```javascript
/**
 * Individual project item component
 */
import React, { useState } from 'react';

function ProjectItem({ project, onProjectClick }) {
  const [expanded, setExpanded] = useState(false);

  const handleToggleExpand = (e) => {
    e.stopPropagation();
    setExpanded(!expanded);
  };

  const handleProjectClick = () => {
    onProjectClick(project.repo_name);
  };

  return (
    <div className="project-item">
      <div className="project-header" onClick={handleProjectClick}>
        <span onClick={handleToggleExpand} className="expand-icon">
          {expanded ? '[-]' : '[+]'}
        </span>
        <span className="project-name">{project.project_name}</span>
      </div>
      
      {expanded && (
        <div className="project-details">
          <div className="project-detail-row">
            <span className="detail-label">Repository:</span>
            <span className="detail-value">{project.repo_name}</span>
          </div>
          <div className="project-detail-row">
            <span className="detail-label">Description:</span>
            <span className="detail-value">{project.description}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectItem;
```

---

#### File: `frontend/src/components/ProjectList/CreateProjectWidget.jsx`

```javascript
/**
 * Create new project widget
 */
import React from 'react';

function CreateProjectWidget({ onCreate }) {
  return (
    <div className="create-project-widget" onClick={onCreate}>
      <span className="create-icon">[+]</span>
      <span className="create-text">Create New Project</span>
    </div>
  );
}

export default CreateProjectWidget;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.jsx`

```javascript
/**
 * Main project list component
 */
import React, { useEffect, useState } from 'react';
import { api } from '../../api/client';
import ProjectItem from './ProjectItem';
import CreateProjectWidget from './CreateProjectWidget';
import './ProjectList.css';

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.listProjects();
      setProjects(data.projects);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (repoName) => {
    console.log('Project clicked:', repoName);
    // TODO: Navigate to project detail view
  };

  const handleCreateProject = () => {
    console.log('Create new project clicked');
    // TODO: Open create project dialog
  };

  if (loading) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div>Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="project-list-container">
      <div className="project-list-header">
        <h2>ContextKeep Projects</h2>
      </div>

      <div className="project-list-content">
        {projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects found.</p>
            <p>Create your first project to get started.</p>
          </div>
        ) : (
          projects.map((project) => (
            <ProjectItem
              key={project.repo_name}
              project={project}
              onProjectClick={handleProjectClick}
            />
          ))
        )}
      </div>

      <div className="project-list-footer">
        <CreateProjectWidget onCreate={handleCreateProject} />
      </div>
    </div>
  );
}

export default ProjectList;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.css`

```css
/**
 * Project list styles - Dark theme matching VS Code
 */

.project-list-container {
  background-color: #1e1e1e;
  color: #d4d4d4;
  min-height: 100vh;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.project-list-header h2 {
  color: #cccccc;
  margin-bottom: 20px;
  border-bottom: 1px solid #3c3c3c;
  padding-bottom: 10px;
}

.project-list-content {
  margin-bottom: 20px;
}

/* Project Item */
.project-item {
  margin-bottom: 10px;
  background-color: #252526;
  border: 1px solid #3c3c3c;
  border-radius: 4px;
  padding: 10px;
  transition: background-color 0.2s;
}

.project-item:hover {
  background-color: #2d2d30;
}

.project-header {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.expand-icon {
  margin-right: 8px;
  cursor: pointer;
  user-select: none;
  font-weight: bold;
  color: #cccccc;
}

.project-name {
  color: #4ec9b0;
  font-weight: 500;
}

.project-details {
  margin-top: 10px;
  padding-left: 24px;
  font-size: 0.9em;
  color: #9cdcfe;
}

.project-detail-row {
  margin-bottom: 5px;
}

.detail-label {
  color: #808080;
  margin-right: 8px;
}

.detail-value {
  color: #d4d4d4;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px;
  color: #808080;
}

.empty-state p {
  margin: 10px 0;
}

/* Create Project Widget */
.project-list-footer {
  border-top: 1px solid #3c3c3c;
  padding-top: 20px;
}

.create-project-widget {
  background-color: #0e639c;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: background-color 0.2s;
}

.create-project-widget:hover {
  background-color: #1177bb;
}

.create-icon {
  margin-right: 8px;
  font-weight: bold;
}

.create-text {
  font-weight: 500;
}

/* Error State */
.error {
  color: #f48771;
  padding: 20px;
}

/* Loading State */
.project-list-container > div {
  color: #d4d4d4;
}
```

---

#### File: `frontend/src/App.jsx`

```javascript
import React from 'react';
import ProjectList from './components/ProjectList/ProjectList';
import './App.css';

function App() {
  return (
    <div className="App">
      <ProjectList />
    </div>
  );
}

export default App;
```

---

#### File: `frontend/src/App.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #1e1e1e;
}

.App {
  min-height: 100vh;
}
```

---

## 9. Implementation Guide

### Implementation Strategy

Work in **chunks** - each chunk contains related code files plus tests. Run pytest after each chunk to ensure green tests before moving forward. If you hit red, iterate with Claude using the stack trace.

**Chunk Order**: Build from foundation up (models → low-level services → high-level services → API → frontend)

### Chunk 0: Project Setup

**Goal**: Create project structure and verify tooling works

**Backend Setup**:
```bash
# Create module directory structure
mkdir -p backend/modules/files
mkdir -p backend/modules/projects

# Create centralized test directory structure
mkdir -p backend/tests/unit/files
mkdir -p backend/tests/unit/projects
mkdir -p backend/tests/integration
mkdir -p backend/tests/fixtures/projects

# Create __init__.py files for modules
touch backend/modules/__init__.py
touch backend/modules/files/__init__.py
touch backend/modules/projects/__init__.py

# Create __init__.py files for tests (helps with imports)
touch backend/tests/__init__.py
touch backend/tests/unit/__init__.py
touch backend/tests/unit/files/__init__.py
touch backend/tests/unit/projects/__init__.py
touch backend/tests/integration/__init__.py

# Install dependencies
cd backend
pip install -e ".[dev]"
```

**Frontend Setup**:
```bash
# Create frontend with Vite
cd frontend
npm install

# Create directory structure
mkdir -p src/components/ProjectList
mkdir -p src/api
```

**Verification**:
```bash
# Backend: Should pass (no tests yet)
cd backend && pytest

# Frontend: Should start
cd frontend && npm run dev
```

---

### Chunk 1: Files Module - Models and Service

**Files**:
- `backend/modules/files/models.py`
- `backend/modules/files/service.py`
- `backend/tests/unit/files/test_file_service.py`

**Tests to Pass**:
- TC-F1: List directories in empty directory
- TC-F2: List directories with subdirectories
- TC-F3: List directories ignores files
- TC-F4: Read valid JSON file
- TC-F5: Read JSON file - file not found
- TC-F6: Read JSON file - invalid JSON

**Run**:
```bash
cd backend
pytest tests/unit/files/test_file_service.py -v
```

**Expected**: 6/6 tests passing ✅

---

### Chunk 2: Projects Module - Models

**Files**:
- `backend/modules/projects/models.py`
- `backend/tests/unit/projects/test_models.py`

**Tests to Pass**:
- Model validation tests (Pydantic automatically validates)

**Run**:
```bash
cd backend
pytest tests/unit/projects/test_models.py -v
```

**Expected**: All model tests passing ✅

---

### Chunk 3: Projects Module - Service

**Files**:
- `backend/modules/projects/service.py`
- `backend/tests/unit/projects/test_service.py`

**Tests to Pass**:
- TC-P1: List projects - empty directory
- TC-P2: List projects - three valid projects
- TC-P3: List projects - skip invalid project
- TC-P4: List projects - skip malformed JSON

**Run**:
```bash
cd backend
pytest tests/unit/projects/test_service.py -v
```

**Expected**: 4/4 tests passing ✅

---

### Chunk 4: Projects Module - API Integration

**Files**:
- `backend/config.py`
- `backend/main.py`
- `backend/modules/projects/api.py`
- `backend/tests/conftest.py`
- `backend/tests/unit/projects/test_api.py`
- `backend/tests/integration/test_list_projects_flow.py`
- `backend/tests/fixtures/projects/` (create real test data)

**Tests to Pass**:
- TC-P5: API unit test (mocked service)
- TC-I1: Integration test (real files, no mocks)

**Run**:
```bash
cd backend
# Run API unit test
pytest tests/unit/projects/test_api.py -v

# Run integration test (uses real fixture files)
pytest tests/integration/test_list_projects_flow.py -v
```

**Expected**: 2/2 tests passing ✅

**Manual Verification**:
```bash
# Start backend
uvicorn main:app --reload

# In another terminal
curl http://localhost:8000/api/projects
```

---

### Chunk 5: Frontend - API Client

**Files**:
- `frontend/src/api/client.js`

**Manual Verification**:
- File compiles without errors
- No console errors in browser

---

### Chunk 6: Frontend - Components

**Files**:
- `frontend/src/components/ProjectList/ProjectItem.jsx`
- `frontend/src/components/ProjectList/CreateProjectWidget.jsx`
- `frontend/src/components/ProjectList/ProjectList.jsx`
- `frontend/src/components/ProjectList/ProjectList.css`
- `frontend/src/App.jsx`
- `frontend/src/App.css`
- `frontend/src/main.jsx`

**Manual Verification**:
- UI renders project list
- Expand/collapse works
- Dark theme looks correct
- No console errors

---

## Implementation Checklist

Follow the chunked implementation guide above. After each chunk, verify tests pass before moving forward.

- [ ] **Chunk 0**: Project setup complete
- [ ] **Chunk 1**: Files module (6 tests passing)
- [ ] **Chunk 2**: Projects models (model validation passing)
- [ ] **Chunk 3**: Projects service (4 tests passing)
- [ ] **Chunk 4**: API integration (2 tests passing, curl works)
- [ ] **Chunk 5**: Frontend API client (compiles)
- [ ] **Chunk 6**: Frontend components (UI works)
- [ ] **Final**: End-to-end manual verification complete

---

## Code Files

The following sections contain the complete implementation code for UC-001, organized by chunk.

---

### Chunk 1: Files Module

#### File: `backend/modules/files/models.py`

```python
"""
Data models for file operations
"""
from pydantic import BaseModel
from pathlib import Path
from typing import List

class DirectoryListing(BaseModel):
    """Result of listing directory contents"""
    base_path: Path
    directories: List[Path]
    
class FileContent(BaseModel):
    """Content read from a file"""
    path: Path
    content: str
```

---

#### File: `backend/modules/files/service.py`

```python
"""
Low-level file system operations
"""
from pathlib import Path
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

def list_directories(base_path: Path) -> List[Path]:
    """
    List all immediate subdirectories in a path.
    
    Args:
        base_path: Directory to scan
        
    Returns:
        List of Path objects for subdirectories (non-recursive)
    """
    if not base_path.exists():
        logger.warning(f"Base path does not exist: {base_path}")
        return []
    
    if not base_path.is_dir():
        logger.warning(f"Path is not a directory: {base_path}")
        return []
    
    try:
        return [p for p in base_path.iterdir() if p.is_dir()]
    except PermissionError:
        logger.error(f"Permission denied reading directory: {base_path}")
        return []

def read_json_file(file_path: Path) -> dict:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON as dict
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

---

#### File: `backend/tests/unit/files/test_file_service.py`

```python
import pytest
from pathlib import Path
import tempfile
import json
from backend.modules.files.service import list_directories, read_json_file

def test_list_directories_empty():
    """TC-F1: Empty directory returns empty list"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = list_directories(Path(tmpdir))
        assert result == []

def test_list_directories_has_subdirs():
    """TC-F2: Returns list of subdirectories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        (base / "project1").mkdir()
        (base / "project2").mkdir()
        (base / "project3").mkdir()
        
        result = list_directories(base)
        assert len(result) == 3
        assert all(isinstance(p, Path) for p in result)

def test_list_directories_ignores_files():
    """TC-F3: Only returns directories, not files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        (base / "project1").mkdir()
        (base / "file.txt").touch()
        
        result = list_directories(base)
        assert len(result) == 1
        assert result[0].name == "project1"

def test_read_json_file_valid():
    """TC-F4: Valid JSON file is parsed correctly"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"key": "value"}, f)
        f.flush()
        
        result = read_json_file(Path(f.name))
        assert result == {"key": "value"}

def test_read_json_file_not_found():
    """TC-F5: FileNotFoundError for missing file"""
    with pytest.raises(FileNotFoundError):
        read_json_file(Path("/nonexistent/file.json"))

def test_read_json_file_invalid_json():
    """TC-F6: JSONDecodeError for malformed JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json")
        f.flush()
        
        with pytest.raises(json.JSONDecodeError):
            read_json_file(Path(f.name))
```

---

### Chunk 2: Projects Module - Models

#### File: `backend/modules/projects/models.py`

```python
"""
Project data models
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
```

---

#### File: `backend/tests/unit/projects/test_models.py`

```python
import pytest
from datetime import datetime
from pydantic import ValidationError
from backend.modules.projects.models import (
    ProjectMetadata, ProjectSummary, ProjectListResponse
)

def test_project_metadata_valid():
    """TC-M1: Valid ProjectMetadata creation"""
    data = {
        "project_name": "TestProject",
        "repo_name": "test-project",
        "description": "A test project",
        "created_at": datetime.now()
    }
    project = ProjectMetadata(**data)
    assert project.project_name == "TestProject"
    assert project.contextkeep_version == "0.1.0"

def test_project_metadata_missing_required():
    """TC-M2: ValidationError for missing required fields"""
    with pytest.raises(ValidationError):
        ProjectMetadata(project_name="Test")

def test_project_summary_valid():
    """TC-M3: Valid ProjectSummary creation"""
    summary = ProjectSummary(
        project_name="Test",
        repo_name="test",
        description="A test",
        created_at=datetime.now()
    )
    assert summary.project_name == "Test"

def test_project_list_response_empty():
    """TC-M4: Empty project list"""
    response = ProjectListResponse()
    assert response.projects == []

def test_project_list_response_with_projects():
    """TC-M5: Response with multiple projects"""
    projects = [
        ProjectSummary(
            project_name="A",
            repo_name="a",
            description="First",
            created_at=datetime.now()
        ),
        ProjectSummary(
            project_name="B",
            repo_name="b",
            description="Second",
            created_at=datetime.now()
        )
    ]
    response = ProjectListResponse(projects=projects)
    assert len(response.projects) == 2
```

---

### Chunk 3: Projects Module - Service

#### File: `backend/modules/projects/service.py`

```python
"""
Project business logic
"""
from pathlib import Path
from typing import List
import logging
import json
from backend.modules.files import service as file_service
from backend.modules.projects.models import ProjectMetadata, ProjectSummary
from backend.config import settings

logger = logging.getLogger(__name__)

def list_projects(base_dir: Path = None) -> List[ProjectSummary]:
    """
    List all valid ContextKeep projects.
    
    Args:
        base_dir: Base directory to search (defaults to settings.projects_base_dir)
        
    Returns:
        List of ProjectSummary objects, sorted alphabetically by project_name
    """
    if base_dir is None:
        base_dir = settings.projects_base_dir
    
    projects = []
    
    # Get all directories
    directories = file_service.list_directories(base_dir)
    
    for project_dir in directories:
        try:
            # Try to read project.json
            project_json_path = project_dir / ".contextkeep" / "project.json"
            metadata_dict = file_service.read_json_file(project_json_path)
            
            # Validate against schema
            metadata = ProjectMetadata(**metadata_dict)
            
            # Create summary
            summary = ProjectSummary(
                project_name=metadata.project_name,
                repo_name=metadata.repo_name,
                description=metadata.description,
                created_at=metadata.created_at
            )
            projects.append(summary)
            
        except FileNotFoundError:
            # Not a ContextKeep project (no .contextkeep/project.json)
            logger.debug(f"Skipping {project_dir.name}: no project.json found")
            continue
            
        except json.JSONDecodeError as e:
            # Malformed JSON
            logger.warning(f"Skipping {project_dir.name}: malformed JSON - {e}")
            continue
            
        except Exception as e:
            # Other validation errors
            logger.warning(f"Skipping {project_dir.name}: {e}")
            continue
    
    # Sort alphabetically by project_name (case-insensitive)
    projects.sort(key=lambda p: p.project_name.lower())
    
    return projects
```

---

#### File: `backend/tests/unit/projects/test_service.py`

```python
import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime
from backend.modules.projects.service import list_projects
from backend.modules.projects.models import ProjectSummary

@pytest.fixture
def mock_file_service():
    """Fixture to mock file_service module"""
    with patch('backend.modules.projects.service.file_service') as mock:
        yield mock

def test_list_projects_empty_directory(mock_file_service):
    """TC-P1: Empty directory returns empty list"""
    mock_file_service.list_directories.return_value = []
    
    result = list_projects(Path("/test"))
    assert result == []

def test_list_projects_three_valid_projects(mock_file_service):
    """TC-P2: Three valid projects sorted alphabetically"""
    # Mock directory listing
    mock_file_service.list_directories.return_value = [
        Path("/test/zebra"),
        Path("/test/alpha"),
        Path("/test/beta")
    ]
    
    # Mock JSON reading for each project
    def mock_read_json(path):
        project_name = path.parent.name
        return {
            "project_name": project_name.capitalize(),
            "repo_name": project_name,
            "description": f"Description for {project_name}",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 3
    assert result[0].project_name == "Alpha"
    assert result[1].project_name == "Beta"
    assert result[2].project_name == "Zebra"

def test_list_projects_skip_invalid(mock_file_service):
    """TC-P3: Skip directories without .contextkeep/project.json"""
    mock_file_service.list_directories.return_value = [
        Path("/test/valid1"),
        Path("/test/invalid"),
        Path("/test/valid2")
    ]
    
    def mock_read_json(path):
        if "invalid" in str(path):
            raise FileNotFoundError("No project.json")
        project_name = path.parent.name
        return {
            "project_name": project_name.capitalize(),
            "repo_name": project_name,
            "description": f"Description for {project_name}",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 2
    assert all("Valid" in p.project_name for p in result)

def test_list_projects_skip_malformed_json(mock_file_service):
    """TC-P4: Skip projects with malformed JSON"""
    mock_file_service.list_directories.return_value = [
        Path("/test/good"),
        Path("/test/bad")
    ]
    
    def mock_read_json(path):
        if "bad" in str(path):
            raise json.JSONDecodeError("Invalid JSON", "", 0)
        return {
            "project_name": "Good",
            "repo_name": "good",
            "description": "A good project",
            "created_at": "2025-11-15T10:00:00Z"
        }
    
    mock_file_service.read_json_file.side_effect = mock_read_json
    
    result = list_projects(Path("/test"))
    
    assert len(result) == 1
    assert result[0].project_name == "Good"
```

---

### Chunk 4: Projects Module - API and Configuration

#### File: `backend/config.py`

```python
"""
Application configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """App-wide settings"""
    
    # Project storage
    projects_base_dir: Path = Path.home() / ".contextkeep-projects"
    
    # API settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_prefix = "CONTEXTKEEP_"

settings = Settings()

# Ensure base directory exists
settings.projects_base_dir.mkdir(parents=True, exist_ok=True)
```

---

#### File: `backend/modules/projects/api.py`

```python
"""
FastAPI routes for project operations
"""
from fastapi import APIRouter, HTTPException
from backend.modules.projects.service import list_projects
from backend.modules.projects.models import ProjectListResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=ProjectListResponse)
async def get_projects():
    """
    List all ContextKeep projects.
    
    Returns:
        ProjectListResponse with list of projects
    """
    try:
        projects = list_projects()
        return ProjectListResponse(projects=projects)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

#### File: `backend/main.py`

```python
"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.modules.projects.api import router as projects_router

app = FastAPI(
    title="ContextKeep API",
    version="0.1.0",
    description="Backend API for ContextKeep project management"
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(projects_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "ContextKeep API"}
```

---

#### File: `backend/tests/unit/projects/test_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime
from backend.main import app
from backend.modules.projects.models import ProjectSummary

client = TestClient(app)

@patch('backend.modules.projects.api.list_projects')
def test_get_projects_success(mock_list_projects):
    """TC-P5: GET /api/projects returns projects from service"""
    mock_list_projects.return_value = [
        ProjectSummary(
            project_name="Project A",
            repo_name="project-a",
            description="First project",
            created_at=datetime.now()
        ),
        ProjectSummary(
            project_name="Project B",
            repo_name="project-b",
            description="Second project",
            created_at=datetime.now()
        )
    ]
    
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["projects"]) == 2
    assert data["projects"][0]["project_name"] == "Project A"

@patch('backend.modules.projects.api.list_projects')
def test_get_projects_empty(mock_list_projects):
    """TC-P6: Empty project list returns empty array"""
    mock_list_projects.return_value = []
    
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    assert data["projects"] == []
```

---

#### File: `backend/tests/integration/projects/test_api.py`

```python
import pytest
import tempfile
import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

client = TestClient(app)

@pytest.fixture
def temp_projects_dir():
    """Create temporary projects directory with fixtures"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create valid project 1
        p1 = base / "kjbot"
        (p1 / ".contextkeep").mkdir(parents=True)
        with open(p1 / ".contextkeep" / "project.json", "w") as f:
            json.dump({
                "project_name": "KJBot",
                "repo_name": "kjbot",
                "description": "Karaoke system",
                "created_at": "2025-11-15T10:00:00Z"
            }, f)
        
        # Create valid project 2
        p2 = base / "taskflow"
        (p2 / ".contextkeep").mkdir(parents=True)
        with open(p2 / ".contextkeep" / "project.json", "w") as f:
            json.dump({
                "project_name": "TaskFlow",
                "repo_name": "taskflow",
                "description": "Workflow automation",
                "created_at": "2025-11-14T10:00:00Z"
            }, f)
        
        # Create invalid project (no .contextkeep)
        p3 = base / "invalid"
        p3.mkdir()
        
        # Temporarily override settings
        original_base = settings.projects_base_dir
        settings.projects_base_dir = base
        
        yield base
        
        settings.projects_base_dir = original_base

def test_get_projects_integration(temp_projects_dir):
    """TC-I1: Full integration test with real file system"""
    response = client.get("/api/projects")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have 2 valid projects (alphabetically sorted)
    assert len(data["projects"]) == 2
    assert data["projects"][0]["project_name"] == "KJBot"
    assert data["projects"][0]["repo_name"] == "kjbot"
    assert data["projects"][1]["project_name"] == "TaskFlow"
    assert data["projects"][1]["repo_name"] == "taskflow"
```

---

### Chunk 5: Frontend - API Client

#### File: `frontend/package.json`

```json
{
  "name": "contextkeep-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.2"
  }
}
```

---

#### File: `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});
```

---

#### File: `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ContextKeep</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

#### File: `frontend/src/main.jsx`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

#### File: `frontend/src/index.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #1e1e1e;
  color: #d4d4d4;
}
```

---

#### File: `frontend/src/api/client.js`

```javascript
/**
 * API client using native fetch
 */

const API_BASE_URL = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  async listProjects() {
    const response = await fetch(`${API_BASE_URL}/projects`);
    return handleResponse(response);
  }
};
```

---

### Chunk 6: Frontend - Components

#### File: `frontend/src/components/ProjectList/ProjectItem.jsx`

```javascript
/**
 * Individual project item component
 */
import React, { useState } from 'react';

function ProjectItem({ project, onProjectClick }) {
  const [expanded, setExpanded] = useState(false);

  const handleToggleExpand = (e) => {
    e.stopPropagation();
    setExpanded(!expanded);
  };

  const handleProjectClick = () => {
    onProjectClick(project.repo_name);
  };

  return (
    <div className="project-item">
      <div className="project-header" onClick={handleProjectClick}>
        <span onClick={handleToggleExpand} className="expand-icon">
          {expanded ? '[-]' : '[+]'}
        </span>
        <span className="project-name">{project.project_name}</span>
      </div>
      
      {expanded && (
        <div className="project-details">
          <div className="project-detail-row">
            <span className="detail-label">Repository:</span>
            <span className="detail-value">{project.repo_name}</span>
          </div>
          <div className="project-detail-row">
            <span className="detail-label">Description:</span>
            <span className="detail-value">{project.description}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectItem;
```

---

#### File: `frontend/src/components/ProjectList/CreateProjectWidget.jsx`

```javascript
/**
 * Create new project widget
 */
import React from 'react';

function CreateProjectWidget({ onCreate }) {
  return (
    <div className="create-project-widget" onClick={onCreate}>
      <span className="create-icon">[+]</span>
      <span className="create-text">Create New Project</span>
    </div>
  );
}

export default CreateProjectWidget;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.jsx`

```javascript
/**
 * Main project list component
 */
import React, { useEffect, useState } from 'react';
import { api } from '../../api/client';
import ProjectItem from './ProjectItem';
import CreateProjectWidget from './CreateProjectWidget';
import './ProjectList.css';

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.listProjects();
      setProjects(data.projects);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (repoName) => {
    console.log('Project clicked:', repoName);
    // TODO: Navigate to project detail view
  };

  const handleCreateProject = () => {
    console.log('Create new project clicked');
    // TODO: Open create project dialog
  };

  if (loading) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div>Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="project-list-container">
      <div className="project-list-header">
        <h2>ContextKeep Projects</h2>
      </div>

      <div className="project-list-content">
        {projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects found.</p>
            <p>Create your first project to get started.</p>
          </div>
        ) : (
          projects.map((project) => (
            <ProjectItem
              key={project.repo_name}
              project={project}
              onProjectClick={handleProjectClick}
            />
          ))
        )}
      </div>

      <div className="project-list-footer">
        <CreateProjectWidget onCreate={handleCreateProject} />
      </div>
    </div>
  );
}

export default ProjectList;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.css`

```css
/**
 * Project list styles - Dark theme matching VS Code
 */

.project-list-container {
  background-color: #1e1e1e;
  color: #d4d4d4;
  min-height: 100vh;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.project-list-header h2 {
  color: #cccccc;
  margin-bottom: 20px;
  border-bottom: 1px solid #3c3c3c;
  padding-bottom: 10px;
}

.project-list-content {
  margin-bottom: 20px;
}

/* Project Item */
.project-item {
  margin-bottom: 10px;
  background-color: #252526;
  border: 1px solid #3c3c3c;
  border-radius: 4px;
  padding: 10px;
  transition: background-color 0.2s;
}

.project-item:hover {
  background-color: #2d2d30;
}

.project-header {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.expand-icon {
  margin-right: 8px;
  cursor: pointer;
  user-select: none;
  font-weight: bold;
  color: #cccccc;
}

.project-name {
  color: #4ec9b0;
  font-weight: 500;
}

.project-details {
  margin-top: 10px;
  padding-left: 24px;
  font-size: 0.9em;
  color: #9cdcfe;
}

.project-detail-row {
  margin-bottom: 5px;
}

.detail-label {
  color: #808080;
  margin-right: 8px;
}

.detail-value {
  color: #d4d4d4;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px;
  color: #808080;
}

.empty-state p {
  margin: 10px 0;
}

/* Create Project Widget */
.project-list-footer {
  border-top: 1px solid #3c3c3c;
  padding-top: 20px;
}

.create-project-widget {
  background-color: #0e639c;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: background-color 0.2s;
}

.create-project-widget:hover {
  background-color: #1177bb;
}

.create-icon {
  margin-right: 8px;
  font-weight: bold;
}

.create-text {
  font-weight: 500;
}

/* Error State */
.error {
  color: #f48771;
  padding: 20px;
}

/* Loading State */
.project-list-container > div {
  color: #d4d4d4;
}
```

---

#### File: `frontend/src/App.jsx`

```javascript
import React from 'react';
import ProjectList from './components/ProjectList/ProjectList';
import './App.css';

function App() {
  return (
    <div className="App">
      <ProjectList />
    </div>
  );
}

export default App;
```

---

#### File: `frontend/src/App.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #1e1e1e;
}

.App {
  min-height: 100vh;
}
```

---

## 10. How to Run This Feature

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### First-Time Setup

1. **Clone repository**:
```bash
git clone <repo-url>
cd contextkeep
```

2. **Backend setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

3. **Frontend setup**:
```bash
cd frontend
npm install
```

4. **Create test projects** (optional):
```bash
mkdir -p ~/.contextkeep-projects/demo-project/.contextkeep
cat > ~/.contextkeep-projects/demo-project/.contextkeep/project.json << 'EOF'
{
  "project_name": "Demo Project",
  "repo_name": "demo-project",
  "description": "A demonstration project",
  "created_at": "2025-11-15T10:00:00Z",
  "contextkeep_version": "0.1.0"
}
EOF
```

### Running the Application

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Access the app**: http://localhost:5173

### Running Tests

**Backend tests**:
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=backend --cov-report=html
```

**Frontend** (future):
```bash
cd frontend
npm test
```

---

**End of UC-001 Specification**
