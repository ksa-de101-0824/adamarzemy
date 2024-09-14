# FastAPI Docker Application with Persistent Storage Guide

This document provides notes and commands for building and running a Docker container for a FastAPI application with persistent storage.

## Application Details

The application is a FastAPI server that accepts user input via POST requests and stores it in a file. It also provides a GET endpoint to retrieve all stored inputs.

```python
from fastapi import FastAPI, Form

app = FastAPI()

FILE_PATH = "/data/storage.txt"  # Path to store user inputs in the volume

@app.post("/submit/")
def submit_input(user_input: str = Form(...)):
    # Save the user input to the file
    with open(FILE_PATH, "a") as f:
        f.write(user_input + "\n")
    return {"status": "Input received", "input": user_input}

@app.get("/")
def read_inputs():
    # Read all inputs from the file
    try:
        with open(FILE_PATH, "r") as f:
            content = f.read().splitlines()
    except FileNotFoundError:
        content = []
    return {"saved_inputs": content}
```

## Dockerfile

The Dockerfile uses Ubuntu 22.04 as the base image and sets up the environment for running the FastAPI application with persistent storage.

```dockerfile
# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory to /app inside the container
COPY . /app

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install FastAPI and Uvicorn using pip
RUN pip3 install fastapi uvicorn

# Create the /data directory for persistent storage
RUN mkdir /data

# Declare that /data will be used as a volume
VOLUME /data

# Expose port 8080 for the FastAPI app
EXPOSE 8080

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Docker Commands

### Creating Persistent Storage Directory

Before building the Docker image, create a directory on your host machine for persistent storage:

```bash
mkdir -p /workspaces/Docker-Notes/Third_Docker/data
```

### Building the Docker Image

To build the Docker image, use the following command:

```bash
sudo docker build -t fastapi_volume_app:latest .
```

- `fastapi_volume_app` is the image name
- `.` refers to the current directory containing the Dockerfile

### Running the Docker Container with Volume

To run the container with persistent storage, use:

```bash
sudo docker run -d -p 8080:8080 -v /workspaces/Docker-Notes/Third_Docker/data:/data --name fastapi_volume_container fastapi_volume_app:latest
```

- `-d` runs the container in detached mode (in the background)
- `-p 8080:8080` maps port 8080 from the container to port 8080 on the host
- `-v /workspaces/Docker-Notes/Third_Docker/data:/data` mounts the host directory to `/data` in the container
- `--name fastapi_volume_container` assigns a custom name to the container
- `fastapi_volume_app` is the name of the image

### Stopping the Docker Container

To stop the running container:

```bash
sudo docker stop fastapi_volume_container
```

### Removing the Docker Container

To remove the stopped container:

```bash
sudo docker rm fastapi_volume_container
```

### Listing All Containers

To see all containers (running and stopped):

```bash
sudo docker ps -a
```

### Removing the Docker Image

To remove the Docker image:

```bash
sudo docker rmi fastapi_volume_app
```

## Additional Notes

1. **Persistent Storage**: The directory `/workspaces/Docker-Notes/Third_Docker/data` on your host machine is mounted to `/data` inside the container. This ensures that data persists even if the container is stopped or removed.

2. **Volume Declaration**: The `VOLUME /data` instruction in the Dockerfile declares that the `/data` directory will be used as a volume.

3. **File Storage**: User inputs are stored in `/data/storage.txt` inside the container, which corresponds to `/workspaces/Docker-Notes/Third_Docker/data/storage.txt` on your host machine.

4. **Data Persistence**: Even after removing the container, the data will persist in the directory on your host machine.

5. **Port Mapping**: The `-p 8080:8080` option maps port 8080 from the container to port 8080 on the host, allowing you to access the FastAPI application from your host machine.

Remember to adjust file paths and commands based on your specific setup and requirements.