"""
应用配置
"""
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sphinx Quant"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "sphinxquant"
    POSTGRES_PASSWORD: str = "sphinxquant"
    POSTGRES_DB: str = "sphinxquant"
    DATABASE_URL: Optional[str] = None
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # 调试模式
    DEBUG: bool = True
    
    # Celery 配置
    CELERY_BROKER_URL: str = "pyamqp://sphinxquant:sphinxquant@localhost//"
    CELERY_RESULT_BACKEND: str = "rpc://"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 如果没有设置 DATABASE_URL，则从其他配置构建
if not settings.DATABASE_URL:
    settings.DATABASE_URL = (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    )

