import pytest
import re

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


def test_create(vidispine, cassette, storage_metadata):
    result = vidispine.storage.create(storage_metadata)

    assert re.match(r'^VX-\d+$', result['id'])
    assert result['metadata'] == storage_metadata['metadata']

    assert cassette.all_played


def test_create_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.storage.create({})

    err.match('Please supply metadata.')
