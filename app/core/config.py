"""Application configuration using pydantic-settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "MCP Chat API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Database
    database_url: str = "sqlite:///./chat.db"
    
    # MCP Settings (customize as needed)
    mcp_enabled: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )


settings = Settings()


