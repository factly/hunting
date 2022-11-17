import datetime
import json
from typing import List, Union

import numpy as np
from numpy import bool_
from pandas import DataFrame
from pydantic import parse_obj_as

from app.core.config import Settings
from app.models.alerts import Alerts
from app.models.analysis import Analysis
from app.models.correlations import Correlations
from app.models.description import Description
from app.models.duplicates import Duplicates
from app.models.missing import Missing
from app.models.package import Package
from app.models.sample import Sample
from app.models.scatter import Scatter
from app.models.table import Table
from app.models.variables import Variables

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
    def __init__(self, pandas_profile, columns_order=None):
        """
        Pass pandas profile of a dataset as argument
        """
        self.pandas_profile = pandas_profile
        self.profile_description = pandas_profile.get_description()
        self.col_order = columns_order

    def analysis(self) -> Analysis:
        return parse_obj_as(
            Analysis, self.profile_description["analysis"]
        ).dict()

    def table(self) -> Table:
        return parse_obj_as(Table, self.profile_description["table"]).dict()

    def variables(self) -> Variables:
        # get variables
        variables = json.dumps(
            self.profile_description["variables"],
            default=json_conversion_objects,
        ).replace("NaN", '"NaN"')
        mod_var = json.loads(variables)
        return mod_var

    def scatter(self) -> Scatter:
        return parse_obj_as(
            Scatter, self.profile_description["scatter"]
        ).dict()

    def correlations(self) -> Correlations:
        # get correlations
        correlation = self.profile_description.get("correlations", {})
        modified_corr = {}
        for each_corr in correlation:
            modified_corr[each_corr] = correlation[each_corr].to_json()
        return modified_corr

    def missing(self) -> Missing:
        return parse_obj_as(
            Missing, self.profile_description["missing"]
        ).dict()

    def alerts(self) -> Alerts:
        all_alerts = []
        provided_alerts = self.profile_description.get("alerts", [])
        for each_alert in provided_alerts:
            all_alerts.append(f"{each_alert}")
        return all_alerts

    def package(self) -> Package:
        return parse_obj_as(
            Package, self.profile_description["package"]
        ).dict()

    def samples(self) -> List[Sample]:
        # get samples
        samples = self.pandas_profile.get_sample()
        for sample in samples:
            sample.data = sample.data.to_json()
        print(type(samples))
        # * 'head' and 'tail' are returned as dataset sample
        # * use env variable to select `hear` or `tail` or `both`
        return [
            sample
            for sample in samples
            if sample.id in settings.SAMPLE_DATA_RENDERER
        ]

    def duplicates(self) -> Duplicates:
        # get duplicates
        duplicates = self.pandas_profile.get_duplicates()
        if isinstance(duplicates, DataFrame):
            mod_duplicates = duplicates.to_json()
        else:
            mod_duplicates = "None"
        return mod_duplicates

    def columns_order(self) -> Union[List[str], None]:
        return self.col_order

    def description(self) -> Description:
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
            "columns_order": self.columns_order(),
        }
