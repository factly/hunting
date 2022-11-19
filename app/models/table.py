from pydantic import BaseModel

from app.models.types import Types


class Table(BaseModel):
    n: int
    n_var: int
    memory_size: int
    record_size: float
    n_cells_missing: int
    n_vars_with_missing: int
    n_vars_all_missing: int
    p_cells_missing: float
    types: Types
