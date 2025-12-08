from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pydantic-settings v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    MONGO_URI: AnyUrl = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "whatsapp_flow_db"

    WHATSAPP_PROVIDER_API_BASE: str = "https://example-whatsapp-provider"
    EXTERNAL_API_BASE: str = "https://example-external-api"


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
