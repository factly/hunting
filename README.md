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

---------

## WHAT ? 

#### Different routes present to Upload Profiles to S3? 

1. `api/v1/to_s3/bulk/from_file_urls` 

  **STEP 1 :**

 - *sources* : List of arrays of source urls of file.

    Example : 
      ```
      [
        "https://github.com/curran/data/blob/gh-pages/Rdatasets/csv/Ecdat/Airline.csv",
        "https://github.com/curran/data/blob/gh-pages/Rdatasets/csv/Ecdat/Bids.csv",
        "https://raw.githubusercontent.com/curran/data/gh-pages/Rdatasets/csv/Ecdat/Car.csv"
      ]
      ```
- *actions* : Component of Pandas Profiling Required  

    Example : "description"
  
- *minimal* : Produce minimal Value Pandas Profiling and ignore Correlatation and other stuff.

    Example : True

- *destination* : Folder inside S3 bucket to store files 

    Example : "github-datasets"

- *task_prefix_id* : Generic prefix for task 

    Example : "bulk_from_file_urls"

**STEP 2 :**

- Random task id along with prefix provided will be assigned.
- To check progress of task use `api/v1/bulk/task/details/<TASK-ID>` 

**STEP 3** 

- Once Task is completed then navigate to `http://localhost:9001/login` and login with username  `minio` and password `password`.
- Undder `hunting` bucket there will be a folder name with `github-datasets` and inside that folder there will be all pandas profiling in json format.