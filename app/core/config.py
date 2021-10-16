from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Hunting"
    API_V1_STR: str = "/api/v1"
    MODE: str = "development"

    # EXAMPLE PARAMS
    EXAMPLE_URL: str = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"  # noqa: E501

    class Config:
        env_file = ".env"
