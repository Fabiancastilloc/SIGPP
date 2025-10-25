from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SIGPP API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database - Valores por defecto para desarrollo local
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "0407"
    POSTGRES_SERVER: str = "localhost"  # Cambiado de "db" a "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "sigpp_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
