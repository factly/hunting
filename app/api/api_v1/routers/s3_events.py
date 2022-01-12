from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status

from app.core.config import Settings
from app.models.enums import ProfileActions
from app.models.task import Task
from app.models.tasks import Tasks
from app.utils.tasks_functions import (
    create_task_id,
    get_all_tasks,
    get_task_by_id,
)
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
        type=ProfileActions,
        default=[ProfileActions.SAMPLES, ProfileActions.ANALYSIS],
        description="Actions represents different segments \
            of Pandas Profiling Report",
    ),
    minimal: bool = Query(True, description="Minimal or not"),
    destination: str = Query(
        "destination", description="Destination folder to target s3 bucket"
    ),
):
    """
    Functionality to create required Pandas Profiling and\
        upload it to targeted S3 bucket
    """
    # create task for each source
    task_id = await create_task_id()

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
):
    """
    Functionality to create Pandas Profiling of datasets present \
        in a S3 folder and upload it to targeted S3 bucket
    """
    task_id = await create_task_id()

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


@router.get(
    "/bulk/tasks",
    summary="Get all Tasks Ids",
    response_model=Tasks,
    response_model_exclude_none=True,
)
async def get_bg_tasks(skip: int = 0, limit: int = 10):
    """
    Functionality to retrieve all tasks ids of the background processed evoked
    """

    all_tasks = await get_all_tasks(skip=skip, limit=limit)

    return all_tasks


@router.get(
    "/bulk/tasks/{id}",
    summary="Get details of a specific task",
    response_model=Task,
    response_model_exclude_none=True,
)
async def get_task_stauts(
    id: str = Query(None, description="ID of task running in Background"),
):
    """
    Functionlaity to retrieve details of a specific task
    """
    try:
        task = await get_task_by_id(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task ID not found",
            headers={"X-Error": str(e)},
        )
    else:
        return task
