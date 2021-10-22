from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Json


class Correlations(BaseModel):
    spearman: Optional[Json]
    pearson: Optional[Json]
    kendall: Optional[Json]
    cramers: Optional[Json]
    phi_k: Optional[Json]
    # phi_k: Optional[List[Dict[str, Any]]]
    