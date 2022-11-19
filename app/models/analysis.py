from datetime import datetime, timedelta

from pydantic.main import BaseModel


class Analysis(BaseModel):
    title: str
    date_start: datetime
    date_end: datetime
    duration: timedelta
