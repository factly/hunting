from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hunting Server"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"
    ENABLE_PREFETCH: bool = True

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"  # noqa: E501

    # MONGODB PARAMS
    MONGODB_HOST: str = "mongodb"
    MONGODB_PORT: int = 27017
    MONGODB_DATABASE: str = "hunting"
    MONGODB_USER: str = "root"
    MONGODB_PASSWORD: str = "example"

    # S3 CONFIGURATION
    S3_ENDPOINT_URL: str = "CHANGE_ME"
    S3_ACCESS_KEY_ID: str = "CHANGE_ME"
    S3_SECRET_ACCESS_KEY: str = "CHANGE_ME"

    # REDIS CONFIGURATION
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = "password"

    # CELERY CONFIGURATION
    CELERY_BROKER_URL: str = "redis://:password@redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://:password@redis:6379/0"

    # CORS PARAMS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # MODEL PARAMS
    # Constraint for Column names
    COLUMN_NAME_REGEX_PATTERN = r"[\w\s]*"

    # PROFILE SEGMENTS
    SAMPLE_DATA_RENDERER: List[str] = ["head"]

    # LOGGING SETTINGS
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_FILE_SIZE: int = 100_000_000  # 100MB
    LOG_FILE_BACKUP_COUNT: int = 5
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # PROFILING SETTINGS
    PROGRESS_BAR: bool = True

    class Config:
        env_file = ".env"
