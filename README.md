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

