import json
from os import environ
from typing import List

from fastapi import APIRouter
from pandas_profiling import ProfileReport

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
from app.utils.profile_segments import ProfileSegments
from app.utils.util_functions import provide_dataframe

profile_router = router = APIRouter()


@router.get("/profile/raw/")
async def provide_raw_profiling(
    source: str = environ["EXAMPLE_URL"],
    samples_to_show: int = 10,
    minimal: bool = True,
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
        minimal=minimal,
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
async def profile_samples(
    source: str = environ["EXAMPLE_URL"], samples_to_show: int = 10
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

    # use `ProfileSegments` to get table part of pandas profiling
    profile_segment = ProfileSegments(profile)
    samples = profile_segment.samples()

    return samples


@router.get(
    "/profile/description/table/",
    response_model=Table,
    response_model_exclude_none=True,
)
async def profile_table(source: str = environ["EXAMPLE_URL"]):
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

    # use `ProfileSegments` to get table part of pandas profiling
    profile_segment = ProfileSegments(profile)
    table = profile_segment.table()

    return table


@router.get(
    "/profile/description/analysis/",
    response_model=Analysis,
    response_model_exclude_none=True,
)
async def profile_analysis(source: str = environ["EXAMPLE_URL"]):
    """
    Get Analysis part of pandas profiling for data
    """

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=True,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    analysis = profile_segment.analysis()

    return analysis


@router.get(
    "/profile/description/alerts/",
    response_model=Alerts,
    response_model_exclude_none=True,
)
async def profile_alerts(source: str = environ["EXAMPLE_URL"]):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=True,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    alerts = profile_segment.alerts()

    return alerts


@router.get(
    "/profile/description/scatter/",
    response_model=Scatter,
    response_model_exclude_none=True,
)
async def profile_scatter(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    scatter = profile_segment.scatter()

    return scatter


@router.get(
    "/profile/description/correlations/",
    response_model=Correlations,
    response_model_exclude_none=True,
)
async def profile_correlations(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    correlations = profile_segment.correlations()

    return correlations


@router.get(
    "/profile/description/missing/",
    response_model=Missing,
    response_model_exclude_none=True,
)
async def profile_missing(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    missing = profile_segment.missing()

    return missing


@router.get(
    "/profile/description/package/",
    response_model=Package,
    response_model_exclude_none=True,
)
async def profile_package(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    package = profile_segment.package()

    return package


@router.get(
    "/profile/description/variables/",
    response_model=Variables,
    response_model_exclude_none=True,
)
async def profile_variables(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get analysis part of pandas profiling
    profile_segment = ProfileSegments(profile)
    variables = profile_segment.variables()

    return variables


@router.get(
    "/profile/description/duplicates/",
    response_model=Duplicates,
    response_model_exclude_none=True,
)
async def profile_duplicates(
    source: str = environ["EXAMPLE_URL"], minimal: bool = True
):

    dataframe = provide_dataframe(source)

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get duplicates part of pandas profiling
    profile_segment = ProfileSegments(profile)
    duplicates = profile_segment.duplicates()

    return duplicates


@router.get(
    "/profile/description/",
    response_model=Description,
    response_model_exclude_none=True,
)
async def profile_description(
    source: str = environ["EXAMPLE_URL"],
    minimal: bool = True,
    samples_to_show: int = 10,
):
    dataframe = provide_dataframe(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    if dataframe.shape[0] < 100:
        samples_to_show = 5

    profile = ProfileReport(
        dataframe,
        minimal=minimal,
        samples={"head": samples_to_show, "tail": samples_to_show},
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get duplicates part of pandas profiling
    profile_segment = ProfileSegments(profile)
    description = profile_segment.description()

    return description
