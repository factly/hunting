from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, constr

from app.core.config import Settings

settings = Settings()
VARIABLE_COLUMN_CONSTRAINT = constr(regex=settings.COLUMN_NAME_REGEX_PATTERN)


class VariableProperties(BaseModel):
    n_distinct: Optional[int]
    _p_distinct: Optional[float]
    _is_unique: Optional[bool]
    n_unique: Optional[int]
    _p_unique: Optional[float]
    type: Optional[str]
    _hashable: Optional[bool]
    _ordering: Optional[bool]
    _n_missing: Optional[int]
    _n: Optional[int]
    _p_missing: Optional[int]
    count: Optional[int]
    _memory_size: Optional[int]
    _n_negative: Optional[int]
    _p_negative: Optional[int]
    _n_infinite: Optional[int]
    _n_zeros: Optional[int]
    _mean: Optional[float]
    _std: Optional[float]
    _variance: Optional[float]
    _min: Optional[int]
    _max: Optional[float]
    _kurtosis: Optional[float]
    _skewness: Optional[float]
    _sum: Optional[float]
    _mad: Optional[float]
    _range: Optional[float]
    _field_5_: Optional[Union[float, None]] = Field(None, alias="5%")
    _field_25_: Optional[Union[float, None]] = Field(None, alias="25%")
    _field_50_: Optional[Union[float, None]] = Field(None, alias="50%")
    _field_75_: Optional[Union[int, None]] = Field(None, alias="75%")
    _field_95_: Optional[Union[float, None]] = Field(None, alias="95%")
    _iqr: Optional[float]
    _cv: Optional[float]
    _p_zeros: Optional[float]
    _p_infinite: Optional[int]
    _monotonic_increase: Optional[bool]
    _monotonic_decrease: Optional[bool]
    _monotonic_increase_strict: Optional[bool]
    _monotonic_decrease_strict: Optional[bool]
    _monotonic: Optional[int]
    _histogram: Optional[List[Any]]

    class Config:
        underscore_attrs_are_private = True


class Variables(BaseModel):
    __root__: Dict[VARIABLE_COLUMN_CONSTRAINT, VariableProperties]
