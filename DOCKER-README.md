### Prerequisites

- Docker
- Updated environment variables in the docker-compose.yml file
- Access to the dw_p4 and dwdeadline Gitlab repositories, needed to correctly install app dependencies

### Running the Application with Docker Compose

## 1. Build the Docker Image

From the project root directory, build the Docker image:

```sh
docker build -t Flask_API .
```

## 2. Run the Container

Start the container, mapping the desired port (e.g., 8080):

```sh
docker-compose up --build -d
```

The API will be available on port 5000 (http://Flask_API:5000/api/1.0/).
The PostgreSQL database will be accessible on port 5432.

Application logs are mounted in the `logs/` folder of the project.

### Environment Variables

Environment variables are defined in the `docker-compose.yml` file and can be modified as needed (database, logs, etc).

### Stopping the Containers

```sh
docker-compose down
```
