import pytest

from vidispine.errors import InvalidInput


def test_update(vidispine, cassette, metadata_field):
    metadata = {
        'type': 'integer',
        'defaultValue': 0
    }
    result = vidispine.metadata_field.update(metadata, metadata_field)

    assert result == {
        'name': metadata_field,
        'type': metadata['type'],
        'defaultValue': str(metadata['defaultValue']),
        'origin': 'VX'
    }
    assert cassette.all_played


def test_update_invalid_input(vidispine, metadata_field):
    with pytest.raises(InvalidInput) as err:
        vidispine.metadata_field.update({}, metadata_field)

    err.match('Please supply metadata.')
