## {{cookiecutter.project_slug}} Backend

{{cookiecutter.project_slug}} api backend is made of django and celery.

**Important files**

* Source files -> All .py files
* CI configuration file -> .gitlab-ci.yml
* Dockerfile -> Build file

## Running docker file

The system is made out of 2 subcomponents
* master 
* worker
```
master -> Dockerfile
worker -> Dockerfile.worker
```

## Before running docker-compose

```

# Mounting the postgres volume
mkdir data

```

## Running the project

```
docker-compose up --build # only for the first time or you want to rebuild
docker-compose up # after the first time 
```


## Building Image of api

```
docker build -t {{cookiecutter.project_slug}}:latest .
```

## API documentation

On development mode you can run 

https://localhost:8000/swagger # To view the swagger view

https://nusbighero6.gitlab.io/ipredictapi/


