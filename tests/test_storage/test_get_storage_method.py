import pytest

from vidispine.errors import NotFound


def test_get_storage_method(vidispine, cassette, storage, add_storage_method):
    storage_id = storage['id']

    method_id = add_storage_method(storage)

    result = vidispine.storage.get_storage_method(storage_id, method_id)

    assert result['method'][0]['id'] == method_id
    assert cassette.all_played


def test_get_storage_method_storage_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.storage.get_storage_method('VX-1000000', 'VX-1')

    err.match('Not Found: GET')

    assert cassette.all_played


def test_get_storage_method_storage_method_not_found(
    vidispine, cassette, storage
):
    storage_id = storage['id']

    result = vidispine.storage.get_storage_method(storage_id, 'VX-1000000')

    assert result == {}
    assert cassette.all_played


def test_get_storage_method_with_params(
    vidispine, cassette, storage, add_storage_method
):
    storage_id = storage['id']

    method_id = add_storage_method(storage)

    result = vidispine.storage.get_storage_method(
        storage_id, method_id, {'read': True}
    )

    assert result['method'][0]['id'] == method_id
    assert cassette.all_played
