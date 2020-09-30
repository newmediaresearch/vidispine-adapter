import pytest


@pytest.fixture
def create_metadata_field_group(vidispine):
    def _create_metadata_field_group(field_group_name):
        endpoint = f'metadata-field/field-group/{field_group_name}'

        vidispine.client.request('put', endpoint)

    return _create_metadata_field_group


def test_list(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    result = vidispine.metadata_field_group.list()
    field_group_names = [group['name'] for group in result['group']]

    assert test_field_group_name in field_group_names
    assert cassette.all_played


def test_list_with_content(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    result = vidispine.metadata_field_group.list({'content': True})
    field_group_names = [group['name'] for group in result['group']]

    assert test_field_group_name in field_group_names
    assert 'schema' in result['group'][0]
    assert cassette.all_played
