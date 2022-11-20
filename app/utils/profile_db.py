from fastapi.encoders import jsonable_encoder
from pandas_profiling import ProfileReport

from app.core.config import Settings
from app.db.mongo import profiles_collection
from app.utils.profile_segments import ProfileSegments
from app.utils.util_functions import get_dataframe

setting = Settings()


# TODO: return status after saving to MongoDB
async def save_profile(
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

    if dataframe.shape[0] < 100:
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
    # await profiles_collection.insert_one(jsonable_encoder(description))
    await profiles_collection.update_one(
        {"url": url}, {"$set": jsonable_encoder(description)}, upsert=True
    )

    return description


async def get_profile(
    url: str,
    minimal: bool = True,
    samples_to_show: int = 10,
    segment: str = "description",
):

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
    description = await profiles_collection.find_one({"url": url})

    # Return the profile if exists in MongoDB
    if description:
        if segment == "description":
            return description
        else:
            return description[segment]

    # 1. Generate the profile from scratch
    # 2. Save to MongoDB for subsequent requests
    description = await save_profile(url, minimal, samples_to_show)

    # Return the profile based on the segment
    if segment == "description":
        return description
    else:
        return description[segment]