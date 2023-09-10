from datetime import datetime

from pydantic.main import BaseModel


class Analysis(BaseModel):
    title: str
    date_start: datetime
    date_end: datetime
    # TIME DELTA IS REMOVED IN PROFILING VERSION 4 AND ABOVE
    # duration: timedelta

    class Config:
        underscore_attrs_are_private = True
