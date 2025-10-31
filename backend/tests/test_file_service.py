"""Unit tests for FileService."""

import pytest
from pathlib import Path

from services.file_service import FileService


class TestGetProjectPath:
    """Tests for get_project_path method."""
    
    def test_success(self, file_service, temp_project):
        """Should return valid project path."""
        temp_dir, project_dir = temp_project
        
        path = file_service.get_project_path("test-project")
        
        assert path == project_dir
        assert path.is_dir()
    
    def test_not_found(self, file_service):
        """Should raise FileNotFoundError for non-existent project."""
        with pytest.raises(FileNotFoundError, match="not found"):
            file_service.get_project_path("nonexistent")
    
    def test_path_traversal_dots(self, file_service):
        """Should reject path traversal with .."""
        with pytest.raises(ValueError, match="path traversal"):
            file_service.get_project_path("../etc")
    
    def test_path_traversal_slash(self, file_service):
        """Should reject paths with slashes."""
        with pytest.raises(ValueError, match="path traversal"):
            file_service.get_project_path("test/project")
    
    def test_path_traversal_backslash(self, file_service):
        """Should reject paths with backslashes."""
        with pytest.raises(ValueError, match="path traversal"):
            file_service.get_project_path("test\\project")


class TestBuildTree:
    """Tests for build_tree method."""
    
    def test_basic_structure(self, file_service, temp_project):
        """Should build correct tree structure."""
        temp_dir, project_dir = temp_project
        
        tree = file_service.build_tree(project_dir)
        
        # Should have 3 items (file1.py, file2.txt, subdir)
        # .hidden is excluded by default
        assert len(tree) == 3
        
        # Check files
        files = [n for n in tree if n.type == "file"]
        assert len(files) == 2
        assert {f.name for f in files} == {"file1.py", "file2.txt"}
        
        # Check directory
        dirs = [n for n in tree if n.type == "directory"]
        assert len(dirs) == 1
        assert dirs[0].name == "subdir"
    
    def test_nested_structure(self, file_service, temp_project):
        """Should handle nested directories."""
        temp_dir, project_dir = temp_project
        
        tree = file_service.build_tree(project_dir)
        
        # Find subdir
        subdir = next(n for n in tree if n.name == "subdir")
        assert subdir.children is not None
        assert len(subdir.children) == 2  # file3.py and nested/
        
        # Find nested dir
        nested = next(n for n in subdir.children if n.name == "nested")
        assert nested.type == "directory"
        assert nested.children is not None
        assert len(nested.children) == 1
        assert nested.children[0].name == "file4.py"
    
    def test_max_depth(self, file_service, temp_project):
        """Should respect max_depth parameter."""
        temp_dir, project_dir = temp_project
        
        # Depth 1: only immediate children
        tree = file_service.build_tree(project_dir, max_depth=1)
        subdir = next(n for n in tree if n.name == "subdir")
        assert subdir.children is None or len(subdir.children) == 0
        
        # Depth 2: one level of nesting
        tree = file_service.build_tree(project_dir, max_depth=2)
        subdir = next(n for n in tree if n.name == "subdir")
        assert subdir.children is not None
        assert len(subdir.children) == 2
        
        # nested/ should be empty
        nested = next(n for n in subdir.children if n.name == "nested")
        assert nested.children is None or len(nested.children) == 0
    
    def test_show_hidden(self, file_service, temp_project):
        """Should include hidden files when requested."""
        temp_dir, project_dir = temp_project
        
        # Default: hidden files excluded
        tree = file_service.build_tree(project_dir, show_hidden=False)
        names = {n.name for n in tree}
        assert ".hidden" not in names
        
        # With show_hidden: hidden files included
        tree = file_service.build_tree(project_dir, show_hidden=True)
        names = {n.name for n in tree}
        assert ".hidden" in names
    
    def test_file_sizes(self, file_service, temp_project):
        """Should include file sizes."""
        temp_dir, project_dir = temp_project
        
        tree = file_service.build_tree(project_dir)
        
        file1 = next(n for n in tree if n.name == "file1.py")
        assert file1.size is not None
        assert file1.size > 0
    
    def test_relative_paths(self, file_service, temp_project):
        """Should use relative paths from root."""
        temp_dir, project_dir = temp_project
        
        tree = file_service.build_tree(project_dir)
        
        # Top-level file
        file1 = next(n for n in tree if n.name == "file1.py")
        assert file1.path == "file1.py"
        
        # Nested file
        subdir = next(n for n in tree if n.name == "subdir")
        file3 = next(n for n in subdir.children if n.name == "file3.py")
        assert file3.path == "subdir/file3.py"


class TestReadFile:
    """Tests for read_file method."""
    
    def test_success(self, file_service, temp_project):
        """Should read file contents."""
        temp_dir, project_dir = temp_project
        
        content, size = file_service.read_file(project_dir, "file1.py")
        
        assert content == "print('hello')"
        assert size > 0
    
    def test_nested_file(self, file_service, temp_project):
        """Should read files in subdirectories."""
        temp_dir, project_dir = temp_project
        
        content, size = file_service.read_file(project_dir, "subdir/file3.py")
        
        assert content == "print('world')"
        assert size > 0
    
    def test_not_found(self, file_service, temp_project):
        """Should raise FileNotFoundError for missing files."""
        temp_dir, project_dir = temp_project
        
        with pytest.raises(FileNotFoundError, match="not found"):
            file_service.read_file(project_dir, "nonexistent.py")
    
    def test_path_traversal(self, file_service, temp_project):
        """Should reject path traversal attempts."""
        temp_dir, project_dir = temp_project
        
        # Create a file outside project
        (temp_dir / "outside.txt").write_text("secret")
        
        with pytest.raises(PermissionError, match="Access denied"):
            file_service.read_file(project_dir, "../outside.txt")
    
    def test_directory_not_file(self, file_service, temp_project):
        """Should raise ValueError when trying to read a directory."""
        temp_dir, project_dir = temp_project
        
        with pytest.raises(ValueError, match="not a file"):
            file_service.read_file(project_dir, "subdir")


class TestWriteFile:
    """Tests for write_file method."""
    
    def test_create_new_file(self, file_service, temp_project):
        """Should create new file."""
        temp_dir, project_dir = temp_project
        
        size, created = file_service.write_file(
            project_dir,
            "new_file.py",
            "print('new')"
        )
        
        assert created is True
        assert size > 0
        assert (project_dir / "new_file.py").read_text() == "print('new')"
    
    def test_overwrite_existing(self, file_service, temp_project):
        """Should overwrite existing file."""
        temp_dir, project_dir = temp_project
        
        size, created = file_service.write_file(
            project_dir,
            "file1.py",
            "print('updated')"
        )
        
        assert created is False
        assert (project_dir / "file1.py").read_text() == "print('updated')"
    
    def test_create_nested_file(self, file_service, temp_project):
        """Should create parent directories as needed."""
        temp_dir, project_dir = temp_project
        
        size, created = file_service.write_file(
            project_dir,
            "deep/nested/file.py",
            "print('deep')"
        )
        
        assert created is True
        assert (project_dir / "deep" / "nested" / "file.py").exists()
        assert (project_dir / "deep" / "nested" / "file.py").read_text() == "print('deep')"
    
    def test_path_traversal(self, file_service, temp_project):
        """Should reject path traversal attempts."""
        temp_dir, project_dir = temp_project
        
        with pytest.raises(PermissionError, match="Access denied"):
            file_service.write_file(
                project_dir,
                "../outside.txt",
                "nope"
            )
        
        # Verify file was not created
        assert not (temp_dir / "outside.txt").exists()