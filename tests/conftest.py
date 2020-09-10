import os

import pytest
import vcr

from vidispine.client import Vidispine


@pytest.fixture
def vidispine():
    return Vidispine('http://localhost:8080', 'admin', 'admin')


@pytest.fixture
def cassette(request):
    my_vcr = vcr.VCR(filter_headers=['authorization'])

    caller_name = request.function.__name__.lstrip('test_')
    cassette_file = f'{caller_name}.yaml'

    cassette_path = os.path.join(
        os.path.dirname(request.module.__file__), 'cassettes', cassette_file
    )
    with my_vcr.use_cassette(path=cassette_path) as cass:
        yield cass


@pytest.fixture
def check_field_value_exists():
    def _check_field_value_exists(fields, field_name, value):
        for field in fields:
            if field['name'] == field_name:
                assert field['value'][0]['value'] == value
                break
        else:
            raise ValueError(f'Value not found: {value}.')

    return _check_field_value_exists
