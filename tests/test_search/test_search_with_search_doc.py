import pytest

from vidispine.errors import InvalidInput
from vidispine.utils import generate_metadata


@pytest.fixture
def update_metadata(vidispine):
    def _update_metadata(collection_or_item, vidispine_id):
        endpoint = f'{collection_or_item}/{vidispine_id}/metadata'

        fields = {
            'title': 'My Shared Field',
            'field_one': 'pizza'
        }

        vidispine.client.request(
            'put', endpoint, json=generate_metadata(fields)
        )

    return _update_metadata


@pytest.fixture
def index_of_collection_or_item():
    def _index_of_collection_or_item(result, collection_or_item):
        if collection_or_item in result['entry'][0]:
            return 0
        else:
            return 1

    return _index_of_collection_or_item


def test_search(
    vidispine,
    cassette,
    create_metadata_field,
    update_metadata,
    create_collection,
    create_item
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', create_item)

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
    create_metadata_field,
    update_metadata,
    create_collection,
    create_item,
    index_of_collection_or_item,
    check_field_value_exists
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', create_item)

    metadata = {
        'field': [
            {
                'name': 'field_one',
                'value': [{'value': 'pizza'}]
            }
        ]
    }

    result = vidispine.search(
        metadata=metadata, params={'content': 'metadata'}
    )

    collection_fields = (result
                         ['entry']
                         [index_of_collection_or_item(result, 'collection')]
                         ['collection']['metadata']['timespan'][0]['field']
                         )

    item_fields = (result
                   ['entry']
                   [index_of_collection_or_item(result, 'item')]
                   ['item']['metadata']['timespan'][0]['field']
                   )

    check_field_value_exists(collection_fields, 'field_one', 'pizza')
    check_field_value_exists(item_fields, 'field_one', 'pizza')
    assert cassette.all_played


def test_search_with_matrix_params(
    vidispine,
    cassette,
    create_metadata_field,
    update_metadata,
    create_collection,
    create_item,
    check_field_value_exists
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', create_item)

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
    create_metadata_field,
    update_metadata,
    create_collection,
    create_item,
    index_of_collection_or_item,
    check_field_value_exists
):
    create_metadata_field('field_one')
    update_metadata('collection', create_collection)
    update_metadata('item', create_item)

    metadata = {
        'field': [
            {
                'name': 'field_one',
                'value': [{'value': 'pizza'}]
            }
        ]
    }

    result = vidispine.search(
        metadata=metadata,
        params={'content': 'metadata'},
        matrix_params={'number': 10, 'first': 1}
    )

    collection_fields = (result
                         ['entry']
                         [index_of_collection_or_item(result, 'collection')]
                         ['collection']['metadata']['timespan'][0]['field']
                         )

    item_fields = (result
                   ['entry']
                   [index_of_collection_or_item(result, 'item')]
                   ['item']['metadata']['timespan'][0]['field']
                   )

    check_field_value_exists(collection_fields, 'field_one', 'pizza')
    check_field_value_exists(item_fields, 'field_one', 'pizza')
    assert cassette.all_played


def test_search_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search({})

    err.match('Please supply metadata.')
