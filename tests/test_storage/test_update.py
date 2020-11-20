import pytest

from vidispine.errors import InvalidInput


@pytest.fixture
def storage_metadata():
    return {
        "type": "LOCAL",
        "capacity": "1500000",
        "method": [{
            "uri": "file:///srv/media1/",
            "read": "true",
            "write": "true",
            "browse": "true"
        }],
        "lowWatermarkPercentage": "90",
        "highWatermarkPercentage": "75",
        "showImportables": "true",
        "metadata": {
            "field": [
                {
                    "key": "name",
                    "value": "test_storage"
                },
                {
                    "key": "excludefilter",
                    "value": "\\..*|.*/\\..*"
                }
            ]
        }
    }


def test_update(vidispine, cassette, storage_metadata):
    storage_id = vidispine.client.request(
        'post', 'storage', json=storage_metadata
    )['id']

    updated_metadata = storage_metadata
    updated_metadata['metadata']['field'][0]['value'] = 'updated_test_storage'

    result = vidispine.storage.update(storage_id, updated_metadata)

    assert result['id'] == storage_id
    assert result['metadata']['field'][0]['value'] == 'updated_test_storage'
    assert cassette.all_played


def test_update_invalid_input(vidispine, cassette, storage_metadata):
    storage_id = vidispine.client.request(
        'post', 'storage', json=storage_metadata
    )['id']

    with pytest.raises(InvalidInput)as err:
        vidispine.storage.update(storage_id, {})

    err.match('Please supply metadata.')

    assert cassette.all_played
