from datetime import datetime, timedelta
from typing import Optional

from pydantic.main import BaseModel


class Analysis(BaseModel):
    title: Optional[str]
    date_start: Optional[datetime]
    date_end: Optional[datetime]
    duration: Optional[timedelta]

    class Config:
        underscore_attrs_are_private = True
