from typing import List

from pydantic import BaseModel

from app.models.task import Task


class TaskList(BaseModel):
    total_tasks: int
    maximum_page_size: int
    tasks: List[Task]
