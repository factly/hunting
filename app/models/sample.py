from typing import Optional

from pydantic import Json
from pydantic.main import BaseModel


class Sample(BaseModel):
    id: Optional[str]
    data: Optional[Json]
    name: Optional[str]
    caption: Optional[str] = None

    class Config:
        underscore_attrs_are_private = True
