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