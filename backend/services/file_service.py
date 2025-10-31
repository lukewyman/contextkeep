"""Service for file operations."""

from pathlib import Path
from typing import Optional

from models.file_models import FileNode


class FileService:
    """Service for file operations with security controls."""
    
    # Files/directories to exclude from tree
    EXCLUDED = {
        '.git', '__pycache__', 'node_modules', '.pytest_cache',
        'venv', '.venv', '.contextkeep', '.DS_Store', 'Thumbs.db',
        '*.pyc', '.coverage', 'htmlcov'
    }
    
    def __init__(self, projects_base: Path):
        """Initialize file service.
        
        Args:
            projects_base: Base directory containing all projects
        """
        self.projects_base = projects_base.resolve()
    
    def get_project_path(self, project_id: str) -> Path:
        """Get and validate project path.
        
        Args:
            project_id: Project identifier (must be safe directory name)
        
        Returns:
            Resolved path to project directory
        
        Raises:
            ValueError: If project_id contains path traversal attempts
            FileNotFoundError: If project doesn't exist
        """
        # Security: prevent path traversal
        if '..' in project_id or '/' in project_id or '\\' in project_id:
            raise ValueError("Invalid project_id: contains path traversal")
        
        project_path = (self.projects_base / project_id).resolve()
        
        # Security: ensure path is within projects_base
        if not str(project_path).startswith(str(self.projects_base)):
            raise ValueError("Invalid project path: outside projects directory")
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project '{project_id}' not found")
        
        if not project_path.is_dir():
            raise ValueError(f"Project '{project_id}' is not a directory")
        
        return project_path
    
    def build_tree(
        self,
        path: Path,
        max_depth: int = 3,
        current_depth: int = 0,
        show_hidden: bool = False,
        root_path: Optional[Path] = None
    ) -> list[FileNode]:
        """Recursively build file tree.
        
        Args:
            path: Directory to scan
            max_depth: Maximum recursion depth
            current_depth: Current depth (for recursion tracking)
            show_hidden: Whether to include hidden files
            root_path: Root path for calculating relative paths (internal)
        
        Returns:
            List of FileNode objects representing directory contents
        """
        if root_path is None:
            root_path = path
        
        if current_depth >= max_depth:
            return []
        
        items = []
        
        try:
            for item in sorted(path.iterdir()):
                # Skip hidden files unless requested
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                # Skip excluded directories
                if item.name in self.EXCLUDED:
                    continue
                
                # Calculate relative path from root
                try:
                    relative_path = item.relative_to(root_path)
                except ValueError:
                    # Skip if we can't calculate relative path
                    continue
                
                # Build node
                if item.is_file():
                    node = FileNode(
                        name=item.name,
                        path=str(relative_path),
                        type="file",
                        size=item.stat().st_size
                    )
                    items.append(node)
                
                elif item.is_dir():
                    children = self.build_tree(
                        item,
                        max_depth,
                        current_depth + 1,
                        show_hidden,
                        root_path
                    )
                    
                    node = FileNode(
                        name=item.name,
                        path=str(relative_path),
                        type="directory",
                        children=children if children else None
                    )
                    items.append(node)
        
        except PermissionError:
            # Silently skip directories we can't read
            pass
        
        return items
    
    def read_file(self, project_path: Path, file_path: str) -> tuple[str, int]:
        """Read file contents.
        
        Args:
            project_path: Project root directory
            file_path: Relative path to file from project root
        
        Returns:
            Tuple of (content, size)
        
        Raises:
            PermissionError: If file is outside project directory
            FileNotFoundError: If file doesn't exist
            ValueError: If path is not a file or file is not text
        """
        full_path = (project_path / file_path).resolve()
        
        # Security: ensure file is within project
        if not str(full_path).startswith(str(project_path)):
            raise PermissionError("Access denied: file outside project directory")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not full_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        try:
            content = full_path.read_text(encoding='utf-8')
            size = full_path.stat().st_size
            return content, size
        except UnicodeDecodeError:
            raise ValueError(f"File is not a text file: {file_path}")
    
    def write_file(
        self,
        project_path: Path,
        file_path: str,
        content: str
    ) -> tuple[int, bool]:
        """Write file contents.
        
        Args:
            project_path: Project root directory
            file_path: Relative path to file from project root
            content: Content to write
        
        Returns:
            Tuple of (size, created) where created is True if file was new
        
        Raises:
            PermissionError: If file is outside project directory
            ValueError: If path is invalid
        """
        full_path = (project_path / file_path).resolve()
        
        # Security: ensure file is within project
        if not str(full_path).startswith(str(project_path)):
            raise PermissionError("Access denied: file outside project directory")
        
        # Track if file exists
        created = not full_path.exists()
        
        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        full_path.write_text(content, encoding='utf-8')
        size = full_path.stat().st_size
        
        return size, created