import pytest

from vidispine.errors import APIError, NotFound


def test_update_storage_method(vidispine, cassette, storage):
    method_id = storage['method'][0]['id']
    storage_url = 'file:///srv/TEST_LOCATION/'

    result = vidispine.storage.update_storage_method(
        storage['id'], method_id, {'url': storage_url}
    )

    assert result['method_id'] == method_id
    assert result['storage_url'] == storage_url
    assert cassette.all_played


def test_storage_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.storage.update_storage_method(
            'VX-1000000', 'test', {'url': 'test'}
        )

    err.match('Not Found: PUT')

    assert cassette.all_played


def test_storage_method_not_found(
    vidispine, cassette, storage
):
    with pytest.raises(NotFound) as err:
        vidispine.storage.update_storage_method(
            storage['id'], 'VX-1000000', {'url': 'test'}
        )

    err.match('Not Found: PUT')

    assert cassette.all_played


def test_no_url_supplied(vidispine, cassette, storage):
    method_id = storage['method'][0]['id']

    with pytest.raises(APIError) as err:
        vidispine.storage.update_storage_method(
            storage['id'], method_id, {'read': False}
        )

    err.match('An invalid parameter was entered.')

    assert cassette.all_played
