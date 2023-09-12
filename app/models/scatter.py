from __future__ import annotations

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel


class Scatter(BaseModel):
    data: Optional[Union[Dict, Any]]
