# angelprayer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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


## Linting

The project uses [flake8](https://github.com/PyCQA/flake8) and  [bandit](https://github.com/PyCQA/bandit).
Formatting is done with [black](https://github.com/psf/black).

**Setupping Git hooks**

```
 $ pre-commit install
```

## Environment Setup

The project configuration fields are defined by the [settings.py](.settings.py) file.
All fields present in the settings file can be set via environment variables `.env` file.
Make a copy of the `.env.example` file and change to desired values.

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

Alternatively you can start the app with docker-compose:

`docker-compose up`
