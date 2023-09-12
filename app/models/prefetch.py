from uuid import uuid4

from pydantic import BaseModel, Field


class Prefetch(BaseModel):
    urls: list[str] = Field(..., min_items=1)
    minimal: bool = Field(default=True)
    samples_to_fetch: int = Field(ge=0, default=10)
    trigger_id: str = Field(default=str(uuid4()))

    class Config:
        schema_extra = {
            "example": {
                "urls": [
                    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
                    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/WorldDBTables/CityTable.csv",
                    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/WorldDBTables/LanguageTable.csv",
                ],
                "minimal": True,
                "samples_to_fetch": 10,
                "trigger_id": "test_trigger_id",
            }
        }


class PrefetchResponse(BaseModel):
    task_id: str = Field(...)
    trigger_id: str = Field(...)
