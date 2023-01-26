from pydantic import BaseModel

from app.models.types import Types


class Table(BaseModel):
    n: int
    n_var: int
    _memory_size: int
    _record_size: float
    _n_cells_missing: int
    _n_vars_with_missing: int
    _n_vars_all_missing: int
    _p_cells_missing: float
    _types: Types

    class Config:
        underscore_attrs_are_private = True
