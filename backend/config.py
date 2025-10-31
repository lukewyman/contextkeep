"""Configuration management for ContextKeep backend."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Project storage
    projects_base: Path = Path.home() / "contextkeep-projects"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8765
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CONTEXTKEEP_",
        case_sensitive=False
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure projects directory exists
        self.projects_base.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()