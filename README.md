# Hunting

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
| Minio | API: http://localhost:9000 <br> Console: http://localhost:9001 <br> Username: minio <br> Password: password|


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
- 
