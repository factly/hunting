from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pandas_profiling import ProfileReport

from app.core.config import Settings
from app.db.mongo import profiles_collection
from app.models.prefetch import Prefetch
from app.utils.profile_segments import ProfileSegments
from app.utils.util_functions import get_dataframe

prefetch_router = router = APIRouter()
setting = Settings()


@router.post("/prefetch/")
async def prefetch_profiles(prefetch: Prefetch):
    """Prefetch and save Profiles for a list of Datasets

    Args:

        urls (list[str]): List of URLs for which the profile needs to be prefetched.  # noqa: E501
            example_url (https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) # noqa: E501
        minimal (bool, optional): Mode of Profile that needs to be fetched. Defaults to True.  # noqa: E501
        samples_to_fetch (int, optional): Samples of Dataset rows to fetch. Defaults to 10.  # noqa: E501

    Returns:
        response (json): Pandas-Profile in json
    """

    # Step 1: Implement prefetching of Profiles and save to MongoDB
    urls = prefetch.urls
    minimal = prefetch.minimal
    samples_to_fetch = prefetch.samples_to_fetch

    for url in urls:

        # Fetch Profile for each URL
        # TODO: Move the following code to a separate function
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
        profile_segment = ProfileSegments(
            profile, columns=list(dataframe.columns)
        )
        description = profile_segment.description()

        # Save Profiles to `profiles` collection in MongoDB
        # profile = await profiles_collection.insert_one(description)
        # Add `url` to the description before saving to MongoDB
        description["url"] = url

        # Insert a json-encoded description into MongoDB
        profiles_collection.insert_one(jsonable_encoder(description))

    # Step 1.1: Upsert the document based on the URL
    # Step 1.x: Move the prefetching code to a separate function
    # Step 2: Implement prefetching as a background task
    # Step 3: Create a TaskID and return it to the user
    # Step 4: Implement MongoDB insert as async
    return description
