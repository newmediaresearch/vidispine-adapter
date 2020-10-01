import pytest

from vidispine.errors import NotFound


def test_get(vidispine, cassette, metadata_field_group):
    result = vidispine.metadata_field_group.get(metadata_field_group)

    assert result['name'] == metadata_field_group
    assert cassette.all_played


def test_get_field_group_not_found(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.get('field_1000000')

    err.match('Not Found: GET')

    assert cassette.all_played
