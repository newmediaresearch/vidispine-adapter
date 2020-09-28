import pytest

from vidispine.errors import APIError, InvalidInput


def test_create(vidispine, cassette):
    metadata = {'type': 'string'}
    field_name = 'field_one'
    result = vidispine.metadata_field.create(metadata, field_name)

    assert result['name'] == field_name
    assert result['type'] == 'string'
    assert cassette.all_played


def test_create_invalid_field_name(vidispine, cassette):
    metadata = {'type': 'string'}
    field_name = 'fieldone'

    with pytest.raises(APIError) as err:
        vidispine.metadata_field.create(metadata, field_name)

    err.match('Vidispine Error: PUT')

    assert cassette.all_played


def test_create_invalid_input(vidispine):
    field_name = 'field_one'

    with pytest.raises(InvalidInput) as err:
        vidispine.metadata_field.create({}, field_name)

    err.match('Please supply metadata.')
