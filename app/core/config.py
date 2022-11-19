from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hunting Server"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"
    ENABLE_PREFETCH: bool = True

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"  # noqa: E501

    # CORS PARAMS
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
