from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    deploy_environment: str = Field(..., env="DEPLOY_ENVIRONMENT")
    db_url: str = Field(..., env="DATABASE_URL")
    auth_algorithm: str = Field(..., env="AUTH_ALGORITHM")
    auth_secret_key: str = Field(..., env="AUTH_SECRET_KEY")
    auth_access_token_expire_minutes: int = Field(
        ..., env="AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
