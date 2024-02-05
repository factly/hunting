from fastapi import APIRouter

from app.models.prefetch import Prefetch, PrefetchResponse
from app.utils.tasks import prefetch_profiles

prefetch_router = router = APIRouter()


@router.post("/prefetch/")
async def prefetch_profiles_background(prefetch: Prefetch):
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
    trigger_id = prefetch.trigger_id

    # Prefetch Profiles as a background job
    result = prefetch_profiles.delay(
        urls=urls,
        minimal=minimal,
        samples_to_fetch=samples_to_fetch,
        trigger_id=trigger_id,
    )

    return PrefetchResponse(
        task_id=result.id,
        trigger_id=trigger_id,
    )
