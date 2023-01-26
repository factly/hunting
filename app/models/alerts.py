from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Alerts(BaseModel):
    __root__: List[str]
