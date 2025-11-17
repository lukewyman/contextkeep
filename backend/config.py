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