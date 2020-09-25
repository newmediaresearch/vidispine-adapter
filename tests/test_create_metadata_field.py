import pytest

from vidispine.errors import APIError, InvalidInput


def test_create_metadata_field(vidispine, cassette):
    metadata = {'type': 'string'}
    field_name = 'field_one'
    result = vidispine.create_metadata_field(metadata, field_name)

    assert result['name'] == field_name
    assert result['type'] == 'string'
    assert cassette.all_played


def test_create_metadata_field_invalid_field_name(vidispine, cassette):
    metadata = {'type': 'string'}
    field_name = 'fieldone'

    with pytest.raises(APIError) as err:
        vidispine.create_metadata_field(metadata, field_name)

    err.match('Vidispine Error: PUT')

    assert cassette.all_played


def test_create_metadata_field_invalid_input(vidispine):
    field_name = 'field_one'

    with pytest.raises(InvalidInput) as err:
        vidispine.create_metadata_field({}, field_name)

    err.match('Please supply metadata.')
