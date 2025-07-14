from typing import Any, Dict, List, Union
from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ydata_profiling import ProfileReport

from app.core.config import Settings
from app.core.logging import get_logger
from app.db.mongo import profiles_collection
from app.utils.dataframes import get_dataframe_async
from app.utils.profile_segments import ProfileSegments
from app.utils.tasks import prefetch_profiles

setting = Settings()
logger = get_logger(__name__)


# TODO: return status after saving to MongoDB
async def save_profile(
    url: str,
    minimal: bool = True,
    samples_to_fetch: int = 10,
    round_to: int = 3,
):

    """Save Profile to MongoDB

    Args:
        url (str): URL of the Dataset
        description (Description): Pandas-Profile in json
        minimal (bool, optional): Mode of Profile that needs to be fetched. Defaults to True.  # noqa: E501
        samples_to_fetch (int, optional): Samples of Dataset rows to fetch. Defaults to 10.  # noqa: E501
    """

    dataframe = await get_dataframe_async(url)
    if dataframe is None or dataframe.is_empty():
        raise ValueError(
            f"Unable to fetch dataframe for url or Dataframe is Null: {url}"
        )

    if dataframe.shape[0] < 100:
        logger.info(f"Dataset has less than 100 rows: {dataframe.shape[0]}")
        logger.info("Samples to fetch set to 5")
        samples_to_fetch = 5

    profile = ProfileReport(
        dataframe.to_pandas(),
        minimal=minimal,
        samples={"head": samples_to_fetch, "tail": samples_to_fetch},
        show_variable_description=False,
        progress_bar=setting.PROGRESS_BAR,
    )

    # use `ProfileSegments` to get duplicates part of pandas profiling
    profile_segment = ProfileSegments(
        profile, columns=list(dataframe.columns), round_to=round_to
    )

    description = profile_segment.description()

    # Add `url` to the description before saving to MongoDB
    description["url"] = url

    # Upsert a json-encoded description into MongoDB
    # await profiles_collection.insert_one(jsonable_encoder(description))
    await profiles_collection.update_one(
        {"url": url}, {"$set": jsonable_encoder(description)}, upsert=True
    )
    logger.info(f"Profile Prefetched for: {url}")
    return description


async def filter_descriptions_with_attrs(
    attrs: Union[List[str], None], description
) -> Dict[str, Any]:
    """Filter out required attributes among complete description

    Args:
        attrs (Union[List[str], None]): Comma separated values for attributes; example : "analysis,samples,variables"
        description (_type_): _description_ : Pandas profiling description which is received either from fetching from store or building it with Pandas Profiling

    Returns:
        Dict[str, Any]: Pandas Profile with selected attributes
    """
    # If filter is None then take all descriptions else pass only required onces
    logger.info(f"Filtering description with attrs: {attrs}")
    if attrs:
        return {attr: description[attr] for attr in attrs}
    return description


async def get_profile(
    url: str,
    minimal: bool = True,
    samples_to_show: int = 10,
    segment: str = "description",
    attrs: Union[str, None] = None,
) -> Dict[str, Any]:

    """Get Profile from MongoDB if exists
       Generate the profile from scratch if not exists and save to MongoDB

    Args:
        url (str): URL of the Dataset
        minimal (bool, optional): Mode of Profile that needs to be fetched. Defaults to True.  # noqa: E501
        samples_to_fetch (int, optional): Samples of Dataset rows to fetch. Defaults to 10.  # noqa: E501

    Returns:
        description (dict): Pandas-Profile in json

    """

    # Get the profile from MongoDB
    logger.info(f"Fetching Profile if exist for: {url}")
    description = await profiles_collection.find_one({"url": url})

    # check what instances are required from description
    attrs = attrs.split(",") if isinstance(attrs, str) else None

    # Return the profile if exists in MongoDB
    if description:
        logger.info(f"Profile exist for: {url}")
        if segment == "description":
            return await filter_descriptions_with_attrs(attrs, description)
        # {attr: description[attr] for attr in attrs.split(",")}
        else:
            return description[segment]
    else:
        logger.error(f"Profile does not exist for: {url}")
        prefetch_profiles.delay(
            urls=[url],
            minimal=minimal,
            samples_to_fetch=samples_to_show,
            trigger_id=str(uuid4()),
        )
        raise HTTPException(
            status_code=404, detail="Profile does not exist for the URL"
        )
