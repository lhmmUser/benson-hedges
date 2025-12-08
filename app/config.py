import os
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    MONGO_URI: AnyUrl = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "whatsapp_flow_db"

    # Placeholder for external integrations
    WHATSAPP_PROVIDER_API_BASE: str = "https://example-whatsapp-provider"
    EXTERNAL_API_BASE: str = "https://example-external-api"

    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    # Simple singleton-ish pattern
    global _settings
    try:
        return _settings
    except NameError:
        _settings = Settings()
        return _settings
