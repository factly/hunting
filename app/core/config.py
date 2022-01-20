from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Hunting Server"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"  # noqa: E501

    # S3 (MINIO) PARAMS
    S3_ENDPOINT: str = "minio:9000"
    S3_BUCKET: str = "hunting"
    S3_KEY: str = "minio"
    S3_SECRET: str = "password"
    S3_SECURE: bool = False

    S3_ENDPOINT_TARGET: str = "minio:9000"
    S3_BUCKET_TARGET: str = "hunting"
    S3_KEY_TARGET: str = "minio"
    S3_SECRET_TARGET: str = "password"
    S3_SECURE_TARGET: bool = False

    # CORS PARAMS
    CORS_ORIGINS: list = [
        "http://127.0.0.1:8000",
        "http://localhost",
        "http://localhost:8000",
    ]
    CORS_METHODS: list = ["GET"]

    class Config:
        env_file = ".env"
