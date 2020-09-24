import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, create_collection):
    vidispine.collection.delete(create_collection)

    assert cassette.all_played


def test_non_existent_collection(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.collection.delete('VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
