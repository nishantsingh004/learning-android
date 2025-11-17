from pydantic import BaseModel
import os

class Settings(BaseModel):
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8080"))
    env: str = os.getenv("ENV", "dev")

    db_user: str = os.getenv("POSTGRES_USER", "postgres")
    db_pass: str = os.getenv("POSTGRES_PASSWORD", "yellowbus")
    db_name: str = os.getenv("POSTGRES_DB", "kifagri")
    db_host: str = os.getenv("POSTGRES_HOST", "49.205.172.128")
    db_port: int = int(os.getenv("POSTGRES_PORT", "5432"))

settings = Settings()
