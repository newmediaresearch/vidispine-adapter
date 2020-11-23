import pytest


@pytest.fixture
def create_multiple_storages(vidispine, cassette, storage_metadata):
    def _create_multiple_storages(quantity):
        storage_ids = []
        for i in range(1, quantity + 1):
            storage_id = vidispine.client.request(
                'post', 'storage', json=storage_metadata
            )['id']

            storage_ids.append(storage_id)

        return storage_ids

    return _create_multiple_storages


def test_list(vidispine, cassette, create_multiple_storages):
    storage_ids = create_multiple_storages(3)

    results = vidispine.storage.list()['storage']

    all_storage_ids = [result['id'] for result in results]

    assert set(storage_ids).issubset(all_storage_ids)
    assert cassette.all_played


def test_list_with_params(vidispine, cassette, create_multiple_storages):
    storage_ids = create_multiple_storages(3)

    results = vidispine.storage.list({'state': 'NONE'})['storage']

    all_storage_ids = [result['id'] for result in results]

    assert set(storage_ids).issubset(all_storage_ids)
    assert cassette.all_played
