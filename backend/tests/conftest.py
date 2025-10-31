"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil

from services.file_service import FileService


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_project(temp_dir):
    """Create a temporary project with sample files.
    
    Structure:
        test-project/
        ├── file1.py
        ├── file2.txt
        ├── subdir/
        │   ├── file3.py
        │   └── nested/
        │       └── file4.py
        └── .hidden
    """
    project_dir = temp_dir / "test-project"
    project_dir.mkdir()
    
    # Create files
    (project_dir / "file1.py").write_text("print('hello')")
    (project_dir / "file2.txt").write_text("some text")
    
    # Create subdirectories
    subdir = project_dir / "subdir"
    subdir.mkdir()
    (subdir / "file3.py").write_text("print('world')")
    
    nested = subdir / "nested"
    nested.mkdir()
    (nested / "file4.py").write_text("print('nested')")
    
    # Create hidden file
    (project_dir / ".hidden").write_text("secret")
    
    return temp_dir, project_dir


@pytest.fixture
def file_service(temp_dir):
    """Create a FileService instance with temp directory."""
    return FileService(temp_dir)