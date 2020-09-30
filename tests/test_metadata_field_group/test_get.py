import pytest

from vidispine.errors import NotFound


def test_get(vidispine, cassette, create_metadata_field_group):
    test_field_group_name = create_metadata_field_group
    result = vidispine.metadata_field_group.get(test_field_group_name)

    assert result['name'] == test_field_group_name
    assert cassette.all_played


def test_get_field_group_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.get('field_1000000')

    err.match('Not Found: GET')

    assert cassette.all_played
