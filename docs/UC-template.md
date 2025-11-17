# UC-XXX: [Feature Name]

**Feature**: [One-line description of what this feature does]  
**Status**: Draft  
**Created**: [YYYY-MM-DD]  
**Modules**: [List modules involved, e.g., `projects`, `files`, `git`]

---

## Table of Contents

1. [User Story](#user-story)
2. [UI Specification](#ui-specification)
3. [API Contracts](#api-contracts)
4. [Module Architecture](#module-architecture)
5. [Data Models](#data-models)
6. [Test Cases](#test-cases)
7. [Implementation Notes](#implementation-notes)
8. [Dependencies](#dependencies)
9. [Code Structure](#code-structure)
10. [Implementation Guide](#implementation-guide)
11. [How to Run This Feature](#how-to-run-this-feature)

---

## 1. User Story

**As a** [user role]  
**I want to** [goal/desire]  
**So that** [benefit/value]

### Acceptance Criteria

- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

---

## 2. UI Specification

### [View Name]

```
┌─────────────────────────────────────────────┐
│  [ASCII wireframe of UI]                    │
│                                             │
│  [Show layout, widgets, interactions]       │
│                                             │
└─────────────────────────────────────────────┘
```

### UI Behavior

- **[Action]**: [What happens]
- **[Action]**: [What happens]

### Theme

- Dark gray/black night theme (matching VS Code and Claude.ai)

---

## 3. API Contracts

### [HTTP METHOD] /api/[endpoint]

**Description**: [What this endpoint does]

**Request**: [Request body schema or "None"]

```json
{
  "field": "value"
}
```

**Response**: [Status Code]

```json
{
  "result": "data"
}
```

**Error Responses**: 

- **[Status Code]**: [When this occurs]

---

## 4. Module Architecture

### Module Interaction Flow

```
Frontend
    │
    │ [Interaction description]
    ▼
[module]/api.py
    │
    │ [function_call()]
    ▼
[module]/service.py
    │
    │ [calls to other modules]
    ▼
[other_module]/service.py
```

### Module: `[module_name]`

**Purpose**: [What this module is responsible for]

**Location**: `backend/modules/[module_name]/`

**Files**:
- `api.py` - [What it does]
- `service.py` - [What it does]
- `models.py` - [What it does]
- `tests/` - [What it tests]

**Public Interface** (`service.py`):
```python
def function_name(params) -> ReturnType:
    """
    [Description]
    
    Args:
        [arg]: [description]
        
    Returns:
        [description]
        
    Raises:
        [Exception]: [when]
    """
```

---

## 5. Data Models

### [Model Purpose/Location]

**Location**: `[path/to/file]`

**Schema**:
```json
{
  "field": "value",
  "field2": "value2"
}
```

### Pydantic Models

**File**: `backend/modules/[module]/models.py`

```python
from pydantic import BaseModel, Field

class ModelName(BaseModel):
    """
    [Description]
    """
    field_name: str = Field(..., description="[description]")
```

---

## 6. Test Cases

### Test Organization

All tests are centralized in `backend/tests/` for clear separation from production code and easy exclusion from Electron builds.

```
backend/tests/
├── unit/                      # Fast, isolated, mocked dependencies
│   ├── [module1]/
│   │   ├── test_models.py
│   │   ├── test_service.py
│   │   └── test_api.py
│   └── [module2]/
│       └── test_service.py
│
├── integration/               # Real I/O, multiple components, no mocks
│   └── test_[feature]_flow.py
│
└── fixtures/                  # Test data
    └── [test_data]/
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

### Module: `[module]` - Unit Tests

**File**: `tests/unit/[module]/test_[component].py`

#### TC-XX-1: [Test case description]
```python
def test_[test_name](tmp_path):  # or @patch for mocking
    """
    Given: [precondition]
    When: [action]
    Then: [expected result]
    And: [additional expectation]
    """
```

#### TC-XX-2: [Test case description]
```python
@patch('[module].service.[dependency]')
def test_[test_name](mock_dependency):
    """
    Given: [mocked dependency behavior]
    When: [action]
    Then: [expected result]
    And: [verify mock was called correctly]
    """
```

### Integration Test

**File**: `tests/integration/test_[feature]_flow.py`

#### TC-I-XX: [Integration test description]
```python
def test_[feature]_end_to_end(test_client, test_fixture_path, monkeypatch):
    """
    Full integration test - NO MOCKS, uses real fixture files
    
    Given: [real test data setup]
    When: [actual API call or system action]
    Then: [verify real behavior across multiple components]
    
    This test verifies the full stack:
    - [Component 1]
    - [Component 2]
    - [Component 3]
    """
    # Point system to use test fixtures
    from config import settings
    monkeypatch.setattr(settings, '[setting]', test_fixture_path)
    
    # Make real call - no mocks
    response = test_client.get("/api/[endpoint]")
    
    assert response.status_code == 200
    # ... verify real data was processed correctly
```

---

## 7. Implementation Notes

### [Subsection Name]

[Any important implementation details, design decisions, or gotchas]

### Error Handling Philosophy

[How errors should be handled for this UC]

### Future Enhancements (Not in This UC)

- [Enhancement idea 1]
- [Enhancement idea 2]

---

## 8. Dependencies

### New Python Dependencies

Add to `pyproject.toml` under `[project] dependencies`:

```toml
"[package-name]>=[version]",
```

**Why needed**: [Explanation of what this dependency does for this UC]

### New Development Dependencies

Add to `[project.optional-dependencies] dev`:

```toml
"[package-name]>=[version]",
```

**Why needed**: [Explanation]

### Installation

After updating `pyproject.toml`:
```bash
cd backend
pip install -e ".[dev]"
```

---

## 9. Code Structure

### Backend Directory Tree

```
backend/
├── modules/
│   ├── [module_name]/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── service.py
│   │   └── models.py
│   │
│   └── [other_module]/
│       ├── __init__.py
│       ├── api.py
│       └── service.py
│
├── config.py
├── main.py
├── pyproject.toml
│
└── tests/                      # All tests centralized here
    ├── conftest.py             # Shared fixtures
    │
    ├── unit/                   # Unit tests (mocked dependencies)
    │   ├── [module1]/
    │   │   ├── test_models.py
    │   │   ├── test_service.py
    │   │   └── test_api.py
    │   └── [module2]/
    │       └── test_service.py
    │
    ├── integration/            # Integration tests (real I/O, no mocks)
    │   └── test_[feature]_flow.py
    │
    └── fixtures/               # Test data
        └── [test_data]/
```

### Frontend Directory Tree

```
frontend/
├── src/
│   ├── components/
│   │   └── [ComponentName]/
│   │       ├── [ComponentName].tsx
│   │       └── [ComponentName].css
│   │
│   ├── api/
│   │   └── [module].ts
│   │
│   ├── types/
│   │   └── [module].types.ts
│   │
│   └── App.tsx
```

---

## 10. Implementation Guide

### Implementation Strategy

Work in **chunks** - each chunk contains related code files plus tests. Run pytest after each chunk to ensure green tests before moving forward. If you hit red, iterate with Claude using the stack trace.

**Chunk Order**: [Describe the logical build order]

### Chunk 0: Project Setup

**Goal**: Create project structure and verify tooling works

**Backend Setup**:
```bash
# Create module directory structure
mkdir -p backend/modules/[module1]
mkdir -p backend/modules/[module2]

# Create centralized test directory structure
mkdir -p backend/tests/unit/[module1]
mkdir -p backend/tests/unit/[module2]
mkdir -p backend/tests/integration
mkdir -p backend/tests/fixtures/[test_data]

# Create __init__.py files for modules
touch backend/modules/__init__.py
touch backend/modules/[module1]/__init__.py
touch backend/modules/[module2]/__init__.py

# Create __init__.py files for tests (helps with imports)
touch backend/tests/__init__.py
touch backend/tests/unit/__init__.py
touch backend/tests/unit/[module1]/__init__.py
touch backend/tests/unit/[module2]/__init__.py
touch backend/tests/integration/__init__.py

# Install dependencies (if any new ones)
cd backend
pip install -e ".[dev]"
```

**Frontend Setup** (if applicable):
```bash
# Install any new packages
cd frontend
npm install [packages]
```

**Verification**:
```bash
# Should pass or start successfully
[command to verify]
```

---

### Chunk 1: [Chunk Name/Purpose]

**Files**:
- `[path/to/file1]`
- `[path/to/file2]`
- `[path/to/test_file]`

**Tests to Pass**:
- TC-XX-1: [Test name]
- TC-XX-2: [Test name]

**Run**:
```bash
cd backend
pytest [path/to/tests] -v
```

**Expected**: X/X tests passing ✅

---

### Chunk 2: [Next Chunk]

**Files**:
- `[path/to/file]`

**Tests to Pass**:
- [List tests]

**Run**:
```bash
[command]
```

**Expected**: [Expected outcome]

---

### Chunk N: [Final Frontend Chunk]

**Files**:
- `[frontend files]`

**Manual Verification**:
- [What to check in browser]
- [What behavior to verify]

---

## 11. How to Run This Feature

### Step 1: [Setup Step]

[Instructions for any data setup, configuration, etc.]

```bash
# Commands
```

### Step 2: Start Backend

```bash
cd backend
uvicorn main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Verify API Works (if applicable)

```bash
curl [endpoint] | jq
```

**Expected Response**:
```json
{
  "expected": "data"
}
```

### Step 4: Start Frontend (if applicable)

```bash
cd frontend
npm start
```

**Expected**: Browser opens to `http://localhost:3000`

### Step 5: See It Work!

You should see:
- [Observable behavior 1]
- [Observable behavior 2]
- [Observable behavior 3]

---

## Implementation Checklist

Follow the chunked implementation guide above. After each chunk, verify tests pass before moving forward.

- [ ] **Chunk 0**: Project setup complete
- [ ] **Chunk 1**: [Description] (X tests passing)
- [ ] **Chunk 2**: [Description] (X tests passing)
- [ ] **Chunk N**: [Description] (verification complete)
- [ ] **Final**: End-to-end manual verification complete

---

## Code Files

The following sections contain the complete implementation code for UC-XXX, organized by chunk.

---

### Chunk 1: [Chunk Name]

#### File: `[path/to/file.py]`

```python
"""
[Module docstring]
"""

# Code here
```

---

#### File: `[path/to/test_file.py]`

```python
"""
[Test module docstring]
"""

# Test code here
```

---

### Chunk 2: [Next Chunk]

[Continue pattern for all chunks...]

---

**End of UC-XXX Specification**
