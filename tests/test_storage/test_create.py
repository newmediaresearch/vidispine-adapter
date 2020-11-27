import re

import pytest

from vidispine.errors import InvalidInput


def test_create(vidispine, cassette, storage_metadata):
    result = vidispine.storage.create(storage_metadata)

    assert re.match(r'^VX-\d+$', result['id'])
    assert result['metadata'] == storage_metadata['metadata']

    assert cassette.all_played


def test_create_invalid_input(vidispine):
    with pytest.raises(InvalidInput) as err:
        vidispine.storage.create({})

    err.match('Please supply metadata.')
