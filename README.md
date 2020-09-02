# Python Vidispine Adapter


## Running tests

This package is setup to use the Pytest framework for testing.
To run tests, simply execute:

    $ pytest tests

To run tests with coverage and flake8 (which is required for all PR's):

    $ make coverage


## Publishing a new version

Install [Poetry](https://python-poetry.org/). This will allow you to easily build and publish the repository.

You will then need to ensure you have a [PyPi](https://pypi.org/) account with permissions to publish builds.
Once you have an account, create an API token and execute the following to save your token:

    $ poetry config pypi-token.pypi my-token

You will then want to add this repo to the Poetry config:

    $ poetry config repositories.vidispine-adapter https://pypi.org/project/vidispine-adapter/

Create a virtualenv using your virtualenv manager of choice. For example:

    $ pyenv virtualenv 3.8 vidispine
    $ pyenv activate vidispine

You can then install the dependencies using Poetry:

    $ poetry install

This will install dependencies from the `poetry.lock` file. If you would like to update the dependencies run:

    $ poetry update


This will update all dependencies. To just update a single dependency:

    $ poetry update requests

See the [docs](https://python-poetry.org/docs/cli/) for more information on this.

You can then build the package:

    $ poetry build


And finally to publish to PyPi:

    $ poetry publish
