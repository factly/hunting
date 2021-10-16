from typing import Optional

from pydantic import Json
from pydantic.main import BaseModel


class Sample(BaseModel):
    id: str
    data: Json
    name: str
    caption: Optional[str] = None
