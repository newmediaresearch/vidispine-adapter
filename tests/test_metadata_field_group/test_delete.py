import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = 'field_group_one'
    create_metadata_field_group(test_field_group_name)

    vidispine.metadata_field_group.delete(test_field_group_name)

    assert cassette.all_played


def test_non_existent_metadata_field_group(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.delete('field1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
