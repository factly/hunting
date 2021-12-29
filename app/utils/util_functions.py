import datetime
import json
from io import BytesIO
from pathlib import Path

import numpy as np
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from minio import Minio
from numpy import bool_
from pandas import read_csv
from pandas_profiling import ProfileReport

from app.core.config import Settings
from app.utils.profile_segments import ProfileSegments
from app.utils.tasks_functions import create_new_task, update_tasks_report

setting = Settings()


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


def provide_dataframe(
    file_url: str, source="url", s3_client: Minio = None, bucket: str = None
):
    """Functionality to provide dataframe from various sources

    Args:
        file_url (str): URL to the file to be read
        source (str, optional): Various sources from where file can be read.\
                                Defaults to "url".
        s3_client (Minio, optional): Minio Client Object to bucket ,\
                                if source is "s3". Defaults to None.
        bucket (str, optional): Name of bucket under which file is present.\
                                Defaults to None.

    Returns:
        [type]: [description]
    """
    # read any thing and provide proper dataframe instance
    # link : str, validate as proper url

    if source == "s3":
        obj = s3_client.get_object(bucket, file_url)
        df = read_csv(obj)

    # use link from file present in mande Studio
    # dataframe : dataframe
    # csv file path : str
    if source == "url":
        df = read_csv(file_url, na_values="NA")
    return df


async def _create_minio_client(endpoint, key, secret, secure):
    """Functionality to create Minio Client

    Args:
        endpoint (str): End point to connect to Minio
        key (str): Access key
        secret (str): Password / Secret key
        secure (Bool): Connect to Minio securely or not

    Raises:
        HTTPException: Failed to create Minio Client,\
                due to improper parameters

    Returns:
        Minio Client: Minio connection clients
    """
    try:
        minio_client = Minio(
            endpoint=endpoint,
            access_key=key,
            secret_key=secret,
            secure=secure,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create Minio Client",
            headers={"error_message": f"{e}"},
        )
    else:
        return minio_client


async def _list_files_under_s3_folder(
    source_client, source_folder_path, format=None
):
    """Functionality to list down all files present in s3 bucket\
            with provided prefix

    Args:
        source_client (Minio-Client): Minio Client for the source bucket
        source_folder_path (str): folder path to list files, this is a prefix
        format (str, optional): File extension for files to consider.\
                                Defaults to None.

    Returns:
        List[Minio Object]: List of all files present in the bucket ,\
                            with provided prefix and extension
    """
    # get list of files under the source folder
    objects = list(
        source_client.list_objects(
            setting.S3_BUCKET, recursive=True, prefix=source_folder_path
        )
    )

    # filter operation to only process certail file extensions
    if format:
        objects = list(
            filter(
                lambda object: object.object_name.split(".")[-1] == format,
                objects,
            )
        )

    return objects


async def _perform_hunting(
    path, actions, minimal, minio_client, files_sources: str
):
    """Functionality to perform hunting on the provided file

    Args:
        path (str): source location of file, could be url or s3 file path
        actions (str): Various parts of json profiles required
        minimal (bool): Provide minimal profile or not
        minio_client (Minio Client): Minio Client connected to source bucket
        files_sources (str): Provide source of file, could be "url" or "s3"

    Returns:
        Dict: hunting response in json format
    """
    # get dataframe from source
    dataframe = provide_dataframe(
        path,
        source=files_sources,
        bucket=setting.S3_BUCKET,
        s3_client=minio_client,
    )

    # generate class to segment profile
    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        samples={"head": 10, "tail": 10},
        show_variable_description=False,
        progress_bar=False,
    )
    profile_actions = ProfileSegments(profile)
    # description = profile.get_description()

    # perform functionality on dataframe for each function
    response = {}
    for each_action in actions:
        response[each_action] = getattr(profile_actions, each_action)()

    return response


async def _put_profiles_to_destination(
    path, destination, profile_report, minio_client
):
    """Functionality to put profiles to destination"""
    # destination file_path is made up of source folder structure and file_name
    file_path = Path(path)
    file_path = file_path.with_name(f"hunting_{file_path.name}").with_suffix(
        ".json"
    )
    # dest_folder_structure = path.split(source)[-1].lstrip("/")
    destination_file_path = (destination + "/" + str(file_path)).strip("/")
    # make buffer from response received, This buffer is saved to s3
    json_compatible_data = jsonable_encoder(profile_report)
    # converting json response to Bytes object
    out_buffer = BytesIO(json.dumps(json_compatible_data).encode("utf-8"))
    # put buffer bytes object to destination
    if not minio_client.bucket_exists(setting.S3_BUCKET):
        minio_client.make_bucket(setting.S3_BUCKET)
    minio_client.put_object(
        object_name=destination_file_path,
        data=out_buffer,
        bucket_name=setting.S3_BUCKET_TARGET,
        length=-1,
        part_size=10485760,
    )

    return destination_file_path


async def _to_s3_bulk_from_file_urls(
    sources, actions, minimal, destination, task_id
):
    """Functionality to perform hunting on the provided file.\
        This functions serves as background process

    Args:
        sources (List[str]): List of source file urls
        actions (List[str]): Various actions to perform on the dataframe
        minimal (Bool): Provide minimal profile or not
        destination (str): Folder name of path within Target bucket
        task_id (str): Task id of the task
    """
    try:
        target_minio_client = await _create_minio_client(
            endpoint=setting.S3_ENDPOINT_TARGET,
            key=setting.S3_KEY_TARGET,
            secret=setting.S3_SECRET_TARGET,
            secure=setting.S3_SECURE_TARGET,
        )
    except Exception as e:
        raise f"{e}"

    _ = await create_new_task(id=task_id, file_count=len(sources))

    for source in sources:
        try:
            profile_report = await _perform_hunting(
                path=source,
                actions=actions,
                minimal=minimal,
                files_sources="url",
                minio_client=None,
            )
            destination_file_path = await _put_profiles_to_destination(
                path=source.split("/")[-1],
                destination=destination,
                profile_report=profile_report,
                minio_client=target_minio_client,
            )
            err_msg = None
            error = False
        except Exception as e:
            err_msg = e
            error = True
            destination_file_path = None
        finally:
            await update_tasks_report(
                source_file_path=source,
                success_file_path=destination_file_path,
                error=error,
                err_msg=f"{err_msg}",
                task_id=task_id,
            )


async def _bulk_s3_folder(
    source_folder_path, actions, destination, format, task_id, minimal
):
    """Functionality to perform hunting on the provided file under S3 bucket.\
        This functions serves as background process

    Args:
        source_folder_path (str): Folder path under source bucket ,\
                                    where datasets are present
        actions (List[str]): Various actions to perform on the dataframe
        minimal (Bool): Provide minimal profile or not
        destination (str): Folder name of path within Target bucket
        task_id (str): Task id of the task
        format (str): File Extension for file types to consider
    """
    # create a minio client
    try:
        source_minio_client = await _create_minio_client(
            endpoint=setting.S3_ENDPOINT,
            key=setting.S3_KEY,
            secret=setting.S3_SECRET,
            secure=setting.S3_SECURE,
        )

        target_minio_client = await _create_minio_client(
            endpoint=setting.S3_ENDPOINT_TARGET,
            key=setting.S3_KEY_TARGET,
            secret=setting.S3_SECRET_TARGET,
            secure=setting.S3_SECURE_TARGET,
        )
    except Exception as e:
        raise f"{e}"
    # create task ID
    datasets = await _list_files_under_s3_folder(
        source_minio_client, source_folder_path, format=format
    )
    _ = await create_new_task(id=task_id, file_count=len(datasets))

    # iterate over list of files from S3 bucket
    for each_dataset in datasets:
        try:
            # perform hunting on each dataset
            profile_report = await _perform_hunting(
                path=each_dataset.object_name,
                actions=actions,
                minimal=minimal,
                minio_client=source_minio_client,
                files_sources="s3",
            )
            # put the buffer to s3
            destination_file_path = await _put_profiles_to_destination(
                path=each_dataset.object_name,
                destination=destination,
                profile_report=profile_report,
                minio_client=target_minio_client,
            )
            err_msg = None
            error = False
        except Exception as e:
            err_msg = e
            error = True
            destination_file_path = None
            # add the destination file path to the task report
        finally:
            await update_tasks_report(
                source_file_path=each_dataset.object_name,
                success_file_path=destination_file_path,
                error=error,
                err_msg=f"{err_msg}",
                task_id=task_id,
            )
