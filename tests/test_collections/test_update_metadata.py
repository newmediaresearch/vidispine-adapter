import re

import pytest

from vidispine.errors import NotFound
from vidispine.utils import generate_metadata


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


def test_update_metadata(
    vidispine, cassette, create_metadata_field, create_collection
):
    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    vidispine.collection.update_metadata(
        create_collection, generate_metadata(fields)
    )

    assert cassette.all_played


def test_update_metadata_field_does_not_exist(
    vidispine, cassette, create_metadata_field, create_collection
):
    create_metadata_field('field_one')
    create_metadata_field('field_two')

    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123,
        'field_three': 'stuff'
    }

    with pytest.raises(NotFound) as err:
        vidispine.collection.update_metadata(
            create_collection, generate_metadata(fields)
        )

        re.match(
            r'Endpoint not found: PUT'
            r' - http://localhost:8080/API/collection/VX-\d+$/metadata', err
        )

    assert cassette.all_played


def test_update_metadata_collection_not_found(vidispine, cassette):
    fields = {
        'title': 'Foo bar',
        'field_one': 'eggs',
        'field_two': 123
    }

    with pytest.raises(NotFound) as err:
        vidispine.collection.update_metadata(
            'VX-1000000', generate_metadata(fields)
        )

    err.match(
        r'Endpoint not found: PUT'
        r' - http://localhost:8080/API/collection/VX-1000000/metadata'
    )

    assert cassette.all_played
