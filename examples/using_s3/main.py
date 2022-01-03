import json
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import requests
from dotenv import dotenv_values
from minio import Minio

FILE_PATH = Path(__file__).resolve()
PROJECT_DIR = FILE_PATH.parents[2]
ENV_FILE_PATH = FILE_PATH.parents[0] / ".env"


@dataclass
class ETLSourceConfig:
    """Config class for source configurations"""

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


@dataclass
class ETLTransformConfig:
    """Config class for Transformation configurations"""

    api_endpoint: str


@dataclass
class ETLTargetConfig:
    """Config class for target configurations"""

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str
    length: int
    part_size: int


class ETLSession:
    """Class that will perform all ETL operations"""

    def __init__(
        self,
        source_argument: ETLSourceConfig,
        transform_argument: ETLTransformConfig,
        target_argument: ETLTargetConfig,
    ) -> None:
        self.source_argument = source_argument
        self.transform_argument = transform_argument
        self.target_argument = target_argument

    def extract(self, key_prefix: str):
        """
        Function that will provide generator object for keys of required object
        """
        try:
            client = Minio(
                endpoint=self.source_argument.endpoint_url,
                access_key=self.source_argument.access_key,
                secret_key=self.source_argument.secret_key,
            )
        except Exception as e:
            print(f"{e}")
            raise
        else:
            objects = client.list_objects(
                self.source_argument.bucket_name,
                prefix=key_prefix,
                recursive=True,
            )
            for each_obj in objects:
                yield each_obj.object_name

    def transform(self, source_file_url: str):
        """
        Function to perform/run hunting library on csv
        that are provided by extract function
        """
        print(f"source File URL: {source_file_url}")
        print(f"End Point: {self.transform_argument.api_endpoint}")
        try:
            response = requests.get(
                url=self.transform_argument.api_endpoint,
                params={"source": source_file_url, "samples_to_show": 10},
            )
        except Exception as e:
            print(f"{e}")
            print(f"Skipping: {source_file_url}")
            raise
        else:
            if response.status_code not in [200, 201]:
                print(f"Improper Response received: {response.text}")
                raise
            out_buffer = BytesIO(json.dumps(response.json()).encode("utf-8"))
            return out_buffer

    def load(self, file_path_key, buffer_to_upload):
        """Function to put response of hunting library to required output"""
        client = Minio(
            endpoint=self.target_argument.endpoint_url,
            access_key=self.target_argument.access_key,
            secret_key=self.target_argument.secret_key,
            secure=False,
        )

        # create bucket if it does not exists
        if not client.bucket_exists(self.target_argument.bucket_name):
            client.make_bucket(self.target_argument.bucket_name)

        client.put_object(
            object_name=file_path_key,
            data=buffer_to_upload,
            bucket_name=self.target_argument.bucket_name,
            length=self.target_argument.length,
            part_size=self.target_argument.part_size,
        )
        return True

    def pipeline(self, file_prefix):
        """Function to run all required ETL steps together"""
        for each_s3_file_path in self.extract(file_prefix):
            try:
                file_path = (
                    "https://"
                    + self.source_argument.endpoint_url
                    + "/"
                    + self.source_argument.bucket_name
                    + "/"
                    + each_s3_file_path
                )
                profile = self.transform(file_path)
                self.load(
                    file_path_key=each_s3_file_path.split(".")[0] + ".json",
                    buffer_to_upload=profile,
                )

            except Exception as e:
                print(f"COULD NOT CREATE PROFILE: {e}")


def main():
    env_configs = dotenv_values(ENV_FILE_PATH)

    # assing all env values to variables
    source_configs = ETLSourceConfig(**json.loads(env_configs.get("source")))
    clean_config = ETLTransformConfig(
        **json.loads(env_configs.get("transform"))
    )
    target_configs = ETLTargetConfig(**json.loads(env_configs.get("target")))

    session_etl = ETLSession(
        source_argument=source_configs,
        transform_argument=clean_config,
        target_argument=target_configs,
    )

    session_etl.pipeline(file_prefix="fci/data/processed")


if __name__ == "__main__":
    main()
