import pytest


@pytest.fixture
def get_metadata_field_group(vidispine):
    def _get_metadata_field_group(field_group_name):
        endpoint = f'metadata-field/field-group/{field_group_name}'
        return vidispine.client.get(endpoint)

    return _get_metadata_field_group


def test_create(vidispine, cassette, get_metadata_field_group):
    test_field_group_name = 'field_one'
    vidispine.metadata_field_group.create(test_field_group_name)

    created_field_group = get_metadata_field_group(test_field_group_name)

    assert created_field_group['name'] == test_field_group_name
    assert cassette.all_played
