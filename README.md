# Hunting

The easiest way to get started with Hunting is to open it on Gitpod or GitHub Codespaces:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/factly/hunting)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://deshetti-shiny-fiesta-r4g7w969qwr2xppg.github.dev/)

### Pre-requisites

- Currently the setup is only tested for development on Mac OS and Linux
- Install and run Docker and Docker Compose

### Starting the application

- Execute the following command docker-compose command to start the entire NEDC Database application and the dependent services

  ```
    docker-compose up
  ```

- When the application is started using docker-compose, a directory with name `volumes` will be created in the directory where all the docker data for all the services will be persisted.

### Access the application

Once the application is up and running you should be able to access it using the following urls:

| Service | URL |
|--|--|
| Server | API Root: http://0.0.0.0:8000/api/v1 <br> Swagger: http://0.0.0.0:8000/api/docs <br> Redoc: http://0.0.0.0:8000/redoc|
| MongoDB | http://localhost:27017 <br> Username: root <br> Password: example <br>|
| Redis | http://localhost:6379 <br> Password: password|
| Flower | Dashboard: http://localhost:5555|


### Stopping the application

- Execute the following command docker-compose command to stop Dega and all the components

  ```
    docker-compose stop
  ```

Or use the following command to stop the application, and remove all the containers and networks that were created:

  ```
    docker-compose down
  ```

### Environment variables

- Create `.env` file in the root directory based on `.env.example`. 
    - The values in `.env.example` are pre-configured to running the application using the default `docker-compose.yml`
- If no `.env` file is found in the root directory, the default values provided in `/app/core/config.py` will be considered for the environment variables.
    - The values in `/app/core/config.py` are pre-configured to running the application using the default `docker-compose.yml`

### Prefetch

- Prefetch group of routes will only be enabled if `ENABLE_PREFETCH` is `true`
- Flower Dashboard 

### S3

- Limitation is that it will only supports one set of AWS credentials that has access to all the S3 buckets.
- S3 URL expected in the following pattern: `s3://bucket_name/path/to/file/file_name.csv` 

### Background Task

- On Celery: SecurityWarning: You're running the worker with superuser privileges: this is absolutely not recommended!
- Redis Backend configuration: https://docs.celeryq.dev/en/stable/userguide/configuration.html#conf-redis-result-backend
- Confirm about task serialization (Pickle)
- Split task into several chunks: https://docs.celeryq.dev/en/stable/userguide/canvas.html#canvas-chunks
- Take care in PROD:
  - Backends use resources to store and transmit results. To ensure that resources are released, you must eventually call get() or forget() on EVERY AsyncResult instance returned after calling a task.
- Change Redis database from default 0 to best practice
- Make Production Ready: 
  - https://blog.wolt.com/engineering/2021/09/15/5-tips-for-writing-production-ready-celery-tasks/

### TODO
- Error Handling
- Structured Logging: https://calmcode.io/logging/introduction.html
- Convert get_dataframe to async
- Add helm chart
- Create index on MongoDB on `url`: https://motor.readthedocs.io/en/stable/api-tornado/motor_collection.html
- Save and Get from MongoDB only when `ENABLE_PREFETCH` is `True`
- Add all the example csv files into the project directory
- Write unit tests for the functionality