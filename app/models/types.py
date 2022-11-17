from typing import Optional

from pydantic.main import BaseModel


class Types(BaseModel):
    Numeric: Optional[int]
    Categorical: Optional[int]
    Unsupported: Optional[int]

    class Config:
        underscore_attrs_are_private = True
