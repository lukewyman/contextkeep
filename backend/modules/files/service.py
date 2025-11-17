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