from pydantic import BaseModel


class Prefetch(BaseModel):
    urls: list[str]
    minimal: bool = True
    samples_to_fetch: int = 10
