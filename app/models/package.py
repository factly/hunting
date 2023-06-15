from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Package(BaseModel):
    ydata_profiling_version: Optional[str]
    ydata_profiling_config: Optional[str]

    class Config:
        underscore_attrs_are_private = True
