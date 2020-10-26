import pytest

from vidispine.errors import NotFound


def test_get_with_no_metadata(vidispine, cassette, collection):
    result = vidispine.collection.get(collection, metadata=False)

    assert result['name'] == 'test_collection_1'
    assert cassette.all_played


def test_get_with_metadata(
    vidispine, cassette, collection, check_field_value_exists
):
    result = vidispine.collection.get(collection)

    fields = result['timespan'][0]['field']
    check_field_value_exists(fields, 'title', 'test_collection_1')
    assert cassette.all_played


def test_not_found_with_no_metadata(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000', metadata=False)

    assert cassette.all_played

    err.match(r'Not Found: GET')


def test_not_found_with_metadata(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: GET')
