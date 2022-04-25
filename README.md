# angelprayer
Calling the Altitude Angel Surveillance API

https://docs.altitudeangel.com/docs/surveillance-api
https://docs.altitudeangel.com/docs/altitude-angel-identity-provider


## Development Setup

It is possible to install Python packages straight from `requirements.txt`.

`python -m pip install -r requirements.txt`

The project is using [pip-tools](https://github.com/jazzband/pip-tools).

For further development, please install it:

`(venv) $ python -m pip install pip-tools`

Then you can alternativelly install all dependencies with the command:

`pip-sync`

More details at [pip-tools](https://github.com/jazzband/pip-tools).

## Running Tests

In the project directory under virtual environment please run:

`python -m unittest discover tests`

## Run from CLI

`uvicorn --port 8000 main:app`

Now go to `http://localhost:8000`

## Build and Run Docker Image

Building the Docker image:

`docker build --tag angelprayer-docker-test .`

Running the image:

`docker run -dp 3000:8000 angelprayer-docker-test`

App should be available there: `http://localhost:3000`
