from celery import Celery

from app.core.config import Settings

settings = Settings()

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.utils.tasks"],
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["application/json", "application/x-python-serialize"],
)
