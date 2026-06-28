from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    project_name: str = "Genesis Engine"
    api_v1_str: str = "/api/v1"
    
    # Security
    secret_key: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", description="Secret key for JWT")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 8  # 8 days
    token_issuer: str = "genesis-engine"
    token_audience: str = "genesis-users"
    
    # Limits
    max_upload_size_mb: float = 10.0
    max_preview_size_mb: float = 2.0
    
    # Users Configuration
    admin_bootstrap_username: str = "admin"
    admin_bootstrap_password: str = "admin" # In production, this must be changed or loaded via env
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()
