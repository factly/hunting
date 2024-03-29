import json
from typing import List

from fastapi import APIRouter, Depends
from ydata_profiling import ProfileReport

from app.core.config import Settings
from app.models.alerts import Alerts
from app.models.analysis import Analysis
from app.models.correlations import Correlations
from app.models.description import Description, ProfileDescriptionRequest
from app.models.duplicates import Duplicates
from app.models.missing import Missing
from app.models.package import Package
from app.models.sample import Sample
from app.models.scatter import Scatter
from app.models.table import Table
from app.models.variables import Variables
from app.utils.dataframes import get_dataframe_async
from app.utils.profile_db import get_profile

profile_router = router = APIRouter()
setting = Settings()


@router.get("/profile/raw/")
async def provide_raw_profiling(
    source: str = setting.EXAMPLE_URL,
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

    dataframe = await get_dataframe_async(source)

    # WHAT?: Change sample sizes based on number of rows
    # WHY?: Fow smaller dataset number of samples to
    if dataframe.shape[0] < 100:
        samples_to_show = 5

    profile = ProfileReport(
        dataframe.to_pandas(),
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
    source: str = setting.EXAMPLE_URL, samples_to_show: int = 10
):
    """
    Get samples for data
    """

    return await get_profile(
        source,
        minimal=True,
        samples_to_show=samples_to_show,
        segment="samples",
    )


@router.get(
    "/profile/description/table/",
    response_model=Table,
    response_model_exclude_none=True,
)
async def profile_table(source: str = setting.EXAMPLE_URL):
    """
    Get table part of pandas profiling for data
    """

    return await get_profile(source, minimal=True, segment="table")


@router.get(
    "/profile/description/analysis/",
    response_model=Analysis,
    response_model_exclude_none=True,
)
async def profile_analysis(source: str = setting.EXAMPLE_URL):
    """
    Get Analysis part of pandas profiling for data
    """

    return await get_profile(source, minimal=True, segment="analysis")


@router.get(
    "/profile/description/alerts/",
    response_model=Alerts,
    response_model_exclude_none=True,
)
async def profile_alerts(source: str = setting.EXAMPLE_URL):

    return await get_profile(source, minimal=True, segment="alerts")


@router.get(
    "/profile/description/scatter/",
    response_model=Scatter,
    response_model_exclude_none=True,
)
async def profile_scatter(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="scatter")


@router.get(
    "/profile/description/correlations/",
    response_model=Correlations,
    response_model_exclude_none=True,
)
async def profile_correlations(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="correlations")


@router.get(
    "/profile/description/missing/",
    response_model=Missing,
    response_model_exclude_none=True,
)
async def profile_missing(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="missing")


@router.get(
    "/profile/description/package/",
    response_model=Package,
    response_model_exclude_none=True,
)
async def profile_package(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="package")


@router.get(
    "/profile/description/variables/",
    response_model=Variables,
    response_model_exclude_none=True,
)
async def profile_variables(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="variables")


@router.get(
    "/profile/description/duplicates/",
    response_model=Duplicates,
    response_model_exclude_none=True,
)
async def profile_duplicates(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="duplicates")


@router.get(
    "/profile/description/columns/",
    response_model=List[str],
    response_model_exclude_none=True,
)
async def profile_columns(
    source: str = setting.EXAMPLE_URL, minimal: bool = True
):

    return await get_profile(source, minimal=minimal, segment="columns")


@router.get(
    "/profile/description/",
    response_model=Description,
    response_model_exclude_none=True,
)
async def profile_description(
    profile_description_request: ProfileDescriptionRequest = Depends(),
):
    return await get_profile(
        url=profile_description_request.source,
        minimal=profile_description_request.minimal,
        samples_to_show=profile_description_request.samples_to_show,
        segment="description",
        attrs=profile_description_request.attrs,
    )
