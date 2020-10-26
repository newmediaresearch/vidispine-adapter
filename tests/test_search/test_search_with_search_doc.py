import json
import pytest

from vidispine.errors import InvalidInput
from vidispine.utils import generate_metadata
import uuid


@pytest.fixture
def update_metadata(vidispine):
    def _update_metadata(collection_or_item, vidispine_id):
        endpoint = f'{collection_or_item}/{vidispine_id}/metadata'

        fields = {
            'title': 'foo_bar',
            'field_one': 'pizza'
        }

        vidispine.client.request(
            'put', endpoint, json=generate_metadata(fields)
        )

    return _update_metadata


def test_search(
    vidispine,
    cassette,
    create_metadata_field,
    update_metadata,
    create_collection,
    item
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', item)

    metadata = {
        'field': [
            {
                'name': 'field_one',
                'value': [{'value': 'pizza'}]
            }
        ]
    }

    result = vidispine.search(metadata)

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete'
    assert 'entry'
    assert cassette.all_played


def test_search_with_params(
    vidispine,
    cassette,
    create_collection,
    create_item,
    check_field_value_exists
):
    if cassette.dirty:
        item_uuid = str(uuid.uuid4())
        create_item(item_uuid)
    else:
        create_item_request = json.loads(cassette.requests[1].body)

        item_uuid = (
            create_item_request['timespan'][0]['field'][0]['value'][0]['value']
        )

    metadata = {
        'field': [
            {
                'name': 'title',
                'value': [{'value': item_uuid}]
            }
        ]
    }

    result = vidispine.search(
        metadata=metadata, params={'content': 'metadata'}
    )

    item_fields = (
        result['entry'][0]['item']['metadata']['timespan'][0]['field']
    )

    check_field_value_exists(item_fields, 'title', item_uuid)

    search_request_method = cassette.requests[2].method
    assert search_request_method == 'PUT'


def test_search_with_matrix_params(
    vidispine,
    cassette,
    create_metadata_field,
    update_metadata,
    create_collection,
    item
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', item)

    metadata = {
        'field': [
            {
                'name': 'field_one',
                'value': [{'value': 'pizza'}]
            }
        ]
    }

    result = vidispine.search(
        metadata=metadata, matrix_params={'number': 10, 'first': 1}
    )

    assert result['hits'] > 2
    assert 'suggestion' in result
    assert 'autocomplete'
    assert 'entry'
    assert cassette.all_played


def test_search_with_params_and_matrix_params(
    vidispine,
    cassette,
    create_collection,
    create_item,
    check_field_value_exists
):
    if cassette.dirty:
        item_uuid = str(uuid.uuid4())
        create_item(item_uuid)
    else:
        create_item_request = json.loads(cassette.requests[1].body)

        item_uuid = (
            create_item_request['timespan'][0]['field'][0]['value'][0]['value']
        )

    metadata = {
        'field': [
            {
                'name': 'title',
                'value': [{'value': item_uuid}]
            }
        ]
    }

    result = vidispine.search(
        metadata=metadata,
        params={'content': 'metadata'},
        matrix_params={'number': 10, 'first': 1}
    )

    item_fields = (
        result['entry'][0]['item']['metadata']['timespan'][0]['field']
    )

    check_field_value_exists(item_fields, 'title', item_uuid)

    search_request_method = cassette.requests[2].method
    assert search_request_method == 'PUT'


def test_search_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search({})

    err.match('Please supply metadata.')
