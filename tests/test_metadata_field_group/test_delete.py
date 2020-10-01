import pytest

from vidispine.errors import NotFound


def test_delete(vidispine, cassette, metadata_field_group):
    vidispine.metadata_field_group.delete(metadata_field_group)

    assert cassette.all_played


def test_non_existent_metadata_field_group(vidispine, cassette):
    with pytest.raises(NotFound) as err:
        vidispine.metadata_field_group.delete('field1000000')

    assert cassette.all_played

    err.match(r'Not Found: DELETE')
