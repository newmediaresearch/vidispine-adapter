import pytest

from vidispine.errors import NotFound


def test_get(vidispine, cassette, storage):
    storage_id = storage['id']
    result = vidispine.storage.get(storage_id)

    assert result['id'] == storage_id
    assert cassette.all_played


def test_get_storage_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.storage.get('VX-1000000')

    err.match('Not Found:')
