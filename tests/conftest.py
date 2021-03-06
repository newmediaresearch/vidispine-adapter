import os
import re
from pathlib import Path
from typing import Any, Callable

import pytest
import vcr
from vcr.cassette import Cassette

from vidispine.client import Client, Vidispine


@pytest.fixture
def vidispine() -> Vidispine:
    return Vidispine('http://localhost:8080', 'admin', 'admin')


@pytest.fixture
def test_client() -> Client:
    return Client('http://localhost:8080', 'admin', 'admin')


@pytest.fixture
def cassette(request: Any) -> Cassette:
    my_vcr = vcr.VCR(
        filter_headers=['authorization', 'User-Agent'],
        match_on=['method', 'scheme', 'path', 'query', 'body', 'headers']
    )

    cassette_dir = os.path.dirname(request.module.__file__)
    sub_dir_name = request.module.__name__.split('.')[-1]
    sub_dir_path = os.path.join(cassette_dir, 'cassettes', sub_dir_name)

    caller_name = request.node.name.replace('test_', '', 1)
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
def create_multiple_collections(vidispine):
    def _create_multiple_collections(quantity):
        vidispine_ids = [
            vidispine.client.post(
                'collection', params={'name': f'test_collection_{i}'}
            )['id']
            for i in range(1, quantity + 1)
        ]
        return vidispine_ids

    return _create_multiple_collections


@pytest.fixture
def create_collection(vidispine: Vidispine, cassette: Cassette) -> Callable:
    def _create_collection(name='test_collection_1'):
        params = {'name': name}
        response = vidispine.client.post('collection', params=params)

        return response['id']

    return _create_collection


@pytest.fixture
def collection(create_collection):
    return create_collection()


@pytest.fixture
def create_item(vidispine, cassette):
    def _create_item(title="My placeholder import!"):
        metadata = {
            "timespan": [{
                "field": [{
                    "name": "title",
                    "value": [{"value": title}]
                }],
                "start": "-INF",
                "end": "+INF"
            }]
        }
        endpoint = f'{vidispine.client.base_url}import/placeholder'

        params = {'container': 1}
        request = vidispine.client.request(
            'post', endpoint, json=metadata, params=params
        )
        item_id = request['id']

        return item_id

    return _create_item


@pytest.fixture
def item(create_item):
    return create_item()


@pytest.fixture
def create_metadata_field_group(vidispine, cassette):
    def _create_metadata_field_group(field_group_name):
        endpoint = f'metadata-field/field-group/{field_group_name}'
        vidispine.client.request('put', endpoint)

    return _create_metadata_field_group


@pytest.fixture
def metadata_field_group(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)
    return test_field_group_name


@pytest.fixture
def create_metadata_field(vidispine, cassette):
    def _create_metadata_field(field_name):
        metadata = {
            'type': 'string'
        }

        endpoint = f'metadata-field/{field_name}'

        return vidispine.client.request('put', endpoint, json=metadata)

    return _create_metadata_field


@pytest.fixture
def metadata_field(vidispine, cassette, create_metadata_field):
    result = create_metadata_field('field_one')
    metadata_field_name = result['name']
    return metadata_field_name


@pytest.fixture
def sample_file():
    cwd = Path.cwd()
    path = cwd.joinpath('tests', 'test_media', 'sample-mp4-file.mp4')
    relative_path = path.relative_to(cwd)
    return relative_path


@pytest.fixture
def create_shape(vidispine):
    def _create_shape(item_id):
        metadata = {'id': 'VX'}
        endpoint = f'item/{item_id}/shape/create'

        result = vidispine.client.request('post', endpoint, json=metadata)

        return result['id']

    return _create_shape


@pytest.fixture
def create_multiple_shapes(vidispine, create_shape):
    def _create_multiple_shapes(item_id, quantity=1):
        shape_ids = []
        for i in range(1, quantity + 1):
            shape_ids.append(create_shape(item_id))

        return shape_ids

    return _create_multiple_shapes


@pytest.fixture
def storage_metadata():
    return {
        "type": "LOCAL",
        "capacity": "1500000",
        "method": [{
            "uri": "file:///srv/media1/",
            "read": "true",
            "write": "true",
            "browse": "true"
        }],
        "lowWatermarkPercentage": "90",
        "highWatermarkPercentage": "75",
        "showImportables": "true",
        "metadata": {
            "field": [
                {
                    "key": "name",
                    "value": "test_storage"
                },
                {
                    "key": "excludefilter",
                    "value": "\\..*|.*/\\..*"
                }
            ]
        }
    }


@pytest.fixture
def shape_tag_metadata():
    return {
        "format": "mxf",
        "audio": {
            "codec": "pcm_s24le",
            "bitrate": 1152000
        },
        "video": {
            "scaling": {
                "width": 1920,
                "height": 1080
            },
            "codec": "h264",
            "bitrate": 100000000,
            "preset": [
                "intra100i"
            ],
            "profile": [
                "CBR"
            ],
            "setting": [
                {
                    "key": "codecTagString",
                    "value": "ai15"
                }
            ]
        }
    }


@pytest.fixture
def storage(vidispine, cassette, storage_metadata):
    return vidispine.client.request(
        'post', 'storage', json=storage_metadata
    )


@pytest.fixture
def add_storage_method(vidispine, cassette, storage_metadata):
    def _add_storage_method(storage):
        method_id = storage['method'][0]['id']
        storage_url = 'file:///srv/TEST_LOCATION/'

        headers = {'accept': 'text/plain'}
        params = {'url': storage_url}

        result = vidispine.client.request(
            'put',
            f'storage/{storage["id"]}/method/{method_id}',
            headers=headers,
            params=params
        )

        # Return method id from the plain text response.
        return re.match(method_id, result).group(0)

    return _add_storage_method
