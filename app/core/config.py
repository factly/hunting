from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Hunting Server"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv"  # noqa: E501

    # S3 (MINIO) PARAMS
    S3_ENDPOINT: str = "http://minio:9000"
    S3_BUCKET: str = "hunting"
    S3_KEY: str = "minio"
    S3_SECRET: str = "password"

    class Config:
        env_file = ".env"
