from typing import Optional

from pydantic.main import BaseModel
from pydantic import Json

class Sample(BaseModel):
    id: str
    data: Json
    name: str
    caption: Optional[str] = None
