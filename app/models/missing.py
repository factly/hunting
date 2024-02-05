from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Bar(BaseModel):
    name: Optional[str]
    caption: Optional[str]
    matrix: Optional[str]


class Matrix(BaseModel):
    name: Optional[str]
    caption: Optional[str]
    matrix: Optional[str]


class Heatmap(BaseModel):
    name: Optional[str]
    caption: Optional[str]
    matrix: Optional[str]


class Dendrogram(BaseModel):
    name: Optional[str]
    caption: Optional[str]
    matrix: Optional[str]


class Missing(BaseModel):
    bar: Optional[Bar] = None
    matrix: Optional[Matrix] = None
    heatmap: Optional[Heatmap] = None
    dendrogram: Optional[Dendrogram] = None

    class Config:
        underscore_attrs_are_private = True
