from typing import List, Optional, Set, Union

from pydantic import BaseModel, Field, validator

from app.core.config import Settings
from app.models.alerts import Alerts
from app.models.analysis import Analysis
from app.models.correlations import Correlations
from app.models.duplicates import Duplicates
from app.models.enums import ProfileActions
from app.models.missing import Missing
from app.models.package import Package
from app.models.sample import Sample
from app.models.scatter import Scatter
from app.models.table import Table
from app.models.variables import Variables

setting = Settings()


class Description(BaseModel):
    analysis: Optional[Analysis]
    table: Optional[Table]
    variables: Optional[Variables]
    scatter: Optional[Scatter]
    correlations: Optional[Correlations]
    missing: Optional[Missing]
    alerts: Optional[Alerts]
    package: Optional[Package]
    samples: Optional[List[Sample]]
    duplicates: Optional[Duplicates]
    columns: Optional[List[str]]


class ProfileDescriptionRequest(BaseModel):
    source: str = Field(default=setting.EXAMPLE_URL)
    minimal: bool = Field(default=True)
    samples_to_show: int = Field(ge=0, default=10)
    attrs: Union[str, None] = Field(default=None)

    @validator("attrs")
    def attrs_should_be_profile_actions(cls, v):
        if isinstance(v, str):
            query_params_set: Set[str] = {attr for attr in v.split(",")}
            valid_params_set: Set[str] = set(
                member.value for member in ProfileActions
            )

            if query_params_set - valid_params_set:
                raise ValueError(
                    f"Invalid query params passed among : {', '.join(query_params_set)}"
                )
            return v
        return v

    class Config:
        schema_extra = {
            "example": {
                "source": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
                "minimal": True,
                "samples_to_show": 10,
                "attrs": "analysis,samples",
            }
        }
