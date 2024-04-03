from math import isnan
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, constr, validator

from app.core.config import Settings

settings = Settings()
VARIABLE_COLUMN_CONSTRAINT = constr(regex=settings.COLUMN_NAME_REGEX_PATTERN)


class VariableProperties(BaseModel):
    n_distinct: Optional[int]
    p_distinct: Optional[float]
    is_unique: Optional[bool]
    n_unique: Optional[int]
    p_unique: Optional[float]
    type: Optional[str]
    hashable: Optional[bool]
    ordering: Optional[bool]
    n_missing: Optional[int]
    n: Optional[int]
    p_missing: Optional[int]
    count: Optional[int]
    memory_size: Optional[int]
    n_negative: Optional[int]
    p_negative: Optional[int]
    n_infinite: Optional[int]
    n_zeros: Optional[int]
    mean: Optional[float]
    std: Optional[float]
    variance: Optional[float]
    min: Optional[Any]
    max: Optional[Any]
    kurtosis: Optional[float]
    skewness: Optional[float]
    sum: Optional[float]
    mad: Optional[float]
    range: Optional[float]
    field_5_: Optional[Union[float, None]] = Field(None, alias="5%")
    field_25_: Optional[Union[float, None]] = Field(None, alias="25%")
    field_50_: Optional[Union[float, None]] = Field(None, alias="50%")
    field_75_: Optional[Union[int, None]] = Field(None, alias="75%")
    field_95_: Optional[Union[float, None]] = Field(None, alias="95%")
    iqr: Optional[float]
    cv: Optional[float]
    p_zeros: Optional[float]
    p_infinite: Optional[int]
    monotonic_increase: Optional[bool]
    monotonic_decrease: Optional[bool]
    monotonic_increase_strict: Optional[bool]
    monotonic_decrease_strict: Optional[bool]
    monotonic: Optional[int]
    histogram: Optional[List[Any]]

    @validator("*")
    def change_nan_to_none(cls, v, field):
        if field.outer_type_ is float and isnan(v):
            return None
        return v


class Variables(BaseModel):
    __root__: Dict[VARIABLE_COLUMN_CONSTRAINT, VariableProperties]
