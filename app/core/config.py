from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "API Categorías - POO Servicio 03"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./categorias.db"


settings = Settings()
