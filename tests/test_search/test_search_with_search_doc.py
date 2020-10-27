import json
import uuid

import pytest

from vidispine.errors import InvalidInput


def test_search(
    vidispine,
    cassette,
    collection,
    create_item
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

    result = vidispine.search(metadata)

    assert result['hits'] == 1
    assert 'suggestion' in result
    assert 'autocomplete'
    assert 'item' in result['entry'][0]

    assert cassette.requests[2].method == 'PUT'
    assert json.loads(cassette.requests[2].body) == metadata


def test_search_with_params(
    vidispine,
    cassette,
    collection,
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

    assert cassette.requests[2].method == 'PUT'
    assert json.loads(cassette.requests[2].body) == metadata


def test_search_with_matrix_params(
    vidispine,
    cassette,
    collection,
    create_item
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
        metadata=metadata, matrix_params={'number': 10, 'first': 1}
    )

    assert result['hits'] == 1
    assert 'suggestion' in result
    assert 'autocomplete'
    assert 'item' in result['entry'][0]

    assert cassette.requests[2].method == 'PUT'
    assert json.loads(cassette.requests[2].body) == metadata


def test_search_with_params_and_matrix_params(
    vidispine,
    cassette,
    collection,
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

    assert cassette.requests[2].method == 'PUT'
    assert json.loads(cassette.requests[2].body) == metadata


def test_search_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search({})

    err.match('Please supply metadata.')
