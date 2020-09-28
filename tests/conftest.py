import os
from typing import Any, Callable

import pytest
import vcr
from vcr.cassette import Cassette

from vidispine.client import Vidispine


@pytest.fixture
def vidispine() -> Vidispine:
    return Vidispine('http://localhost:8080', 'admin', 'admin')


@pytest.fixture
def cassette(request: Any) -> Cassette:
    my_vcr = vcr.VCR(
        filter_headers=['authorization'],
        match_on=['method', 'scheme', 'path', 'query', 'body', 'headers']
    )

    cassette_dir = os.path.dirname(request.module.__file__)
    sub_dir_name = request.module.__name__.split('.')[-1]
    sub_dir_path = os.path.join(cassette_dir, 'cassettes', sub_dir_name)

    caller_name = request.node.name.lstrip('test_')
    cassette_file = f'{caller_name}.yaml'

    cassette_path = os.path.join(sub_dir_path, cassette_file)

    with my_vcr.use_cassette(path=cassette_path) as cass:
        yield cass


@pytest.fixture
def check_field_value_exists() -> Callable:
    def _check_field_value_exists(fields: list, field_name: str, value: str):
        for field in fields:
            if field['name'] == field_name:
                assert field['value'][0]['value'] == value
                break
        else:
            raise ValueError(f'Value not found: {value}.')

    return _check_field_value_exists


@pytest.fixture
def create_collection(vidispine: Vidispine, cassette: Cassette) -> str:
    return vidispine.collection.create('test_collection_1')


@pytest.fixture
def create_item(vidispine, cassette):
    metadata = {
        "timespan": [{
            "field": [{
                "name": "title",
                "value": [{
                    "value": "My placeholder import!"
                }]
            }],
            "start": "-INF",
            "end": "+INF"
        }]
    }

    client = vidispine.client
    endpoint = f'{client.base_url}import/placeholder'

    params = {
        'container': 1
    }

    request = client.request(
        'post',
        endpoint,
        json=metadata,
        params=params
    )

    item_id = request['id']

    return item_id


@pytest.fixture
def create_metadata_field(vidispine, cassette):
    def _create_metadata_field(field_name):
        metadata = {
            'type': 'string'
        }

        endpoint = f'metadata-field/{field_name}'

        vidispine.client.request(
            'put',
            endpoint,
            json=metadata
        )

    return _create_metadata_field
