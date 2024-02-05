from __future__ import annotations

from typing import List, Optional

from pydantic import RootModel


class Alerts(RootModel[Optional[List[str]]]):
    pass
