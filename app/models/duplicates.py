from typing import Union

from pydantic import BaseModel, Json


class Duplicates(BaseModel):
    __root__: Union[Json, str]
