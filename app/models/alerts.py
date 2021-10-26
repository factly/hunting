from __future__ import annotations

from typing import List

# from pandas_profiling.model.alerts import Alert
from pydantic import BaseModel


class Alerts(BaseModel):
    # __root__ : List[Alert]
    __root__: List[str]

    # class Config:
    #     arbitrary_types_allowed = True
