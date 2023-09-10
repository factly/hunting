FROM python:3.10-slim-buster as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN mkdir -p /tmp/app
COPY ./app /tmp/app

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10-slim-buster

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --from=requirements-stage /tmp/app /code/app