from __future__ import annotations

from typing import Dict, Optional, Union

from pydantic import BaseModel, Json


class Correlations(BaseModel):
    spearman: Optional[Union[Json, Dict]]
    pearson: Optional[Union[Json, Dict]]
    kendall: Optional[Union[Json, Dict]]
    cramers: Optional[Union[Json, Dict]]
    phi_k: Optional[Union[Json, Dict]]
