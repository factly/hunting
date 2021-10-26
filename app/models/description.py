from pydantic import BaseModel

from app.models.alerts import Alerts
from app.models.analysis import Analysis
from app.models.correlations import Correlations
from app.models.duplicates import Duplicates
from app.models.missing import Missing
from app.models.package import Package
from app.models.scatter import Scatter
from app.models.table import Table
from app.models.variables import Variables


class Description(BaseModel):
    table: Table
    analysis: Analysis
    alerts: Alerts
    scatter: Scatter
    correlations: Correlations
    missing: Missing
    package: Package
    variables: Variables
    duplicates: Duplicates
