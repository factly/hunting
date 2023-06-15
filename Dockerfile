FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

ENV POETRY_VERSION=1.5.1

# Install Poetry
RUN curl -sSL  https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    /opt/poetry/bin/poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml /

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then /opt/poetry/bin/poetry install --no-root ; else /opt/poetry/bin/poetry install --no-root --no-dev ; fi"

COPY . .
ENV PYTHONPATH=/app