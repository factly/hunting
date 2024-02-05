from typing import Optional

from pydantic import BaseModel

from app.models.types import Types


class Table(BaseModel):
    n: Optional[int]
    n_var: Optional[int]
    _memory_size: Optional[int]
    _record_size: Optional[float]
    _n_cells_missing: Optional[int]
    _n_vars_with_missing: Optional[int]
    _n_vars_all_missing: Optional[int]
    _p_cells_missing: Optional[float]
    _types: Optional[Types]

    class Config:
        underscore_attrs_are_private = True
