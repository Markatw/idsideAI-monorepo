from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    POSTGRES_URI: str | None = None
    REDIS_URL: str | None = None

    OPENAI_API_KEY: str
    CORS_ALLOW_ORIGINS: str = "*"
    CSP: str | None = None
    NEO4J_URI: AnyUrl | None = None
    NEO4J_USER: str | None = None
    NEO4J_PASSWORD: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
