from fastapi.encoders import jsonable_encoder
from ydata_profiling import ProfileReport

from app.core.logging import get_logger
from app.db.mongo import profiles_collection
from app.utils.dataframes import get_dataframe
from app.utils.profile_segments import ProfileSegments
from app.worker import celery

logger = get_logger(__name__)


@celery.task(name="prefetch_profile")
def prefetch_profile(
    url: str, minimal: bool = True, samples_to_fetch: int = 10
):

    """Save Profile to MongoDB

    Args:
        url (str): URL of the Dataset
        description (Description): Pandas-Profile in json
        minimal (bool, optional): Mode of Profile that needs to be fetched. Defaults to True.  # noqa: E501
        samples_to_fetch (int, optional): Samples of Dataset rows to fetch. Defaults to 10.  # noqa: E501
    """

    dataframe = get_dataframe(url)
    logger.info(f"Prefetching Profile for: {url}")

    if dataframe.shape[0] < 100:
        logger.info(f"Dataset has less than 100 rows: {dataframe.shape[0]}")
        logger.info("Samples to fetch set to 5")
        samples_to_fetch = 5

    profile = ProfileReport(
        dataframe.to_pandas(),
        minimal=minimal,
        samples={"head": samples_to_fetch, "tail": samples_to_fetch},
        show_variable_description=False,
        progress_bar=False,
    )

    # use `ProfileSegments` to get duplicates part of pandas profiling
    profile_segment = ProfileSegments(profile, columns=list(dataframe.columns))

    description = profile_segment.description()

    # Add `url` to the description before saving to MongoDB
    description["url"] = url

    # Upsert a json-encoded description into MongoDB
    profiles_collection.update_one(
        {"url": url}, {"$set": jsonable_encoder(description)}, upsert=True
    )
    logger.info(f"Profile Prefetched for: {url}")
    return


@celery.task(name="prefetch_profiles")
def prefetch_profiles(
    urls: list, minimal: bool = True, samples_to_fetch: int = 10
):

    """Save Profiles to MongoDB

    Args:
        urls (list[str]): List of URLs for which the profile needs to be prefetched.  # noqa: E501
            example_url (https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) # noqa: E501
        minimal (bool, optional): Mode of Profile that needs to be fetched. Defaults to True.  # noqa: E501
        samples_to_fetch (int, optional): Samples of Dataset rows to fetch. Defaults to 10.  # noqa: E501
    """

    for url in urls:
        logger.info(f"Added to Queue: {url}")
        prefetch_profile.delay(url, minimal, samples_to_fetch)

    return
