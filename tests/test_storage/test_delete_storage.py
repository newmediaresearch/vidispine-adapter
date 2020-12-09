import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, storage):
    vidispine.storage.delete(storage['id'])

    assert cassette.all_played


def test_delete_with_params(vidispine, cassette, storage):
    vidispine.storage.delete(storage['id'], {'safe': True})

    assert cassette.all_played


def test_delete_storage_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.storage.delete('VX-1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
