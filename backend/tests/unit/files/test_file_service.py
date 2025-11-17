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