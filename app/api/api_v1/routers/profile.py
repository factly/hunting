import json
from typing import List

from fastapi import APIRouter
from pandas_profiling import ProfileReport
from pydantic import parse_obj_as

from app.core.config import Settings
from app.models.analysis import Analysis
from app.models.sample import Sample
from app.models.table import Table
from app.utils.utils import provide_dataframe

settings = Settings()

profile_router = router = APIRouter()


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
        minimal=True,
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
