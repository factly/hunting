import datetime
from urllib.parse import urlparse

import numpy as np
import polars as pl
import polars.exceptions as pl_exc
import s3fs
from charset_normalizer import from_bytes
from fastapi.logger import logger
from numpy import bool_
from requests import get

from app.core.config import Settings

setting = Settings()


def get_encoding(obj=None, url=None):
    if url:
        obj = get(url).content
    encoding = from_bytes(obj).best().encoding
    return encoding


async def get_dataframe_honouring_encoding_async(
    file_url: str,
) -> pl.DataFrame:
    try:
        df = pl.read_csv(file_url, null_values="NA", infer_schema_length=0)
    except (UnicodeDecodeError, pl_exc.ComputeError) as err:
        logger.exception(f"Could not interpret File encoding : {err}")
        encoding = get_encoding(url=file_url)
        logger.info(f"File encoding for `{file_url}` : {encoding}")
        df = pl.read_csv(
            file_url,
            null_values="NA",
            encoding=encoding,
            infer_schema_length=0,
        )
    return df


def get_dataframe_honouring_encoding(file_url: str) -> pl.DataFrame:
    try:
        df = pl.read_csv(file_url, null_values="NA", infer_schema_length=0)
    except (UnicodeDecodeError, pl_exc.ComputeError) as err:
        logger.exception(f"Could not interpret File encoding : {err}")
        encoding = get_encoding(url=file_url)
        logger.info(f"File encoding for `{file_url}` : {encoding}")
        df = pl.read_csv(
            file_url,
            null_values="NA",
            encoding=encoding,
            infer_schema_length=0,
        )
    return df


def json_conversion_objects(obj):
    """Fix improper objects while creating json
    Function use to convert non-JSON serializable objects to proper format
    Args:
        obj ([datetime,np.generic]): Object required to convert to json
    Returns:
        obj: JSON Serializable object
    """
    if isinstance(obj, bool_):
        return bool(obj)
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    if isinstance(obj, np.generic):
        return obj.item()


async def get_dataframe_async(file_url: str):
    """Functionality to provide dataframe from various sources

    Args:
        file_url (str): URL to the file to be read

    Returns:
        [type]: [description]
    """
    # read any thing and provide proper dataframe instance
    # link : str, validate as proper url
    # use link from file present in mande Studio

    url = urlparse(file_url)

    if url.scheme == "http" or url.scheme == "https":
        df = await get_dataframe_honouring_encoding_async(file_url)
        return df

    elif url.scheme == "s3":

        fs = s3fs.S3FileSystem(
            key=setting.S3_ACCESS_KEY_ID,
            secret=setting.S3_SECRET_ACCESS_KEY,
            client_kwargs={"endpoint_url": setting.S3_ENDPOINT_URL},
        )

        with fs.open(f"{url.netloc}{url.path}") as f:
            df = await get_dataframe_honouring_encoding_async(f)

        return df


def get_dataframe(file_url: str):
    """Functionality to provide dataframe from various sources

    Args:
        file_url (str): URL to the file to be read

    Returns:
        [type]: [description]
    """
    # read any thing and provide proper dataframe instance
    # link : str, validate as proper url
    # use link from file present in mande Studio

    url = urlparse(file_url)

    if url.scheme == "http" or url.scheme == "https":
        df = get_dataframe_honouring_encoding(file_url)
        return df

    elif url.scheme == "s3":

        fs = s3fs.S3FileSystem(
            key=setting.S3_ACCESS_KEY_ID,
            secret=setting.S3_SECRET_ACCESS_KEY,
            client_kwargs={"endpoint_url": setting.S3_ENDPOINT_URL},
        )

        with fs.open(f"{url.netloc}{url.path}") as f:
            df = get_dataframe_honouring_encoding(f)

        return df
