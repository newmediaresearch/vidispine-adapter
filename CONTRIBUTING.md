# How to contribute

Thanks for wanting to contribute to the Python Vidispine adapter. This adapter is intended to be a 'thin' wrapper around the Vidispine API and includes no business logic.

Important Paddle resources:


  * [Vidispine docs](https://apidoc.vidispine.com//latest/)
  * [Vidispine](https://www.vidispine.com)
  * [NMR](http://nmr.com/) - The current maintainers of this repo


Python resources:

  * [Poetry](https://python-poetry.org/) for python dependency management and packaging
  * [pytest](https://docs.pytest.org/en/latest/) for running test
  * [VCR.py](https://vcrpy.readthedocs.io/) for easy to refresh mocks
  * [Mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
  * [isort](https://timothycrosley.github.io/isort/) to keep all our imports looking nice and easy to read
  * [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)


## Summary

Please see the sections below for more details

1. Fork this repo
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Make your code changes and write your tests
1. Ensure all the tests pass (`pytest tests/`)
1. Check all coding conventions are adhered to (`tox`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create new pull request


## Setup

It encourage that you have [pyenv](https://github.com/pyenv/pyenv) installed and setup with each minor version of Python above 3.6 so you can easily run your tests against each version via `tox` before publishing to pypi.

This project uses the [Poetry](https://python-poetry.org/) for packaging and dependency management. Before you get started please install it.

Once you have the above setup and have cloned this repository you will then need:
* A running Vidispine to do requests against
* The username and password for a Vidispine user with the `_administrator` role.


```bash
# Fork and clone this repo
poetry install

# Create a file called .env and add the above settings
export VIDISPINE_URL="http://localhost:8080"
export VIDISPINE_USER="admin"
export VIDISPINE_PASSWORD="admin"

poetry shell
source .env
```

## Running tests

This package is setup to use the Pytest framework for testing.
To run tests, simply execute:
```bash
pytest tests/
```

A coverage report will displayed in the shell on each test run as well as written to `htmlcov/` and can be viewed with `open htmlcov/index.html`



### Mocking tests

Tests use [VCR.py](https://vcrpy.readthedocs.io/en/latest/index.html) for easily mocking Vidispine's output whilst also giving the ability to refresh mocks to ensure they are accurate. Mocks in VCR.py are know as cassettes. On the first run they will require an active Vidispine instance to work to determine what the mocked output should be. This output is then stored as yaml files in `<test_module>/cassettes/` and will be played back whenever tests are run again.

By default, the tests will check to see if a cassette file exists and use it for the mocked output. If it does not exist then it will attempt to reach Vidispine to fulfill the request and save it as a new cassette.


#### Creating mocks

To ensure cassettes in sane default locations a cassette fixture has been created [conftest.py](https://github.com/newmediaresearch/vidispine-adapter/blob/master/tests/conftest.py). Whenever a test is written which calls Vidispine (which you want to mock via VCR.py), you can simply include the `cassette` as a arg in your function / method like a normal pytest fixture.

It is then possible to use `cassette.requests` to get back data on the request to Vidispine. For example:

```python
def test_create(vidispine, cassette):
    result = vidispine.collection.create('test_collection_1')

    last_request = cassette.requests[0]
    url = urlparse(last_request.url)

    assert re.match(r'^VX-\d+$', result)
    assert cassette.play_count == 1
    assert parse_qs(url.query) == {'name': ['test_collection_1']}
```

#### Refreshing mocks

If you would to refresh ALL the cassettes, for example to test against a new Vidispine version you can run:
```bash
pytest tests --vcr-record=new_episodes
```

If you need to update a mock / cassette for a specific test due to a change, you can refresh the cassettes for a single test with:
```bash
pytest tests -k test_foobar --vcr-record=new_episodes
```

See [Record modes](https://vcrpy.readthedocs.io/en/latest/usage.html?highlight=new_episodes#record-modes) for more information and other record options.



## tox

`tox` is set up to help run `pytest` against each of the supported versions (python 3.6+). It will also ensure the above code conventions are adhered to by running, `mypy`, `flake8` and `isort` against your code.

To use tox to test against different Python versions you first need to follow the test setup above and ensure pyenv is installed. Once that is complete install each of the python 3 minor versions via pyenv:
```bash
pyenv install --list
pyenv install 3.6.x
pyenv install 3.7.x
pyenv install 3.8.x
```

Finally run tox:
```bash
$ tox
```


## Coding conventions

* We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a guide
* All functions / methods in the vidispine module should have type hints for arg / kwargs and responses (checked by mypy)
* Make sure everything is flake8 compliment
* Use `isort` to sort imports and make them easy to read
* String formatting should generally use `fstrings`
* Please keep to the same style as the code already (single quotes, line length etc)



## Submitting changes

Please send a [GitHub Pull Request to paddle-python](https://github.com/newmediaresearch/vidispine-adapter/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)).

All changes should have at least one test to accompany it, either to prove the bug it is fixing has indeed been fixed on to ensure a new feature works as expected.

Please follow our coding conventions and try and make all of your commits atomic (one feature per commit) where possible.



## Documentation

Comming soon



## Updating dependencies

See the [docs](https://python-poetry.org/docs/cli/) for more information on this.

This will install dependencies from the `poetry.lock` file. If you would like to update the dependencies run:
```bash
poetry update
```

This will update all dependencies. To just update a single dependency:
```bash
poetry update requests
```



## Publishing to PyPi

Install [Poetry](https://python-poetry.org/) as above. This will allow you to easily build and publish the repository.

You will then need to ensure you have a [PyPi](https://pypi.org/) account with permissions to publish builds. You will also  have to be added as a `Collaborator` in PyPi

Once you have your account setup, create an API token and execute the following to save your token:
```bash
poetry config pypi-token.pypi my-token
```

You will then want to add this repo to the Poetry config:
```bash
poetry config repositories.vidispine-adapter https://pypi.org/project/vidispine-adapter/
```

You can then build the package:
```bash
poetry build
```

And finally to publish to PyPi:
```bash
poetry publish
```
