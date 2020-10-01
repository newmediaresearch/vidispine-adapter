import pytest

from vidispine.errors import InvalidInput


def test_update(vidispine, cassette, create_metadata_field):
    field_name = 'field_one'
    create_metadata_field(field_name)

    metadata = {
        'type': 'integer',
        'defaultValue': 0
    }
    result = vidispine.metadata_field.update(metadata, field_name)

    assert result['name'] == field_name
    assert result['type'] == metadata['type']
    assert result['defaultValue'] == str(metadata['defaultValue'])
    assert result['origin'] == 'VX'
    assert cassette.all_played


def test_update_invalid_input(vidispine, create_metadata_field):
    field_name = 'field_one'
    create_metadata_field(field_name)

    with pytest.raises(InvalidInput) as err:
        vidispine.metadata_field.update({}, field_name)

    err.match('Please supply metadata.')
