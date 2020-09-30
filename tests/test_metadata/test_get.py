import pytest

from vidispine.errors import InvalidInput, NotFound


def test_get_metadata_returns_single_field(cassette, vidispine):
    field_name = 'durationTimeCode'

    metadata = vidispine.metadata.get(field_name)

    assert not metadata.get('field')
    assert metadata['name'] == field_name
    assert cassette.all_played


def test_get_metadata_returns_single_field_with_values(cassette, vidispine):
    field_name = 'durationTimeCode'

    params = {
        'includeValues': '1'
    }
    metadata = vidispine.metadata.get(field_name, params=params)

    assert 'values' in metadata
    assert cassette.all_played


def test_get_metadata_errors_without_fieldname(cassette, vidispine):
    field_name = ''

    with pytest.raises(InvalidInput) as err:
        vidispine.metadata.get(field_name)

    err.match(r'Must supply field name')

    assert cassette.all_played


def test_get_metadata_errors_with_incorrect_fieldname(cassette, vidispine):
    field_name = 'doesnotexist'
    with pytest.raises(NotFound) as err:
        vidispine.metadata.get(field_name)

    err.match(r'Not Found: GET')

    assert cassette.all_played
