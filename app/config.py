from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pydantic-settings v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    MONGO_URI: AnyUrl = "mongodb+srv://kush:kush%40lhmm@cluster0.gcdsern.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    MONGO_DB_NAME: str = "goldflake-generations"

    WHATSAPP_PROVIDER_API_BASE: str = "https://graph.facebook.com/v19.0"
    EXTERNAL_API_BASE: str = "https://e21a0a2c862d.ngrok-free.app"
    VERIFY_TOKEN: str = "my_secret_token_123"
    ACCESS_TOKEN: str = "EAALtHhrzrNIBQFd6MQ1qlcANtBJnaCtJKvMXonTr5olZAe6l4zxSu9sWUENc75Ce6M3O1yA1W1WHYAbxYZAwSNIgxMqTud6fPA8PlTNbLZBtLPR70uCmwpEtNRS8VjSWF4Eu0yDIqF4fMYXLgaTFdBnkBxEhWTGsujRiNZBAZB4ni6ZCFL5X2zJhybkTTAZBcbSKQZDZD"
    PHONE_NUMBER_ID: str = "848200111711377"

_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
