from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class Analysis(BaseModel):
    title: Optional[str]
    date_start: Optional[datetime]
    date_end: Optional[datetime]

    class Config:
        underscore_attrs_are_private = True
