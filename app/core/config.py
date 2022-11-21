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

    # CORS PARAMS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # MODEL PARAMS
    # Constraint for Column names
    COLUMN_NAME_REGEX_PATTERN = r"[\w\s]*"

    # PROFILE SEGMENTS
    SAMPLE_DATA_RENDERER: List[str] = ["head"]

    class Config:
        env_file = ".env"
