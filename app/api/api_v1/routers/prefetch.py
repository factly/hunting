from fastapi import APIRouter

from app.models.prefetch import Prefetch
from app.utils.profile_db import save_profile

prefetch_router = router = APIRouter()


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

    urls = prefetch.urls
    minimal = prefetch.minimal
    samples_to_fetch = prefetch.samples_to_fetch

    for url in urls:
        await save_profile(url, minimal, samples_to_fetch)

    # Step 2: Implement prefetching as a background task
    # Step 3: Create a TaskID and return it to the user
    # Step 4: Implement MongoDB insert as async
    return None
