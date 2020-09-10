import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, create_collection):
    response = vidispine.collection.delete(create_collection)

    assert response is None
    assert cassette.all_played


def test_delete_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.delete('VX-1000000')

    assert cassette.all_played

    err.match(
        r'Endpoint not found: DELETE'
        r' - http://localhost:8080/API/collection/VX-1000000'
    )
