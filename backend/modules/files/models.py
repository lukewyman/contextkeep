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