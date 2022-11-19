import datetime

import numpy as np
import polars as pl
from charset_normalizer import from_bytes
from numpy import bool_
from requests import get

from app.core.config import Settings

setting = Settings()


def get_encoding(obj=None, url=None):
    if url:
        obj = get(url).content
    encoding = from_bytes(obj).best().encoding
    return encoding


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


def get_dataframe(file_url: str, source="url"):
    """Functionality to provide dataframe from various sources

    Args:
        file_url (str): URL to the file to be read
        source (str, optional): Various sources from where file can be read.\
                                Defaults to "url".

    Returns:
        [type]: [description]
    """
    # read any thing and provide proper dataframe instance
    # link : str, validate as proper url
    # use link from file present in mande Studio
    try:
        df = pl.read_csv(file_url, null_values="NA")
    except UnicodeDecodeError:
        encoding = get_encoding(url=file_url)
        df = pl.read_csv(file_url, null_values="NA", encoding=encoding)
    return df
