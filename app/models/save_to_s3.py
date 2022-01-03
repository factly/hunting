from typing import List, Optional

from pydantic import BaseModel

from app.core.config import Settings
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

settings = Settings()


class RequestSaveToS3(BaseModel):
    hunting_operation_api: str = (
        "http://0.0.0.0:8000/api/v1/profile/description/"
    )
    target_bucket_name: str = settings.S3_BUCKET
    target_access_key: str = settings.S3_KEY
    target_secret_key: str = settings.S3_SECRET
    target_bucket_endpoint: str = "localhost:9000"
    file_name: str = "output.json"
    source: str = settings.EXAMPLE_URL


class To_s3_response(BaseModel):
    analysis: Optional[Analysis]
    table: Optional[Table]
    variables: Optional[Variables]
    scatter: Optional[Scatter]
    correlations: Optional[Correlations]
    missing: Optional[Missing]
    alerts: Optional[Alerts]
    package: Optional[Package]
    sample: Optional[List[Sample]]
    duplicates: Optional[Duplicates]
