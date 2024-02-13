from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Alerts(BaseModel):
    __root__: Optional[List[str]]
