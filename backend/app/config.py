import json
import os
from pathlib import Path
from typing import List


class Settings:
    # Application
    app_name: str = os.getenv("APP_NAME", "DevFlow Checkpoint AI")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Database - Supabase PostgreSQL
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@db.whulvrnkotzizayydtrr.supabase.co:5432/postgres"
    )
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_cache_ttl: int = int(os.getenv("REDIS_CACHE_TTL", "3600"))
    
    # Legacy JSON storage (for backward compatibility during migration)
    data_path: Path = Path(os.getenv("DEVFLOW_DATA_PATH", "data/devflow.json"))
    
    # CORS
    cors_origins: List[str] = json.loads(
        os.getenv("CORS_ORIGINS", '["http://localhost:5173", "http://localhost:3000"]')
    )
    
    # IBM BOB API
    ibm_bob_api_key: str = os.getenv("IBM_BOB_API_KEY", "")
    ibm_bob_api_url: str = os.getenv("IBM_BOB_API_URL", "https://api.ibm.com/bob/v1")
    bob_model: str = os.getenv("BOB_MODEL", "ibm-bob-v1")
    bob_max_tokens: int = int(os.getenv("BOB_MAX_TOKENS", "100000"))
    bob_temperature: float = float(os.getenv("BOB_TEMPERATURE", "0.7"))
    bob_streaming: bool = os.getenv("BOB_STREAMING", "true").lower() == "true"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")


settings = Settings()
