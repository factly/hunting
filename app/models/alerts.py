from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Alerts(BaseModel):
    # __root__ : List[Alert]
    __root__: List[str]

    class Config:
        underscore_attrs_are_private = True
