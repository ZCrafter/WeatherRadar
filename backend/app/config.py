from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_db: str = "weathertracker"
    postgres_user: str = "weathertracker"
    postgres_password: str = "weathertracker"
    postgres_host: str = "db"
    postgres_port: int = 5432
    backend_url: str = "http://backend:8000"
    openmeteo_tz: str = "auto"
    scheduler_interval_minutes: int = 30
    snapshot_models: str = "ecmwf_ifs,gfs_seamless,icon_global,gem_global,meteofrance_arpege_world,ukmo_global"

    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)
