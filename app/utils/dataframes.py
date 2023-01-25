import datetime
from typing import Union
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


def get_encoding(obj: Union[str, bytes], is_object=False) -> str:
    """Get encoding for a csv File for any given object url or file content in bytes

    Args:
        obj (Union[str, bytes]): obj is url in string format for URL or file content in bytes
        is_object (bool, optional): for file content in bytes pass True. Defaults to False.

    Returns:
        str: encoding name
    """
    if not is_object:
        obj: bytes = get(obj).content

    encoding: str = from_bytes(obj).best().encoding
    return encoding


async def get_dataframe_honouring_encoding_async(
    source: Union[str, bytes],
    is_object=False,
) -> pl.DataFrame:
    """Get Dataframe irrespective of encoding for csv file with async

    Args:
        source (Union[str, bytes]): source is url string incase for file url else incase for s3
                                    file content in bytes
        is_object (bool, optional): _description_. pass it as True in case for s3 file.

    Returns:
        pl.DataFrame: polars Dataframe object
    """
    try:
        df = pl.read_csv(source, null_values="NA", infer_schema_length=0)
    except (UnicodeDecodeError, pl_exc.ComputeError) as err:
        logger.error(f"Could not interpret File encoding : {err}")
        encoding = get_encoding(obj=source, is_object=is_object)
        logger.info(f"File encoding : {encoding}")
        df = pl.read_csv(
            source,
            null_values="NA",
            encoding=encoding,
            infer_schema_length=0,
        )
    return df


def get_dataframe_honouring_encoding(
    source: Union[str, bytes], is_object=False
) -> pl.DataFrame:
    """Get Dataframe irrespective of encoding for csv file with sync

    Args:
        source (Union[str, bytes]): source is url string incase for file url else incase for s3
                                    file content in bytes
        is_object (bool, optional): _description_. pass it as True in case for s3 file.

    Returns:
        pl.DataFrame: polars Dataframe object
    """
    try:
        df = pl.read_csv(source, null_values="NA", infer_schema_length=0)
    except (UnicodeDecodeError, pl_exc.ComputeError) as err:
        logger.error(f"Could not interpret File encoding : {err}")
        encoding = get_encoding(obj=source, is_object=is_object)
        logger.info(f"File encoding : {encoding}")
        df = pl.read_csv(
            source,
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
        logger.info("Check for files with s3 extension")
        fs = s3fs.S3FileSystem(
            key=setting.S3_ACCESS_KEY_ID,
            secret=setting.S3_SECRET_ACCESS_KEY,
            client_kwargs={"endpoint_url": setting.S3_ENDPOINT_URL},
        )

        with fs.open(f"{url.netloc}{url.path}", "rb") as f:
            obj = f.read()

        df = await get_dataframe_honouring_encoding_async(obj, is_object=True)
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
        df = get_dataframe_honouring_encoding(source=file_url, is_object=False)
        return df

    elif url.scheme == "s3":

        fs = s3fs.S3FileSystem(
            key=setting.S3_ACCESS_KEY_ID,
            secret=setting.S3_SECRET_ACCESS_KEY,
            client_kwargs={"endpoint_url": setting.S3_ENDPOINT_URL},
        )

        with fs.open(f"{url.netloc}{url.path}", "rb") as f:
            file_content = f.read()
        df = get_dataframe_honouring_encoding(
            source=file_content, is_object=True
        )
        return df
