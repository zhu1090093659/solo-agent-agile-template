"""
Application Settings
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "[AGENT_NAME]"
    app_env: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    db_pool_size: int = 5
    db_echo: bool = False
    
    # Authentication
    secret_key: str = "change-this-to-a-secure-random-string"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # ========================================
    # Claude Code / Agent Configuration
    # ========================================
    anthropic_api_key: str = ""
    claude_model: str = "sonnet"  # sonnet, opus, haiku
    
    # Agent workspace (where Claude Code runs)
    agent_workspace_dir: str = "/tmp/agent_workspaces"
    agent_max_turns: int = 10
    agent_timeout: int = 300  # 5 minutes
    
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"
    
    # Aliases for backward compatibility
    @property
    def ANTHROPIC_API_KEY(self) -> str:
        return self.anthropic_api_key
    
    @property
    def AGENT_WORKSPACE_DIR(self) -> str:
        return self.agent_workspace_dir


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
