from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_name: str
    database_url: str
    test_database_url: str
    debug: bool


settings = Settings()  # type: ignore[call-arg]  # 字段值从 .env / 环境变量注入

     




