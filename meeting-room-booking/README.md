# Meeting Room Booking System

A console-based Python application for managing users, meeting rooms, and room bookings. It uses Repository and Strategy design patterns and includes time conflict validation for bookings.

## Requirements

- Python 3.10 or higher
- Docker

## Installation and Execution

### 1. Clone the repository

```sh
git clone <REPOSITORY_URL>
cd meeting-room-booking
````

Make sure you have Python 3.10+ installed.

From the directory that contains the `src` folder, run:

```sh
python -m src.main
```

### 3. Run unit tests

```sh
python -m unittest discover tests
```

## Run with Docker

1. Build the image:

```sh
docker build -t meeting-room-booking .
```

2. Run the container:

```sh
docker run -it meeting-room-booking
```

This will start the application in interactive mode in the container’s terminal.

## Project Structure

* `src/` – Main source code
* `tests/` – Unit tests
* `requirements.txt` – Dependencies (empty or only standard modules)
* `Dockerfile` – Used to build the Docker image

## Features

* User and room management
* Booking creation with time overlap validation
* Simple console-based interface
* Repository and Strategy design patterns
* Unit tests using `unittest`
* Docker-ready