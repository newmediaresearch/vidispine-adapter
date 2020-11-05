import pytest

from vidispine.errors import NotFound


def test_get_without_params(vidispine, cassette, collection):
    result = vidispine.collection.get(collection)

    assert result['name'] == 'test_collection_1'
    assert cassette.all_played


def test_get_with_params(
    vidispine, cassette, collection, check_field_value_exists
):
    result = vidispine.collection.get(collection, {'content': 'metadata'})

    fields = result['metadata']['timespan'][0]['field']
    check_field_value_exists(fields, 'title', 'test_collection_1')
    assert cassette.all_played


def test_collection_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: GET')
