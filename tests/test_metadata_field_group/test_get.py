import pytest

from vidispine.errors import NotFound


@pytest.fixture
def create_metadata_field_group(vidispine):
    endpoint = f'metadata-field/field-group/field_group_one'
    vidispine.client.request('put', endpoint)


def test_get(vidispine, cassette, create_metadata_field_group):
    result = vidispine.metadata_field_group.get('field_group_one')

    assert result['name'] == 'field_group_one'
    assert cassette.all_played


def test_get_field_group_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.get('field_1000000')

    err.match('Not Found: GET')

    assert cassette.all_played
