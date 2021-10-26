import datetime
import json
from typing import List

from fastapi import APIRouter
from numpy import bool_
from pandas import DataFrame
from pandas_profiling import ProfileReport
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
from app.utils.utils import provide_dataframe

settings = Settings()

profile_router = router = APIRouter()


def json_conversion_objects(obj):
    """Fix improper objects while creating json
    Function use to convert non-JSON serializable objects to proper format
    Args:
        obj ([datetime,np.generic]): Object required to convert to json
    Returns:
        obj: JSON Serializable object
    """
    # if isinstance(obj, datetime.datetime):
    #     return obj.__str__()
    # if isinstance(obj, np.generic):
    #     return obj.item()
    if isinstance(obj, bool_):
        return bool(obj)
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


@router.get("/profile/raw")
def provide_raw_profiling(
    source: str = settings.EXAMPLE_URL, samples_to_show: int = 10
):
    """Provide Pandas-Profile for a dataset

    Args:
        source (str, optional): Source of the dataset, as of now only url, csv file path.  # noqa: E501
        Defaults to example_url (https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv).  # noqa: E501
        samples_to_show (int, optional): Samples of Dataset rows to display. Defaults to 10.  # noqa: E501

    Returns:
        response (json): Pandas-Profile in json
    """

    dataframe = provide_dataframe(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    if dataframe.shape[0] < 100:
        samples_to_show = 5

    profile = ProfileReport(
        dataframe,
        minimal=False,
        samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    # replacing all NaN Values to "NA" as NaN throws error
    json_profile = json.loads(profile.to_json().replace("NaN", '"NA"'))

    return json_profile


@router.get(
    "/profile/samples/",
    response_model=List[Sample],
    response_model_exclude_none=True,
)
def profile_samples(
    source: str = settings.EXAMPLE_URL, samples_to_show: int = 10
):
    """
    Get samples for data
    """

    dataframe = provide_dataframe(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    if dataframe.shape[0] < 100:
        samples_to_show = 5

    profile = ProfileReport(
        dataframe,
        minimal=True,
        samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    samples = profile.get_sample()

    # convert `data` filed from `dataframe` to `json`
    for sample in samples:
        sample.data = sample.data.to_json()

    return samples


@router.get(
    "/profile/description/table/",
    response_model=Table,
    response_model_exclude_none=True,
)
def profile_table(source: str = settings.EXAMPLE_URL):
    """
    Get table part of pandas profiling for data
    """

    dataframe = provide_dataframe(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    # if dataframe.shape[0] < 100:
    #     samples_to_show = 5

    profile = ProfileReport(
        dataframe,
        minimal=True,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    description = profile.get_description()

    table = parse_obj_as(Table, description["table"])

    return table


@router.get(
    "/profile/description/analysis/",
    response_model=Analysis,
    response_model_exclude_none=True,
)
def profile_analysis(source: str = settings.EXAMPLE_URL):
    """
    Get Analysis part of pandas profiling for data
    """

    dataframe = provide_dataframe(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    # if dataframe.shape[0] < 100:
    #     samples_to_show = 5

    profile = ProfileReport(
        dataframe,
        minimal=True,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    description = profile.get_description()

    analysis = parse_obj_as(Analysis, description["analysis"])

    return analysis


@router.get(
    "/profile/description/alerts",
    response_model=Alerts,
    response_model_exclude_none=True,
)
def profile_alerts(source: str = settings.EXAMPLE_URL):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=True,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    provided_alerts = profile.get_description().get("alerts", [])

    all_alerts = []
    for each_alert in provided_alerts:
        all_alerts.append(f"{each_alert}")

    # description = profile.get_description()
    # all_alerts = parse_obj_as(Alerts, description["alerts"])

    return all_alerts


@router.get(
    "/profile/description/scatter",
    response_model=Scatter,
    response_model_exclude_none=True,
)
def profile_scatter(source: str = settings.EXAMPLE_URL, minimal: bool = True):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    description = profile.get_description()

    scatter = parse_obj_as(Scatter, description["scatter"])

    return scatter


@router.get(
    "/profile/description/correlations",
    response_model=Correlations,
    response_model_exclude_none=True,
)
def profile_correlations(
    source: str = settings.EXAMPLE_URL, minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    correlation = profile.get_description().get("correlations", {})

    # each correlation was specified as pandas dataframe
    modified_corr = {}
    for each_corr in correlation:
        modified_corr[each_corr] = correlation[each_corr].to_json()

    return modified_corr


@router.get(
    "/profile/description/missing",
    response_model=Missing,
    response_model_exclude_none=True,
)
def profile_missing(source: str = settings.EXAMPLE_URL, minimal: bool = True):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    description = profile.get_description()

    missings = parse_obj_as(Missing, description["missing"])

    return missings


@router.get(
    "/profile/description/package",
    response_model=Package,
    response_model_exclude_none=True,
)
def profile_package(source: str = settings.EXAMPLE_URL, minimal: bool = True):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    description = profile.get_description()

    package = parse_obj_as(Package, description["package"])

    return package


@router.get(
    "/profile/description/variables",
    response_model=Variables,
    response_model_exclude_none=True,
)
def profile_variables(
    source: str = settings.EXAMPLE_URL, minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    # few objects are not json serializable and have type : numpy.bool_,
    # using default option
    variables = json.dumps(
        profile.get_description()["variables"], default=json_conversion_objects
    )
    # variables = parse_obj_as(Package, json.load(description["variables"]))
    mod_var = json.loads(variables)
    return mod_var


@router.get(
    "/profile/description/duplicates",
    response_model=Duplicates,
    response_model_exclude_none=True,
)
def profile_duplicates(
    source: str = settings.EXAMPLE_URL, minimal: bool = True
):

    dataframe = provide_dataframe(source)
    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    duplicates = profile.get_duplicates()
    if isinstance(duplicates, DataFrame):
        mod_duplicates = duplicates.to_json()
    else:
        mod_duplicates = "None"
    return mod_duplicates


@router.get(
    "/profile/description",
    response_model=Description,
    response_model_exclude_none=True,
)
def profile_description(
    source: str = settings.EXAMPLE_URL, minimal: bool = True
):
    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        # samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )
    description = profile.get_description()

    # get alerts
    provided_alerts = profile.get_description().get("alerts", [])
    all_alerts = []
    for each_alert in provided_alerts:
        all_alerts.append(f"{each_alert}")

    # get correlations
    correlation = profile.get_description().get("correlations", {})
    modified_corr = {}
    for each_corr in correlation:
        modified_corr[each_corr] = correlation[each_corr].to_json()

    variables = json.dumps(
        profile.get_description()["variables"], default=json_conversion_objects
    )
    mod_var = json.loads(variables)

    duplicates = profile.get_duplicates()
    if isinstance(duplicates, DataFrame):
        mod_duplicates = duplicates.to_json()
    else:
        mod_duplicates = "None"

    desc = {
        "table": parse_obj_as(Table, description["table"]),
        "analysis": parse_obj_as(Analysis, description["analysis"]),
        "alerts": all_alerts,
        "scatter": parse_obj_as(Scatter, description["scatter"]),
        "correlations": modified_corr,
        "missing": parse_obj_as(Missing, description["missing"]),
        "package": parse_obj_as(Package, description["package"]),
        "variables": mod_var,
        "duplicates": mod_duplicates,
    }
    return desc
