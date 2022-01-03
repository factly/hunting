from typing import List

from pydantic import BaseModel

from app.models.alerts import Alerts
from app.models.analysis import Analysis
from app.models.correlations import Correlations
from app.models.duplicates import Duplicates
from app.models.missing import Missing
from app.models.package import Package
from app.models.sample import Sample
from app.models.scatter import Scatter
from app.models.table import Table
from app.models.variables import Variables


class Description(BaseModel):
    analysis: Analysis
    table: Table
    variables: Variables
    scatter: Scatter
    correlations: Correlations
    missing: Missing
    alerts: Alerts
    package: Package
    samples: List[Sample]
    duplicates: Duplicates
