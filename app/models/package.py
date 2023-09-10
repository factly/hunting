from __future__ import annotations

from pydantic import BaseModel


class Package(BaseModel):
    ydata_profiling_version: str
    ydata_profiling_version: str

    class Config:
        underscore_attrs_are_private = True
