from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Bar(BaseModel):
    name: str
    caption: str
    matrix: str


class Matrix(BaseModel):
    name: str
    caption: str
    matrix: str


class Heatmap(BaseModel):
    name: str
    caption: str
    matrix: str


class Dendrogram(BaseModel):
    name: str
    caption: str
    matrix: str


class Missing(BaseModel):
    bar: Optional[Bar] = None
    matrix: Optional[Matrix] = None
    heatmap: Optional[Heatmap] = None
    dendrogram: Optional[Dendrogram] = None

    class Config:
        underscore_attrs_are_private = True
