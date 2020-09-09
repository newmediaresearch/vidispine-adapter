import pytest
from vidispine.errors import NotFound


@pytest.fixture
def create_collection(vidispine, cassette):
    return vidispine.collection.create('test_collection_2')


def test_get_with_no_metadata(vidispine, cassette, create_collection):
    result = vidispine.collection.get(create_collection, metadata=False)

    assert result['name'] == 'test_collection_2'
    assert cassette.all_played


def test_get_with_metadata(
    vidispine, cassette, create_collection, check_field_value_exists
):
    result = vidispine.collection.get(create_collection)

    fields = result['timespan'][0]['field']
    check_field_value_exists(fields, 'title', 'test_collection_2')
    assert cassette.all_played


def test_not_found_with_no_metadata(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000', metadata=False)

    assert cassette.all_played

    err.match(
        r'Endpoint not found: GET'
        r' - http://localhost:8080/API/collection/VX-1000000'
    )


def test_not_found_with_metadata(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.get('VX-1000000')

    assert cassette.all_played

    err.match(
        r'Endpoint not found: GET'
        r' - http://localhost:8080/API/collection/VX-1000000/metadata'
    )
