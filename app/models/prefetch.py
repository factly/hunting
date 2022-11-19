from pydantic import BaseModel, Field


class Prefetch(BaseModel):
    urls: list[str] = Field(..., min_items=1)
    minimal: bool = Field(default=True)
    samples_to_fetch: int = Field(ge=0, default=10)

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
            }
        }
