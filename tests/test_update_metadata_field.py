import pytest

from vidispine.errors import InvalidInput


def test_update_metadata_field(vidispine, cassette, create_metadata_field):
    field_name = 'field_one'
    create_metadata_field(field_name)

    metadata = {
        'type': 'integer',
        'defaultValue': 0
    }
    result = vidispine.update_metadata_field(metadata, field_name)

    assert result['name'] == field_name
    assert result['type'] == metadata['type']
    assert result['defaultValue'] == str(metadata['defaultValue'])
    assert cassette.all_played


def test_update_metadata_field_invalid_input(vidispine, create_metadata_field):
    field_name = 'field_one'
    create_metadata_field(field_name)

    with pytest.raises(InvalidInput) as err:
        vidispine.update_metadata_field({}, field_name)

    err.match('Please supply metadata.')
