from __future__ import annotations

from pydantic import BaseModel


class Package(BaseModel):
    pandas_profiling_version: str
    pandas_profiling_config: str