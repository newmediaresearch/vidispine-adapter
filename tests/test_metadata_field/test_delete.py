import pytest

from vidispine.errors import NotFound


@pytest.fixture
def get_metadata_field(vidispine, cassette):
    def _get_metadata_field(field_name):
        endpoint = f'metadata-field/{field_name}'

        vidispine.client.request(
            'get',
            endpoint,
        )

    return _get_metadata_field


def test_delete(
    vidispine, cassette, create_metadata_field, get_metadata_field
):
    field_name = 'field_one'
    create_metadata_field(field_name)

    vidispine.metadata_field.delete(field_name)

    with pytest.raises(NotFound):
        get_metadata_field(field_name)

    assert cassette.all_played


def test_delete_field_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field.delete('field1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
