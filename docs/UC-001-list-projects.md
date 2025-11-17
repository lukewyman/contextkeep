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
├── integration/               # Real I/O, multiple components, no mocks
│   └── test_list_projects_flow.py
│
└── fixtures/
    └── projects/              # Real test project structures
        ├── kjbot/
        │   └── .contextkeep/
        │       └── project.json
        ├── taskflow/
        │   └── .contextkeep/
        │       └── project.json
        └── weather-api/
            └── .contextkeep/
                └── project.json
```

### Test Taxonomy

**Unit Tests** - Fast, isolated, mock all external dependencies:
- File I/O operations use `tmp_path` (pytest fixture, isolated filesystem)
- Service layer tests mock lower-level services
- API tests mock the service layer

**Integration Tests** - Real components working together, no mocks:
- Use real fixture files from `tests/fixtures/`
- Test full stack: API → Service → File I/O
- Verify end-to-end behavior

### Module: `files` - Test Cases

**File**: `tests/unit/files/test_file_service.py`

#### TC-F1: List directories in empty directory
```python
def test_list_directories_empty(tmp_path):
    """
    Given: An empty directory
    When: list_directories() is called
    Then: Returns empty list
    """
```

#### TC-F2: List directories with subdirectories
```python
def test_list_directories_with_subdirs(tmp_path):
    """
    Given: A directory with 3 subdirectories
    When: list_directories() is called
    Then: Returns list of 3 Path objects
    And: Paths are absolute paths to subdirectories
    And: Only immediate children are returned (not recursive)
    """
```

#### TC-F3: List directories ignores files
```python
def test_list_directories_ignores_files(tmp_path):
    """
    Given: A directory with 2 subdirs and 3 files
    When: list_directories() is called
    Then: Returns only the 2 subdirectories
    """
```

#### TC-F4: Read valid JSON file
```python
def test_read_json_file_valid(tmp_path):
    """
    Given: A valid JSON file
    When: read_json_file() is called
    Then: Returns parsed dict with correct data
    """
```

#### TC-F5: Read JSON file - file not found
```python
def test_read_json_file_not_found(tmp_path):
    """
    Given: A non-existent file path
    When: read_json_file() is called
    Then: Raises FileNotFoundError
    """
```

#### TC-F6: Read JSON file - invalid JSON
```python
def test_read_json_file_invalid_json(tmp_path):
    """
    Given: A file with invalid JSON content
    When: read_json_file() is called
    Then: Raises JSONDecodeError
    """
```

### Module: `projects` - Test Cases

**File**: `tests/unit/projects/test_project_service.py`

#### TC-P1: List projects - empty directory
```python
@patch('modules.files.service.list_directories')
def test_list_projects_empty(mock_list_dirs):
    """
    Given: contextkeep-projects directory is empty
    When: list_projects() is called
    Then: Returns empty list
    And: files.service.list_directories() was called once
    """
    mock_list_dirs.return_value = []
    
    result = await list_projects()
    
    assert result == []
    assert mock_list_dirs.call_count == 1
```

#### TC-P2: List projects - three valid projects
```python
@patch('modules.files.service.read_json_file')
@patch('modules.files.service.list_directories')
def test_list_projects_three_valid(mock_list_dirs, mock_read_json):
    """
    Given: contextkeep-projects has 3 project directories
    And: Each has valid .contextkeep/project.json
    When: list_projects() is called
    Then: Returns list of 3 ProjectSummary objects
    And: Projects are sorted alphabetically by project_name
    And: Each project has correct name, repo_name, description
    """
    # Mock setup
    mock_list_dirs.return_value = [
        Path('/home/user/contextkeep-projects/kjbot'),
        Path('/home/user/contextkeep-projects/taskflow'),
        Path('/home/user/contextkeep-projects/weather-api')
    ]
    
    mock_read_json.side_effect = [
        {
            "project_name": "KJBot",
            "repo_name": "kjbot",
            "description": "Karaoke DJ system",
            "created_at": "2025-11-15T10:30:00Z",
            "contextkeep_version": "0.1.0"
        },
        {
            "project_name": "TaskFlow",
            "repo_name": "taskflow",
            "description": "Workflow automation",
            "created_at": "2025-11-14T15:22:00Z",
            "contextkeep_version": "0.1.0"
        },
        {
            "project_name": "WeatherAPI",
            "repo_name": "weather-api",
            "description": "Weather data",
            "created_at": "2025-11-13T09:15:00Z",
            "contextkeep_version": "0.1.0"
        }
    ]
    
    result = await list_projects()
    
    assert len(result) == 3
    assert result[0].project_name == "KJBot"
    assert result[1].project_name == "TaskFlow"
    assert result[2].project_name == "WeatherAPI"
```

#### TC-P3: List projects - skip invalid project
```python
@patch('modules.files.service.read_json_file')
@patch('modules.files.service.list_directories')
def test_list_projects_skip_invalid(mock_list_dirs, mock_read_json):
    """
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
    
    result = await list_projects()
    
    assert len(result) == 1
    assert result[0].project_name == "KJBot"
```

#### TC-P4: List projects - skip malformed JSON
```python
@patch('modules.files.service.read_json_file')
@patch('modules.files.service.list_directories')
def test_list_projects_skip_malformed_json(mock_list_dirs, mock_read_json):
    """
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
        JSONDecodeError("Invalid JSON", "", 0)
    ]
    
    result = await list_projects()
    
    assert len(result) == 1
    assert result[0].project_name == "KJBot"
```

### Module: `projects` - API Unit Tests

**File**: `tests/unit/projects/test_api.py`

#### TC-P5: GET /api/projects endpoint (mocked service)
```python
@patch('modules.projects.api.list_projects')
def test_get_projects_endpoint_unit(mock_list_projects, test_client):
    """
    Unit test for API endpoint - mocks service layer
    
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
            created_at=datetime.now()
        )
    ]
    
    response = test_client.get("/api/projects")
    
    assert response.status_code == 200
    assert mock_list_projects.call_count == 1
```

### Integration Test

**File**: `tests/integration/test_list_projects_flow.py`

#### TC-I1: GET /api/projects - end-to-end with real files
```python
def test_list_projects_end_to_end(test_client, test_projects_fixture_path, monkeypatch):
    """
    Full integration test - NO MOCKS, uses real fixture files
    
    Given: Real fixture project directories with .contextkeep/project.json files
    When: GET /api/projects is called
    Then: System reads actual files from fixtures
    And: Returns 200 OK with correctly parsed projects
    And: Projects are sorted alphabetically
    
    This test verifies the full stack:
    - API endpoint
    - Service layer
    - File I/O operations
    - Pydantic parsing
    """
    # Point settings to use test fixtures directory
    from config import settings
    monkeypatch.setattr(settings, 'projects_base_dir', test_projects_fixture_path)
    
    # Make actual API call - will read real files
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
```

---

## 7. Implementation Notes

### Configuration

**File**: `backend/config.py`

```python
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Projects
    projects_base_dir: Path = Path.home() / "contextkeep-projects"
    
    class Config:
        env_prefix = "CK_"
        env_file = ".env"

settings = Settings()
```

### Error Handling Philosophy

For UC-001, we adopt a **silent skip** approach:
- Projects without `.contextkeep/project.json` → skip, don't list
- Projects with malformed JSON → skip, don't list
- Empty projects directory → return empty list

**Rationale**: This is a read-only list operation. Invalid projects are the user's problem to fix outside ContextKeep. We don't pollute the UI with error messages for edge cases.

### Future Enhancements (Not in UC-001)

- Project search/filter
- Sort by created_at (most recent first)
- Project icons/avatars
- Last accessed timestamp
- Project statistics (# of microservices, test coverage, etc.)

---

## 8. Code Structure

### Backend Directory Tree

```
backend/
├── modules/
│   ├── __init__.py
│   │
│   ├── files/
│   │   ├── __init__.py
│   │   ├── api.py              # Future: File browser endpoints
│   │   ├── service.py          # Core file I/O operations
│   │   └── models.py           # File operation models
│   │
│   └── projects/
│       ├── __init__.py
│       ├── api.py              # GET /api/projects endpoint
│       ├── service.py          # Project business logic
│       └── models.py           # ProjectMetadata, ProjectSummary, etc.
│
├── config.py                   # Settings (projects_base_dir)
├── main.py                     # FastAPI app setup
├── pyproject.toml              # Python dependencies
│
└── tests/                      # All tests centralized here
    ├── conftest.py             # Shared test fixtures
    │
    ├── unit/                   # Unit tests (mocked dependencies)
    │   ├── files/
    │   │   └── test_file_service.py
    │   └── projects/
    │       ├── test_models.py
    │       ├── test_service.py
    │       └── test_api.py
    │
    ├── integration/            # Integration tests (real I/O, no mocks)
    │   └── test_list_projects_flow.py
    │
    └── fixtures/               # Test data
        └── projects/
            ├── kjbot/
            │   └── .contextkeep/
            │       └── project.json
            ├── taskflow/
            │   └── .contextkeep/
            │       └── project.json
            └── weather-api/
                └── .contextkeep/
                    └── project.json
```

### Frontend Directory Tree

```
frontend/
├── public/
│   └── index.html
│
├── src/
│   ├── components/
│   │   ├── ProjectList/
│   │   │   ├── ProjectList.tsx       # Main list component
│   │   │   ├── ProjectList.css       # Dark theme styles
│   │   │   ├── ProjectItem.tsx       # Individual project row
│   │   │   └── CreateProjectWidget.tsx
│   │   │
│   │   └── common/
│   │       └── ExpandIcon.tsx        # [+] / [-] icon component
│   │
│   ├── api/
│   │   └── projects.ts               # API client for /api/projects
│   │
│   ├── types/
│   │   └── project.types.ts          # TypeScript interfaces
│   │
│   ├── App.tsx                       # Root component
│   ├── App.css                       # Global styles
│   └── index.tsx                     # React entry point
│
├── package.json
└── tsconfig.json
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
# Create React app with TypeScript
npx create-react-app frontend --template typescript
cd frontend
npm install axios
```

**Verification**:
```bash
# Backend: Should pass (no tests yet)
cd backend && pytest

# Frontend: Should start
cd frontend && npm start
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

### Chunk 5: Frontend - Types and API Client

**Files**:
- `frontend/src/types/project.types.ts`
- `frontend/src/api/projects.ts`

**Manual Verification**:
- TypeScript compiles without errors
- No console errors in browser

---

### Chunk 6: Frontend - Components

**Files**:
- `frontend/src/components/common/ExpandIcon.tsx`
- `frontend/src/components/ProjectList/ProjectItem.tsx`
- `frontend/src/components/ProjectList/CreateProjectWidget.tsx`
- `frontend/src/components/ProjectList/ProjectList.tsx`
- `frontend/src/components/ProjectList/ProjectList.css`
- `frontend/src/App.tsx`
- `frontend/src/App.css`

**Manual Verification**:
- UI renders project list
- Expand/collapse works
- Dark theme looks correct
- No console errors

---

## 10. How to Run This Feature

### Step 1: Create Test Data

Create some sample projects in your local `~/contextkeep-projects` directory:

```bash
# Create KJBot project
mkdir -p ~/contextkeep-projects/kjbot/.contextkeep
cat > ~/contextkeep-projects/kjbot/.contextkeep/project.json << 'EOF'
{
  "project_name": "KJBot",
  "repo_name": "kjbot",
  "description": "Karaoke DJ system with queue management",
  "created_at": "2025-11-15T10:30:00Z",
  "contextkeep_version": "0.1.0"
}
EOF

# Create TaskFlow project
mkdir -p ~/contextkeep-projects/taskflow/.contextkeep
cat > ~/contextkeep-projects/taskflow/.contextkeep/project.json << 'EOF'
{
  "project_name": "TaskFlow",
  "repo_name": "taskflow",
  "description": "Workflow automation service",
  "created_at": "2025-11-14T15:22:00Z",
  "contextkeep_version": "0.1.0"
}
EOF

# Create WeatherAPI project
mkdir -p ~/contextkeep-projects/weather-api/.contextkeep
cat > ~/contextkeep-projects/weather-api/.contextkeep/project.json << 'EOF'
{
  "project_name": "WeatherAPI",
  "repo_name": "weather-api",
  "description": "Real-time weather data aggregation",
  "created_at": "2025-11-13T09:15:00Z",
  "contextkeep_version": "0.1.0"
}
EOF
```

### Step 2: Start Backend

```bash
cd backend
uvicorn main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Verify API Works

In another terminal:
```bash
curl http://localhost:8000/api/projects | jq
```

**Expected Response**:
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

### Step 4: Start Frontend

```bash
cd frontend
npm start
```

**Expected**: Browser opens to `http://localhost:3000`

### Step 5: See It Work!

You should see:
- Three projects listed: KJBot, TaskFlow, WeatherAPI (alphabetical)
- Each project has a [+] icon
- Clicking [+] expands to show repo name and description
- "Create New Project" widget at bottom
- Dark theme (gray/black like VS Code)

---

## Implementation Checklist

Follow the chunked implementation guide above. After each chunk, verify tests pass before moving forward.

- [ ] **Chunk 0**: Project setup complete
- [ ] **Chunk 1**: Files module (6 tests passing)
- [ ] **Chunk 2**: Projects models (model validation passing)
- [ ] **Chunk 3**: Projects service (4 tests passing)
- [ ] **Chunk 4**: API integration (1 test passing, curl works)
- [ ] **Chunk 5**: Frontend types and API client (compiles)
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
File operation models for ContextKeep.
"""
from pydantic import BaseModel
from pathlib import Path
from typing import List


class DirectoryListing(BaseModel):
    """Result of listing directories"""
    directories: List[Path]


class FileReadResult(BaseModel):
    """Result of reading a file"""
    content: dict
    path: Path
```

---

#### File: `backend/modules/files/service.py`

```python
"""
Low-level file system operations.

This module provides basic file I/O functionality used by other modules.
All functions are synchronous for simplicity in MVP.
"""
from pathlib import Path
from typing import List
import json


def list_directories(base_path: Path) -> List[Path]:
    """
    List all directories within a base path (non-recursive).
    
    Args:
        base_path: Directory to scan
        
    Returns:
        List of Path objects for immediate subdirectories only.
        Returns empty list if base_path doesn't exist or is not a directory.
    """
    if not base_path.exists() or not base_path.is_dir():
        return []
    
    return [item for item in base_path.iterdir() if item.is_dir()]


def read_json_file(file_path: Path) -> dict:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON as dict
        
    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If file contains invalid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

---

#### File: `backend/tests/unit/files/test_file_service.py`

```python
"""
Unit tests for file service operations.
"""
import pytest
import json
from pathlib import Path
from modules.files.service import list_directories, read_json_file


class TestListDirectories:
    """Tests for list_directories function"""
    
    def test_list_directories_empty(self, tmp_path):
        """
        TC-F1: List directories in empty directory
        
        Given: An empty directory
        When: list_directories() is called
        Then: Returns empty list
        """
        result = list_directories(tmp_path)
        assert result == []
    
    def test_list_directories_with_subdirs(self, tmp_path):
        """
        TC-F2: List directories with subdirectories
        
        Given: A directory with 3 subdirectories
        When: list_directories() is called
        Then: Returns list of 3 Path objects
        And: Paths are absolute paths to subdirectories
        And: Only immediate children are returned (not recursive)
        """
        # Create 3 subdirectories
        (tmp_path / "project1").mkdir()
        (tmp_path / "project2").mkdir()
        (tmp_path / "project3").mkdir()
        
        # Create nested directory (should not be in results)
        (tmp_path / "project1" / "nested").mkdir()
        
        result = list_directories(tmp_path)
        
        assert len(result) == 3
        assert all(isinstance(p, Path) for p in result)
        assert all(p.is_absolute() for p in result)
        
        # Check all subdirs present
        dir_names = {p.name for p in result}
        assert dir_names == {"project1", "project2", "project3"}
    
    def test_list_directories_ignores_files(self, tmp_path):
        """
        TC-F3: List directories ignores files
        
        Given: A directory with 2 subdirs and 3 files
        When: list_directories() is called
        Then: Returns only the 2 subdirectories
        """
        # Create 2 subdirectories
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir2").mkdir()
        
        # Create 3 files
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.json").write_text("{}")
        (tmp_path / "file3.md").write_text("# Title")
        
        result = list_directories(tmp_path)
        
        assert len(result) == 2
        dir_names = {p.name for p in result}
        assert dir_names == {"dir1", "dir2"}


class TestReadJsonFile:
    """Tests for read_json_file function"""
    
    def test_read_json_file_valid(self, tmp_path):
        """
        TC-F4: Read valid JSON file
        
        Given: A valid JSON file
        When: read_json_file() is called
        Then: Returns parsed dict with correct data
        """
        json_file = tmp_path / "test.json"
        test_data = {
            "name": "Test Project",
            "value": 42,
            "nested": {"key": "value"}
        }
        json_file.write_text(json.dumps(test_data))
        
        result = read_json_file(json_file)
        
        assert result == test_data
        assert result["name"] == "Test Project"
        assert result["value"] == 42
        assert result["nested"]["key"] == "value"
    
    def test_read_json_file_not_found(self, tmp_path):
        """
        TC-F5: Read JSON file - file not found
        
        Given: A non-existent file path
        When: read_json_file() is called
        Then: Raises FileNotFoundError
        """
        non_existent = tmp_path / "does_not_exist.json"
        
        with pytest.raises(FileNotFoundError):
            read_json_file(non_existent)
    
    def test_read_json_file_invalid_json(self, tmp_path):
        """
        TC-F6: Read JSON file - invalid JSON
        
        Given: A file with invalid JSON content
        When: read_json_file() is called
        Then: Raises JSONDecodeError
        """
        invalid_json = tmp_path / "invalid.json"
        invalid_json.write_text("{ this is not valid JSON }")
        
        with pytest.raises(json.JSONDecodeError):
            read_json_file(invalid_json)
```

---

### Chunk 2: Projects Module - Models

#### File: `backend/modules/projects/models.py`

```python
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
```

---

#### File: `backend/tests/unit/projects/test_models.py`

```python
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
```

---

### Chunk 3: Projects Module - Service

#### File: `backend/modules/projects/service.py`

```python
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
```

---

#### File: `backend/tests/unit/projects/test_service.py`

```python
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
```

---

### Chunk 4: API Integration

#### File: `backend/config.py`

```python
"""
Configuration settings for ContextKeep.
"""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Projects
    projects_base_dir: Path = Path.home() / "contextkeep-projects"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_prefix = "CK_"
        env_file = ".env"


settings = Settings()
```

---

#### File: `backend/main.py`

```python
"""
FastAPI application setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.projects.api import router as projects_router

app = FastAPI(
    title="ContextKeep API",
    description="Backend API for ContextKeep IDE",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api", tags=["projects"])


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "ContextKeep API"}
```

---

#### File: `backend/modules/projects/api.py`

```python
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
```

---

#### File: `backend/tests/conftest.py`

```python
"""
Shared test fixtures.
"""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def test_client():
    """FastAPI test client for making API requests"""
    return TestClient(app)


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def test_projects_fixture_path(fixtures_dir):
    """
    Path to test projects fixture directory.
    
    Integration tests use this to point settings.projects_base_dir
    to real fixture files instead of the user's actual projects directory.
    """
    return fixtures_dir / "projects"
```

---

#### File: `backend/tests/unit/projects/test_api.py`

```python
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
```

---

#### File: `backend/tests/integration/test_list_projects_flow.py`

```python
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
```

---

### Chunk 5: Frontend - Types and API Client

#### File: `frontend/src/types/project.types.ts`

```typescript
/**
 * TypeScript interfaces for project data.
 */

export interface ProjectSummary {
  project_name: string;
  repo_name: string;
  description: string;
  created_at: string;
}

export interface ProjectListResponse {
  projects: ProjectSummary[];
}
```

---

#### File: `frontend/src/api/projects.ts`

```typescript
/**
 * API client for project endpoints.
 */
import axios from 'axios';
import { ProjectListResponse } from '../types/project.types';

const API_BASE_URL = 'http://localhost:8000/api';

export const projectsApi = {
  /**
   * Fetch all projects.
   */
  async listProjects(): Promise<ProjectListResponse> {
    const response = await axios.get<ProjectListResponse>(
      `${API_BASE_URL}/projects`
    );
    return response.data;
  }
};
```

---

### Chunk 6: Frontend - Components

#### File: `frontend/src/components/common/ExpandIcon.tsx`

```typescript
/**
 * Expand/collapse icon component.
 */
import React from 'react';

interface ExpandIconProps {
  expanded: boolean;
}

const ExpandIcon: React.FC<ExpandIconProps> = ({ expanded }) => {
  return (
    <span style={{ 
      marginRight: '8px', 
      cursor: 'pointer',
      userSelect: 'none',
      fontWeight: 'bold'
    }}>
      {expanded ? '[-]' : '[+]'}
    </span>
  );
};

export default ExpandIcon;
```

---

#### File: `frontend/src/components/ProjectList/ProjectItem.tsx`

```typescript
/**
 * Individual project item component.
 */
import React, { useState } from 'react';
import { ProjectSummary } from '../../types/project.types';
import ExpandIcon from '../common/ExpandIcon';

interface ProjectItemProps {
  project: ProjectSummary;
  onProjectClick: (repoName: string) => void;
}

const ProjectItem: React.FC<ProjectItemProps> = ({ project, onProjectClick }) => {
  const [expanded, setExpanded] = useState(false);

  const handleToggleExpand = (e: React.MouseEvent) => {
    e.stopPropagation();
    setExpanded(!expanded);
  };

  const handleProjectClick = () => {
    onProjectClick(project.repo_name);
  };

  return (
    <div className="project-item">
      <div className="project-header" onClick={handleProjectClick}>
        <span onClick={handleToggleExpand}>
          <ExpandIcon expanded={expanded} />
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
};

export default ProjectItem;
```

---

#### File: `frontend/src/components/ProjectList/CreateProjectWidget.tsx`

```typescript
/**
 * Create new project widget.
 */
import React from 'react';

interface CreateProjectWidgetProps {
  onClick: () => void;
}

const CreateProjectWidget: React.FC<CreateProjectWidgetProps> = ({ onClick }) => {
  return (
    <div className="create-project-widget" onClick={onClick}>
      <span className="create-icon">[+]</span>
      <span className="create-text">Create New Project</span>
    </div>
  );
};

export default CreateProjectWidget;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.tsx`

```typescript
/**
 * Main project list component.
 */
import React, { useEffect, useState } from 'react';
import { ProjectSummary } from '../../types/project.types';
import { projectsApi } from '../../api/projects';
import ProjectItem from './ProjectItem';
import CreateProjectWidget from './CreateProjectWidget';
import './ProjectList.css';

const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await projectsApi.listProjects();
      setProjects(data.projects);
      setError(null);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (repoName: string) => {
    console.log(`Opening project: ${repoName}`);
    // TODO: Navigate to project view (future UC)
  };

  const handleCreateProject = () => {
    console.log('Create new project clicked');
    // TODO: Open project creation dialog (future UC)
  };

  if (loading) {
    return <div className="project-list-container">Loading projects...</div>;
  }

  if (error) {
    return <div className="project-list-container error">{error}</div>;
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
        <CreateProjectWidget onClick={handleCreateProject} />
      </div>
    </div>
  );
};

export default ProjectList;
```

---

#### File: `frontend/src/components/ProjectList/ProjectList.css`

```css
/**
 * Styles for project list (dark theme).
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
```

---

#### File: `frontend/src/App.tsx`

```typescript
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

**End of UC-001 Specification**
