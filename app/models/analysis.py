from pydantic.main import BaseModel
from datetime import datetime, timedelta

class Analysis(BaseModel):
    title: str
    date_start: datetime
    date_end: datetime
    duration: timedelta