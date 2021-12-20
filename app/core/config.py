from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Hunting Server"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"  # noqa: E501

    # S3 (MINIO) PARAMS
    S3_ENDPOINT: str = "localhost:9000"
    S3_BUCKET: str = "hunting"
    S3_KEY: str = "minio"
    S3_SECRET: str = "password"

    # API ACTIONS
    API_ACTIONS: list = [
        "samples",
        "tables",
        "analysis",
        "alerts",
        "description",
        "correlations",
        "missing",
        "package",
        "variable",
        "duplicates",
    ]

    class Config:
        env_file = ".env"
