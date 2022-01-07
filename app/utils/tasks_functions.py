import json
import uuid
from pathlib import Path, PosixPath
from typing import Union

from app.models.tasks import (
    Completed,
    Error,
    NamesOfFailedFileItem,
    NamesOfSuccessFileItem,
    Task,
)

TASK_FOLDER = Path(__file__).resolve().parents[2] / "task"
TASK_FOLDER.mkdir(exist_ok=True, parents=True)


async def create_task_id():
    """Functionality to provide a unique task id.

    Args:
        prefix (str, optional): Keyword of prefix if required.
                                Defaults to "bulk_to_s3".

    Returns:
        str: Uniquely generated uuid
    """
    return f"{str(uuid.uuid4())}"


async def create_new_task(
    id: str,
    file_count: int,
) -> Task:
    """Functionality to create a new task, and save its report to the task folder.

    Args:
        id (str): Unique task id
        file_count (int): Count of files undergoing Hunting

    Returns:
        Task: Task object with provided details
    """
    task = Task(
        task_id=id,
        number_of_files=file_count,
        completed=Completed(number_of_files=0, names_of_file=[]),
        error=Error(number_of_files=0, names_of_file=[]),
    )
    with open(TASK_FOLDER / f"{id}.json", "w") as task_report:
        json.dump(task.dict(), task_report)
    return task


async def update_tasks_report(
    source_file_path: str,
    success_file_path: Union[str, None],
    error: bool,
    err_msg: str,
    task_id: str,
    task_folder: PosixPath = TASK_FOLDER,
):
    """Functionality to update the task report.

    Args:
        source_file_path (str): Key or File path of the source file
            undergoing Hunting
        success_file_path (Union[str, None]): key or file path here
            Profile report saved
        error (bool): Boolean flag to indicate if Hunting process
            on a was successful or not
        task_id (str): Unique task id
        task_folder (PosixPath, optional): "task" folder location ,
            where all task reports are saved. Defaults to TASK_FOLDER.
    """
    # load the json file
    try:
        task_details = json.load(open(task_folder / f"{task_id}.json"))
    except FileNotFoundError as e:
        print(f"{e}")
        raise
    else:
        if not error:
            # update the task details
            task_details["completed"]["number_of_files"] += 1
            task_details["completed"]["names_of_file"].append(
                NamesOfSuccessFileItem(
                    input_file_name=source_file_path,
                    output_file_name=success_file_path,
                ).dict()
            )
        else:
            task_details["error"]["number_of_files"] += 1
            task_details["error"]["names_of_file"].append(
                NamesOfFailedFileItem(
                    input_file_name=source_file_path,
                    error_message=err_msg,
                ).dict()
            )
        # write the task details to the json file
        with open(task_folder / f"{task_id}.json", "w") as task_report:
            json.dump(task_details, task_report)


async def get_all_tasks(
    limit: int,
):
    """Functionality to get all tasks."""
    # consider all files present inside the Task Folder
    task_id_files = [each_file for each_file in TASK_FOLDER.glob("*.json")]

    # check if limit is lower or number of tasks
    limit = min(limit, len(task_id_files))

    # read all tasks and then return
    tasks = [
        json.load(each_file.open()) for each_file in task_id_files[:limit]
    ]
    return tasks


async def get_task_by_id(
    task_id: str,
):
    """Functionality to get a task by its id."""
    # consider all files present inside the Task Folder
    task_id_files = [
        each_file for each_file in TASK_FOLDER.glob(f"*{task_id}.json")
    ]

    # read the task and then return
    task = json.load(task_id_files[0].open())
    return task
