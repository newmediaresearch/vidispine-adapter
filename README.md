# Python Vidispine Adapter

A python (3.6+) wrapper around the [Vidispine API](https://apidoc.vidispine.com//latest/)

Note: This is a work in progress and not all of the vidispine endpoints have been implemented yet.

Full documentation coming soon

## Quick start

### Installation

```bash
pip install vidispine-adapter
```

### Basic Usage

To use the Vidispine API you will need a to know the URL, user and password. The user does not need to be the admin user but does need the correct roles for any API call you make

```python
from vidispine.client import Vidispine

vs = Vidispine(url='http://localhost:8080', user='admin', password='admin')
vs.collection.create(name='test_collection_1')
```

If `url`, `user` and `password` are not passed through when initialising, Vidispine will fall back and try and use environmental variables called `VIDISPINE_URL`, `VIDISPINE_USER` and `VIDISPINE_PASSWORD`
```bash
export VIDISPINE_URL="http://localhost:8080"
export VIDISPINE_USER="admin"
export VIDISPINE_PASSWORD="admin"
```

```python
from vidispine.client import Vidispine

vs = Vidispine()
vs.collection.create(name='test_collection_1')
```


## Running tests

This package is setup to use the Pytest framework for testing.
To run tests, simply execute:

    $ pytest tests

To run tests with coverage and flake8 (which is required for all PR's):

    $ make coverage


These tests use [VCR.py](https://vcrpy.readthedocs.io/en/latest/index.html) for easily mocking Vidispine's output whilst also giving accurate mocks. On the first run they will require an active Vidispine instance to work to determine what the mocked output should be. This output is then stored as yaml files in `tests/cassettes/` and will be played back whenever tests are run again.

By default, the tests will check to see if a cassette file exists and use it for the mocked output. If it does not exist then it will attempt to reach Vidispine to fulfill the request and save it as a new cassette.

You can however run the tests and refresh the cassettes with:

    $ pytest tests --vcr-record=new_episodes

If you would only like to refresh on a specific test then specify the test to run like so:

    $ pytest tests -k test_foobar --vcr-record=new_episodes

See [Record modes](https://vcrpy.readthedocs.io/en/latest/usage.html?highlight=new_episodes#record-modes) for more information and other record options.

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
