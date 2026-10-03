from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "InsightForge API"
    version: str = "1.0.0"
    data_dir: str = "data"
    max_upload_mb: int = 100

settings = Settings()
