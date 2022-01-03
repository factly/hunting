import json
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status

from app.core.config import Settings
from app.models.tasks import Task
from app.utils.tasks_functions import create_task_id
from app.utils.util_functions import (
    _bulk_s3_folder,
    _to_s3_bulk_from_file_urls,
)

s3_event_router = router = APIRouter()
setting = Settings()


@router.get(
    "/to_s3/bulk/from_file_urls/",
    summary="Bulk upload to S3 bucket from file urls",
    status_code=status.HTTP_202_ACCEPTED,
)
async def to_s3_bulk_from_file_urls(
    bg_tasks: BackgroundTasks,
    sources: List[str] = Query(
        [setting.EXAMPLE_URL], description="Source URLs for the dataset"
    ),
    actions: List[str] = Query(
        ["description"],
        description="Actions represents different segments \
            of Pandas Profiling Report",
    ),
    minimal: bool = Query(True, description="Minimal or not"),
    destination: str = Query(
        "destination", description="Destination folder to target s3 bucket"
    ),
    task_id_prefix: str = Query(
        "bulk_from_file_urls", description="Prefix for task id"
    ),
):
    """
    Functionality to create required Pandas Profiling and\
        upload it to targeted S3 bucket
    """
    # create task for each source
    task_id = await create_task_id(task_id_prefix)

    bg_tasks.add_task(
        _to_s3_bulk_from_file_urls,
        sources=sources,
        actions=actions,
        minimal=minimal,
        destination=destination,
        task_id=task_id,
    )

    return {"task_id": task_id, "message": "Process Running in Background"}


@router.get(
    "/to_s3/bulk/from_s3/",
    summary="Bulk upload Profiles to S3 bucket\
        for datasets present in a S3 folder",
    status_code=status.HTTP_202_ACCEPTED,
)
async def to_s3_bulk_upload_folder(
    bg_tasks: BackgroundTasks,
    source_folder_path: str = Query(
        None, description="Folder path where all datasets are present"
    ),
    file_format: str = Query("csv", description="File format of the files"),
    destination_folder_path: str = Query(
        "",
        description="Folder path where all datasets are to be uploaded",
    ),
    actions: List[str] = Query(["description"]),
    minimal: bool = Query(True, description="Minimal or not"),
    task_id_prefix: str = "bulk_s3_folder",
):
    """
    Functionality to create Pandas Profiling of datasets present \
        in a S3 folder and upload it to targeted S3 bucket
    """
    task_id = await create_task_id(task_id_prefix)

    bg_tasks.add_task(
        _bulk_s3_folder,
        source_folder_path=source_folder_path,
        format=file_format,
        destination=destination_folder_path,
        actions=actions,
        minimal=minimal,
        task_id=task_id,
    )
    return {"task_id": task_id, "message": "Process Running in Background"}


@router.get("/bulk/task/id/", summary="Get all Tasks Ids")
async def get_bg_tasks():
    """
    Functionality to retrieve all tasks ids of the background processed evoked
    """
    # go to temp folder and get all files names present
    temp_folder = Path(__file__).resolve().parents[4].joinpath("temp")
    temp_folder.mkdir(exist_ok=True, parents=True)

    files = [
        each_file.stem
        for each_file in temp_folder.iterdir()
        if each_file.is_file()
    ]

    return {"tasks": len(files), "tasks_ids": files}


@router.get(
    "/bulk/task/details/",
    summary="Get details of a specific task",
    response_model=Task,
    response_model_exclude_none=True,
)
async def get_task_stauts(
    task_id: str = Query(None, description="ID of task running in Background"),
):
    """
    Functionlaity to retrieve details of a specific task
    """
    # go to temp folder and get all files names present
    temp_folder = Path(__file__).resolve().parents[4].joinpath("temp")
    temp_folder.mkdir(exist_ok=True, parents=True)

    # get all task available
    task_id_file = [
        each_file for each_file in temp_folder.glob(f"*{task_id}.json")
    ]

    if not task_id_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{task_id} is not a valid TASK_ID",
        )  # {"message" : "Task Id not present"}

    task_details = json.load(task_id_file[0].open())

    return task_details
