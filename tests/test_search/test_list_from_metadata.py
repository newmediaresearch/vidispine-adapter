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


def test_list_from_metadata(
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

    result = vidispine.search.list_from_metadata(metadata)

    assert 'collection' in result['entry'][1]
    assert 'item' in result['entry'][0]
    assert cassette.all_played


def test_list_from_metadata_with_params(
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

    result = vidispine.search.list_from_metadata(
        metadata, {'content': 'metadata'}
    )

    collection_fields = (result
                         ['entry'][1]['collection']
                         ['metadata']['timespan'][0]['field']
                         )

    item_fields = (result
                   ['entry'][0]['item']
                   ['metadata']['timespan'][0]['field']
                   )

    check_field_value_exists(collection_fields, 'field_one', 'pizza')
    check_field_value_exists(item_fields, 'field_one', 'pizza')
    assert cassette.all_played


def test_list_from_metadata_with_matrix_params(
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

    result = vidispine.search.list_from_metadata(
        metadata, {}, {'number': 10, 'first': 1}
    )

    assert 'collection' in result['entry'][1]
    assert 'item' in result['entry'][0]
    assert cassette.all_played


def test_list_from_metadata_with_params_and_matrix_params(
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

    result = vidispine.search.list_from_metadata(
        metadata, {'content': 'metadata'}, {'number': 10, 'first': 1}
    )

    collection_fields = (result
                         ['entry'][1]['collection']
                         ['metadata']['timespan'][0]['field']
                         )

    item_fields = (result
                   ['entry'][0]['item']
                   ['metadata']['timespan'][0]['field']
                   )

    check_field_value_exists(collection_fields, 'field_one', 'pizza')
    check_field_value_exists(item_fields, 'field_one', 'pizza')
    assert cassette.all_played


def test_list_from_metadata_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.search.list_from_metadata({})

    err.match('Please supply metadata.')
