from fastapi import FastAPI

from app.api.api_v1.routers.profile import profile_router
from app.api.api_v1.routers.s3_events import s3_event_router
from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.get(settings.API_V1_STR)
async def root():
    return {"message": "Server is up"}


# Routers
app.include_router(
    profile_router,
    prefix=settings.API_V1_STR,
    tags=["Data Profiling"],
)
app.include_router(
    s3_event_router, prefix=settings.API_V1_STR, tags=["Bulk S3 operations"]
)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
