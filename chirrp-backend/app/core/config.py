from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    CHIRRP_BEARER_TOKEN: str
    API_V1_PREFIX: str = "/api/v1"
    ENV: str = "local"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@db:5432/{self.postgres_db}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # <--- this fixes the ValidationError
    )

settings = Settings()