import pytest

from vidispine.errors import NotFound


@pytest.fixture
def create_metadata_field_group(vidispine):
    def _create_metadata_field_group(field_group_name):
        endpoint = f'metadata-field/field-group/{field_group_name}'

        vidispine.client.request('put', endpoint)

    return _create_metadata_field_group


def test_get(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_one'
    create_metadata_field_group(test_field_group_name)

    result = vidispine.metadata_field_group.get(test_field_group_name)

    assert result['name'] == test_field_group_name
    assert cassette.all_played


def test_get_field_group_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.get('field_1000000')

    err.match('Not Found: GET')

    assert cassette.all_played
