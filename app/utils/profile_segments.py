import datetime
import json
from typing import Any, Dict, List, Union

import numpy as np
from numpy import bool_
from pandas import DataFrame
from pydantic import parse_obj_as

from app.core.config import Settings
from app.models.analysis import Analysis
from app.models.missing import Missing
from app.models.package import Package
from app.models.sample import Sample
from app.models.scatter import Scatter
from app.models.table import Table

settings = Settings()


def json_conversion_objects(obj):
    """Fix improper objects while creating json
    Function use to convert non-JSON serializable objects to proper format
    Args:
        obj ([datetime,np.generic]): Object required to convert to json
    Returns:
        obj: JSON Serializable object
    """
    if isinstance(obj, bool_):
        return bool(obj)
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    if isinstance(obj, np.generic):
        return obj.item()


"""This class provides different segments of Pandas profile"""


class ProfileSegments:
    def __init__(self, pandas_profile, columns=None, round_to=3):
        """
        Pass pandas profile of a dataset as argument
        """
        self.pandas_profile = pandas_profile
        self.profile_description = pandas_profile.get_description()
        self.col_order = columns
        self.round_to = round_to

    def analysis(self) -> Dict:
        return parse_obj_as(
            Analysis, self.profile_description.analysis.__dict__
        ).dict()

    def table(self) -> Dict:
        return parse_obj_as(Table, self.profile_description.table).dict()

    def variables(self) -> Dict:
        # get variables
        variables = json.dumps(
            self.profile_description.variables,
            default=json_conversion_objects,
        ).replace("NaN", '"NaN"')
        mod_var = json.loads(variables)
        return mod_var

    def scatter(self) -> Dict:
        return parse_obj_as(
            Scatter, {"data": self.profile_description.scatter}
        ).dict()

    def correlations(self) -> Dict[str, Any]:
        # get correlations
        correlation = self.profile_description.correlations
        modified_corr = {}
        for each_corr in correlation:
            modified_corr[each_corr] = correlation[each_corr].to_json()
        return modified_corr

    def missing(self) -> Dict:
        return parse_obj_as(Missing, self.profile_description.missing).dict()

    def alerts(self) -> List[str]:
        all_alerts = []
        provided_alerts = self.profile_description.alerts
        for each_alert in provided_alerts:
            all_alerts.append(f"{each_alert}")
        return all_alerts

    def package(self) -> Dict:
        return parse_obj_as(Package, self.profile_description.package).dict()

    def samples(self) -> List[Sample]:
        # get samples
        samples = self.profile_description.sample
        for sample in samples:
            sample.data = sample.data.round(decimals=self.round_to).to_json()
        # * 'head' and 'tail' are returned as dataset sample
        # * use env variable to select `hear` or `tail` or `both`
        return [
            sample
            for sample in samples
            if sample.id in settings.SAMPLE_DATA_RENDERER
        ]

    def duplicates(self) -> Union[str, Dict]:
        # get duplicates
        duplicates = self.profile_description.duplicates
        if isinstance(duplicates, DataFrame):
            mod_duplicates = duplicates.to_json()
        else:
            mod_duplicates = "None"
        return mod_duplicates

    def columns(self) -> Union[List[str], None]:
        return self.col_order

    def description(self, attrs: Union[str, None] = None) -> Dict:
        # require comma separated values for segments that are required to fetch
        if attrs is not None:
            attr_func_mapper = {
                "analysis": self.analysis,
                "table": self.table,
                "variables": self.variables,
                "scatter": self.scatter,
                "correlations": self.correlations,
                "missing": self.missing,
                "alerts": self.alerts,
                "package": self.package,
                "samples": self.samples,
                "duplicates": self.duplicates,
                "columns": self.columns,
            }
            return {
                attr: attr_func_mapper[attr]() for attr in attrs.split(",")
            }
        else:
            return {
                "analysis": self.analysis(),
                "table": self.table(),
                "variables": self.variables(),
                "scatter": self.scatter(),
                "correlations": self.correlations(),
                "missing": self.missing(),
                "alerts": self.alerts(),
                "package": self.package(),
                "samples": self.samples(),
                "duplicates": self.duplicates(),
                "columns": self.columns(),
            }
